# 🧠 Java Migration Plan with CrewAI + Gemini

This project uses [CrewAI](https://docs.crewai.com/) and Google's [Gemini Model](https://aistudio.google.com//) via **Google AI Studio** to automate Java code modernization.

---

## 🚀 What It Does

🔎 **Analyzes legacy Java code**  
🧠 **Uses Gemini LLM** to identify:
- Legacy/deprecated syntax
- Compatibility issues with Java 17+
- Refactoring suggestions using modern Java features (lambdas, streams, switch expressions, etc.)

📝 **Outputs a full migration report** in markdown format.

---

## 🛠️ Technologies Used

- [CrewAI](https://github.com/joaomdmoura/crewai)
- Google AI Studio (Gemini 2.0 via API Key)
- `google-generativeai` SDK (indirectly used through `llm="gemini/..."`)
- Python 3.10+
- `.env` based secure config

---

## 📂 Folder Structure

```
├── legacy_app/
│   └── Main.java                 # Sample Java code to analyze
├── migration_plan.py            # CrewAI workflow
├── .env                         # API key for Gemini
├── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/java-migration-crewai.git
cd java-migration-crewai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Dependencies**
> - `crewai`
> - `crewai-tools`
> - `python-dotenv`

> Optional (in case you extend with direct Gemini SDK):
> - `google-generativeai`

### 3. Add Your Gemini API Key

Create a `.env` file:

```bash
touch .env
```

Inside `.env`:

```env
GEMINI_API_KEY=your-google-ai-studio-api-key
```

### 4. Add Your Java Code

Update or replace the file at:

```bash
legacy_app/Main.java
```

With any Java code you'd like to modernize.

---

## ▶️ Run the Crew

```bash
python migration_plan.py
```

---

## ✅ Sample Output

```
📋 Final Migration Report:

### Detected Legacy Patterns
- Usage of `Vector` instead of `ArrayList`
- Manual thread creation with anonymous `Runnable`

### Compatibility Issues with Java 17
- `System.gc()` usage discouraged
- Raw types detected

### Refactor Suggestions
- Replace anonymous `Runnable` with lambda
- Use `java.time.LocalDate` instead of `new Date()`
```

---

## 🤖 LLM Configuration (under the hood)

- The agents use:
  ```python
  llm="gemini/gemini-2.0-flash"
  ```
- Gemini is accessed **via API key**, not Vertex AI.
- Credentials are controlled via `.env`.

---

## 📌 Notes

- You **do not** need Google Cloud (Vertex AI) setup.
- You **must** use [Google AI Studio](https://makersuite.google.com/app/apikey) API key.
- You can configure any LLM supported by CrewAI like OpenAI etc .

---

## 📬 Contributions

PRs welcome! Especially for:
- Gemini model switching
- VS Code plugin integration
- GitHub Copilot alternative tooling

---

## 📄 License

MIT License
