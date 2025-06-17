import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool
from crewai.tools import BaseTool

# --- Load API key ---
load_dotenv('.env')
#if not os.getenv("OPENAI_API_KEY"):
#    raise ValueError("OPENAI_API_KEY not set in environment or .env")
google_api_key = os.environ.get("GEMINI_API_KEY")
if not google_api_key:
    raise ValueError("Missing GEMINI_API_KEY. Set it in your environment or .env file.")
os.environ["GEMINI_API_KEY"] = google_api_key
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

# --- Static file reader ---
legacy_code_tool = FileReadTool(file_path='legacy_app/Main.java')

# --- LLMTool using CrewAI pattern ---
class CompatibilityCheckerTool(BaseTool):
    name: str = "llm_compatibility_checker"
    description: str = "Uses LLM to detect Java compatibility issues."

    def _run(self, input_text: str) -> str:
        return (
            "Use this prompt inside your agent:\n\n"
            f"Please analyze the following Java code and list potential compatibility issues with Java 17. "
            f"For each issue, explain the root cause and suggest fixes:\n\n{input_text}"
        )


class RefactorSuggestionTool(BaseTool):
    name: str = "llm_refactor_suggestions"
    description: str = "Uses LLM to suggest modern Java refactoring."

    def _run(self, input_text: str) -> str:
        return (
            "Use this prompt inside your agent:\n\n"
            f"Review this Java code and provide refactoring suggestions using modern Java features "
            f"(e.g., lambdas, streams, var, switch expressions). Explain the benefits for each:\n\n{input_text}"
        )

# --- Agent Definitions ---

assessment_agent = Agent(
    role="Legacy Code Assessor",
    goal="Identify deprecated constructs in Java code",
    backstory="Expert in legacy Java analysis for modernization planning.",
    tools=[legacy_code_tool],
    verbose=True
)

compatibility_agent = Agent(
    role="Java Compatibility Checker",
    goal="Use the provided tool prompt to guide a compatibility analysis with Java 17+",
    backstory="Knows what to ask and how to reason through compatibility issues.",
    tools=[CompatibilityCheckerTool()],
    verbose=True,
    #llm="openai/gpt-4o"
    llm="gemini/gemini-2.0-flash"
)

refactor_agent = Agent(
    role="Refactor Advisor",
    goal="Use the tool prompt to provide modern refactoring suggestions",
    backstory="Knows modern Java practices and how to prompt LLMs for code improvements.",
    tools=[RefactorSuggestionTool()],
    verbose=True,
     #llm="openai/gpt-4o"
    llm="gemini/gemini-2.0-flash"
)

report_agent = Agent(
    role="Migration Report Generator",
    goal="Summarize all findings into a comprehensive migration report",
    backstory="Expert in compiling multi-step outputs into a developer-ready plan.",
    verbose=True,
     #llm="openai/gpt-4o"
    llm="gemini/gemini-2.0-flash"
)

# --- Task Definitions ---

assessment_task = Task(
    description="Read the Java code and assess any legacy constructs.",
    expected_output="List of deprecated or legacy Java constructs found in the code.",
    agent=assessment_agent
)

compatibility_task = Task(
    description="Use the LLM prompt from the tool to identify compatibility issues with Java 17 and suggest upgrades.",
    expected_output="List of Java 17 compatibility issues and corresponding solutions.",
    agent=compatibility_agent
)

refactor_task = Task(
    description="Use the tool to prompt for modern Java refactoring ideas and suggest changes.",
    expected_output="Refactoring suggestions using Java 8+ syntax and best practices.",
    agent=refactor_agent
)

report_task = Task(
    description=(
        "Summarize findings into a clear markdown report. Include:\n"
        "- Legacy patterns\n"
        "- Compatibility issues\n"
        "- Refactoring suggestions"
    ),
    expected_output="Migration plan report in markdown format.",
    agent=report_agent,
    markdown=True
)

# --- Crew Setup ---

migration_crew = Crew(
    agents=[assessment_agent, compatibility_agent, refactor_agent, report_agent],
    tasks=[assessment_task, compatibility_task, refactor_task, report_task],
    verbose=True,
    process=Process.sequential
)

# --- Run ---

if __name__ == "__main__":
    print("🚀 Launching Java Migration Crew")
    report = migration_crew.kickoff()
    print("\n📋 Final Migration Report:\n")
    print(report)
