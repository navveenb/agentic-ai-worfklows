import os
import asyncio
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams

import warnings
warnings.filterwarnings("ignore")

# Load environment variables from .env file if present
load_dotenv('.env')  # Adjust path if your .env is elsewhere

# === Config ===
MCP_SSE_URL = os.environ.get("MCP_SSE_URL", "https://mcp.kite.trade/sse")
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("Missing GOOGLE_API_KEY. Set it in your environment or .env file.")
os.environ["GOOGLE_API_KEY"] = google_api_key
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

async def get_agent_async():
    toolset = MCPToolset(
        connection_params=SseServerParams(
            url=MCP_SSE_URL,
            headers={},
        ),
    )
    root_agent = LlmAgent(
        model='gemini-2.0-flash',
        name='zerodha_portfolio_assistant',
        instruction=(
            "You are an expert Zerodha portfolio assistant. "
            "Use the 'login' tool to authenticate, and the 'get_holdings' tool to fetch stock holdings. "
            "When given portfolio data, analyze for concentration risk and best/worst performers."
        ),
        tools=[toolset]
    )
    return root_agent, toolset

def extract_text_from_event(event):
    if getattr(event, "content", None) and getattr(event.content, "parts", None):
        text = getattr(event.content.parts[0], "text", None)
        if text:
            return text
    return None

async def async_main():
    session_service = InMemorySessionService()
    artifacts_service = InMemoryArtifactService()

    session = await session_service.create_session(
        state={}, app_name='zerodha_portfolio_app', user_id='user1'
    )

    root_agent, toolset = await get_agent_async()
    runner = Runner(
        app_name='zerodha_portfolio_app',
        agent=root_agent,
        artifact_service=artifacts_service,
        session_service=session_service,
    )

    try:
        # Step 1: Login (get login URL)
        login_query = "Authenticate and provide the login URL for Zerodha."
        content = types.Content(role='user', parts=[types.Part(text=login_query)])
        events_async = runner.run_async(
            session_id=session.id, user_id=session.user_id, new_message=content
        )
        login_url = None
        async for event in events_async:
            result = extract_text_from_event(event)
            if event.is_final_response() and result:
                import re
                match = re.search(r'(https?://[^\s)]+)', result)
                if match:
                    login_url = match.group(1)
        if not login_url:
            print("No login URL found. Exiting.")
            await toolset.close()
            return
        print(f"Open this URL in your browser and complete login:\n{login_url}\n")
        import webbrowser
        webbrowser.open(login_url)
        input("Press Enter after completing login...")

        # Step 2: Fetch holdings
        holdings_query = "Show my current stock holdings."
        content = types.Content(role='user', parts=[types.Part(text=holdings_query)])
        events_async = runner.run_async(
            session_id=session.id, user_id=session.user_id, new_message=content
        )
        holdings_raw = None
        async for event in events_async:
            result = extract_text_from_event(event)
            if event.is_final_response() and result:
                holdings_raw = result

        if not holdings_raw:
            print("No holdings data found. Exiting.")
            await toolset.close()
            return

        # Step 3: Portfolio Analysis
        analysis_prompt = f"""
You are a senior portfolio analyst.

Given only the raw stock holdings listed below, do not invent or assume any other holdings.

**Perform just these two analyses:**

1. **Concentration Risk**: Identify if a significant percentage of the total portfolio is allocated to a single stock or sector. Quantify the largest exposures, explain why this matters, and suggest specific diversification improvements.

2. **Performance Standouts**: Clearly identify the best and worst performing stocks in the portfolio (by absolute and percentage P&L), and give actionable recommendations (e.g., “Consider booking profits,” “Monitor for recovery or exit,” etc).

Raw holdings:

{holdings_raw}

For each section, include concise, actionable insights (no generic explanations). Use only the provided data.
"""
        content = types.Content(role='user', parts=[types.Part(text=analysis_prompt)])
        events_async = runner.run_async(
            session_id=session.id, user_id=session.user_id, new_message=content
        )
        async for event in events_async:
            text = extract_text_from_event(event)
            if event.is_final_response() and text:
                print("\n=== Portfolio Analysis Report ===\n")
                print(text)
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            await toolset.close()
        except Exception:
            pass

if __name__ == '__main__':
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"An error occurred at top level: {e}")
