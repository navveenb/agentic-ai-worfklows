"""
Portfolio Analysis using CrewAI with Zerodha Kite MCP

This script demonstrates how to interact with the Zerodha Kite MCP server using CrewAI agents,
retrieve portfolio holdings, and perform LLM-based portfolio analysis—all within a modular,
reproducible Python workflow.

Author: Navveen Balani
License: MIT
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
import re
import webbrowser

# -- MCP Server Connection Parameters --
server_params = {
    "url": "https://mcp.kite.trade/sse",  # For local server use: "http://localhost:8080/sse"
    "transport": "sse"
}

def extract_login_url(text):
    """
    Extracts the first HTTP(S) login URL from tool output.
    Handles both markdown link and plain text formats, robust to line breaks.
    """
    # Try to extract markdown link: [label](url)
    markdown_url = re.search(r'\[.*?\]\((https?://[^\s)]+)\)', text, re.DOTALL)
    if markdown_url:
        return markdown_url.group(1).replace('\n', '')
    # Fix cases where URLs are broken by line breaks
    text = re.sub(r'(https?://[^\s\)\]]+)\s*\n\s*([^\s\)\]]+)', r'\1\2', text)
    # Extract raw URL
    url_pattern = r'(https?://[^\s\)\]]+)'
    urls = re.findall(url_pattern, text)
    if urls:
        return urls[0]
    return None

try:
    # Use MCPServerAdapter as a context manager to ensure clean connect/disconnect
    with MCPServerAdapter(server_params) as tools:
        print(f"Available tools from Zerodha SSE MCP server: {[tool.name for tool in tools]}")

        # --- 1. Login Step: Fetch login tool and trigger login ---
        login_tool = next((tool for tool in tools if tool.name == "login"), None)
        if not login_tool:
            print("login tool not found.")
            exit()

        # Define a simple agent for login
        login_agent = Agent(
            role="Zerodha Login User",
            goal="Login to Zerodha via MCP.",
            backstory="Authenticates using the Kite API.",
            tools=[login_tool],
            reasoning=False,
            verbose=True,
        )

        login_task = Task(
            description="Login to Zerodha MCP.",
            expected_output="Return the login URL which must be opened in a browser to complete authentication.",
            agent=login_agent,
            markdown=True,
            max_retries=0,  # Only one attempt, no retries
        )

        login_crew = Crew(
            agents=[login_agent],
            tasks=[login_task],
            verbose=True,
            process=Process.sequential
        )

        print("\n=== Running: login ===")
        login_result = login_crew.kickoff()
        print("\nlogin result:\n", login_result)

        # Parse and launch the login URL in the default web browser
        login_url = extract_login_url(str(login_result))
        if login_url:
            print(f"\nOpen this URL in your browser to complete login:\n{login_url}\n")
            webbrowser.open(login_url)
        else:
            print("\nNo login URL found in result. Check output above.")

        # --- 2. Portfolio Retrieval Step: Get holdings tool and fetch portfolios ---
        get_holdings_tool = next((tool for tool in tools if tool.name == "get_holdings"), None)
        if not get_holdings_tool:
            print("get_holdings tool not found.")
        else:
            # Define an agent for holdings retrieval
            zerodha_agent = Agent(
                role="Zerodha User",
                goal="Run the 'get_holdings' Zerodha tool.",
                backstory="AI agent testing Zerodha 'get_holdings' endpoint.",
                tools=[get_holdings_tool],
                reasoning=True,
                verbose=True,
            )
            zerodha_task = Task(
                description="Show my current stock holdings.",
                expected_output="Output of the get_holdings tool.",
                agent=zerodha_agent,
                markdown=True,
                max_retries=0,  # Only one attempt, no retries
            )
            zerodha_crew = Crew(
                agents=[zerodha_agent],
                tasks=[zerodha_task],
                verbose=True,
                process=Process.sequential
            )
            print("\n=== Running: get_holdings ===")
            try:
                holdings_result = zerodha_crew.kickoff()
                print("------ start -----")
                print(holdings_result)
                print("------ done -----")
                print("\nCrew Task Result (holdings):\n", holdings_result)

                # --- 3. Portfolio Analysis Step: Analyze with LLM agent ---
                analysis_agent = Agent(
                    role="Portfolio Analysis Assistant",
                    goal="Parse the raw stock holdings output and generate a full portfolio analysis report.",
                    backstory="Expert in financial data extraction and analysis.",
                    reasoning=True,
                    verbose=True,
                    llm="openai/gpt-4o",  # Specify your LLM (adjust if needed)
                )
                # - Given below is the sample prompt
                # - You cam modify the prompt to add complex analysis for portfolio recommendations.
                analysis_prompt = f"""
                You are a senior portfolio analyst.

                Given only the raw stock holdings listed below, do not invent or assume any other holdings.

                **Perform just these two analyses:**

                1. **Concentration Risk**: Identify if a significant percentage of the total portfolio is allocated to a single stock or sector. Quantify the largest exposures, explain why this matters, and suggest specific diversification improvements.

                2. **Performance Standouts**: Clearly identify the best and worst performing stocks in the portfolio (by absolute and percentage P&L), and give actionable recommendations (e.g., “Consider booking profits,” “Monitor for recovery or exit,” etc).

                Raw holdings:

                {str(holdings_result)}
                
                For each section, include concise, actionable insights (no generic explanations). Use only the provided data.
                """

                analysis_task = Task(
                    description=analysis_prompt,
                    expected_output="A comprehensive markdown report, starting with parsed holdings, then all portfolio analysis steps.",
                    agent=analysis_agent,
                    markdown=True,
                    max_retries=0,
                )

                analysis_crew = Crew(
                    agents=[analysis_agent],
                    tasks=[analysis_task],
                    verbose=True,
                    process=Process.sequential
                )
                print("\n=== Running: portfolio analysis with LLM ===")
                analysis_report = analysis_crew.kickoff()
                print("\n=== Portfolio Analysis Report ===\n")
                print(analysis_report)

            except Exception as e:
                print(f"Error running get_holdings: {e}")

except Exception as e:
    print(f"Error connecting to or using SSE MCP server (Managed): {e}")
    print("Ensure the SSE MCP server is running and accessible at the specified URL.")
