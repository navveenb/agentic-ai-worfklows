# Zerodha Portfolio Analysis with Google ADK & MCP

This project demonstrates how to automate portfolio retrieval and analysis using [Google ADK](https://google.github.io/adk-docs/) and Zerodha's [Kite MCP](https://github.com/zerodha/kite-mcp-server) (Model Control Protocol) tools, powered by a Large Language Model (LLM) agent.

**Key features:**
- Securely authenticate with Zerodha via browser flow.
- Retrieve your live portfolio holdings using the `get_holdings` MCP tool.
- Analyze portfolio risk and performance using Gemini or OpenAI (LLM).

---

## 🛠 Technologies Used

- **Google ADK (Agent Development Kit):** Multi-agent, tool-using workflow framework for LLMs and APIs.
- **Zerodha Kite MCP:** Secure SSE API server for accessing your Zerodha trading account.
- **Google Gemini / OpenAI GPT-4o:** LLM-driven analytics and portfolio recommendations.
- **python-dotenv:** Loads credentials and configuration from environment variables or `.env`.

---

## 🚦 How It Works

1. **Connect to MCP server:**  
   The agent connects to Zerodha’s MCP SSE endpoint.

2. **Login with Zerodha:**  
   The workflow launches a browser for Zerodha login and authorization (credentials handled only by Zerodha).

3. **Fetch holdings:**  
   Uses the `get_holdings` tool to retrieve your current portfolio holdings.

4. **LLM-powered analysis:**  
   The agent analyzes holdings for:
   - **Concentration risk**
   - **Best/worst performing stocks** and actionable recommendations.

---

## 💻 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/google-adk-zerodha.git
cd google-adk-zerodha
```

### 2. Install Dependencies

```bash
pip install google-adk python-dotenv
```

> Requires Python 3.9+.

### 3. Configure Environment Variables

Create a `.env` file in the project folder:

```
GOOGLE_API_KEY=your_google_gemini_api_key
OPENAI_API_KEY=your_openai_api_key        # (optional, for OpenAI)
ANTHROPIC_API_KEY=your_anthropic_api_key  # (optional, for Anthropic)
MCP_SSE_URL=https://mcp.kite.trade/sse    # (default, override if needed)
```

**Never commit `.env` to source control!**

---

## 🚀 Running the Script

```bash
python portfolio_analysis.py
```

- The script launches a browser for Zerodha login.
- After authentication, it fetches holdings and provides markdown portfolio analysis.
- Results are printed to your terminal.

---

## ⚠️ Notes

- **Manual Login:** Credentials are entered in your browser, never handled or stored by the script.
- **Session Expiry:** If the session expires, rerun the script and login again.
- **Data Privacy:** No personal or financial data is logged or stored.
- **LLM Usage:** Requires Gemini or OpenAI API key.
- **Dependencies:** Only uses open-source Python and Google ADK.

---

## 📝 Customizing

- To analyze other endpoints, update the toolset in `portfolio_analysis.py`.
- To switch LLMs, change the `model=` parameter in the agent.
- Add error handling or more analytics by editing the event processing logic.

---

## 📄 License

MIT

---

## 📚 References

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Zerodha Kite MCP](https://github.com/zerodha/kite-mcp-server)
- [Zerodha Kite Connect API](https://kite.trade/docs/connect/v3/)
- [Google Gemini API](https://ai.google.dev/)
- [OpenAI Platform](https://platform.openai.com/)

---

*For educational and personal use only. Not investment advice. Not affiliated with Zerodha or Google.*

---

**Filename:** `portfolio_analysis.py`  
**Folder:** `google-adk-zerodha`
