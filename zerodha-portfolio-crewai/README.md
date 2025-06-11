# Zerodha Portfolio Analysis with CrewAI & Kite MCP

This repository demonstrates how to automate portfolio retrieval and analysis using [CrewAI](https://crewai.com/) agent workflows and [Zerodha Kite MCP](https://github.com/zerodha/kite-mcp-server) (Model Control Protocol) tools.

**What you can do with this project:**
- Authenticate with Zerodha through a secure, agent-assisted flow,
- Retrieve your live portfolio holdings using the `get_holdings` tool,
- Analyze portfolio risks and performance with a Large Language Model (LLM) agent.

---

## 🛠 Technologies Used

- **CrewAI:** Python framework for building multi-agent, tool-using workflows (supports LLMs and real APIs).
- **Zerodha Kite MCP:** An API and SSE server providing access to your Zerodha trading account for LLMs and agents.
- **OpenAI GPT-4o:** Used for automated portfolio analytics.

---

## 🚦 How It Works

1. **Connects to the MCP server:**  
   The script connects to the Zerodha MCP server (either the official endpoint or your local instance).

2. **Login with Zerodha:**  
   The tool automatically launches the OAuth login URL in your browser.  
   Enter your Zerodha credentials in the browser window and authorize access.  
   (Your credentials are never passed to or processed by the script.)

3. **Fetch portfolio holdings:**  
   The `get_holdings` tool is called after authentication. This retrieves your current stock holdings as raw data.

4. **LLM-powered analysis:**  
   The output is passed to a portfolio analysis agent (using GPT-4o by default) which provides:
   - **Concentration risk** insights,
   - **Performance standouts** (best/worst stocks) and actionable recommendations.

---

## 💻 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/zerodha-portfolio-crewai.git
cd zerodha-portfolio-crewai
```

### 2. Install Python Dependencies

```bash
pip install crewai crewai-tools openai
```

> You’ll need Python 3.9+.

### 3. (Optional) Set up your local MCP server

- See [Kite MCP Server GitHub](https://github.com/zerodha/kite-mcp-server) for installation.
- By default, the script uses the hosted server at `https://mcp.kite.trade/sse`.

---

## 🚀 Running the Script

```bash
python portfolio_analysis.py
```

- The script will launch your browser with a login URL.
- Enter your Zerodha credentials in the browser window and complete the authentication process.
- After authentication, the script will retrieve your holdings and run LLM-powered analysis.

---

## ⚠️ Notes

- **Manual Login:** For security, the script launches the OAuth login URL in your browser. Your credentials are only entered in the browser, never handled or stored by the script.
- **Session Expiry:** If your session expires, re-run the script and complete login again.
- **Data Privacy:** The script does not log or store your personal data.
- **LLM Usage:** Analysis requires OpenAI API access (or other LLM support—see [CrewAI docs](https://docs.crewai.com/)).

---

## 📝 Customizing

- To analyze other data (e.g., orders, margins), change the tool and prompt logic in the script.
- You can switch to another LLM by changing the `llm` parameter in the analysis agent.

---

## 📄 License

MIT

---

## 📚 References

- [CrewAI Documentation](https://docs.crewai.com/)
- [Zerodha Kite MCP](https://github.com/zerodha/kite-mcp-server)
- [Zerodha Kite Connect API](https://kite.trade/docs/connect/v3/)
- [OpenAI Platform](https://platform.openai.com/)

---

*This repository is for educational, research, and personal portfolio analysis purposes only. Not investment advice.*
