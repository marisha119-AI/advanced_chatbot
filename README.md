# ARIA · AI Assistant

> A sleek, professional AI chatbot built with Streamlit and OpenRouter — featuring real-time streaming, multi-model support, and a beautiful dark UI.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![OpenRouter](https://img.shields.io/badge/OpenRouter-API-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## What is ARIA?

**ARIA** (Advanced Reasoning Intelligence Assistant) is a full-featured AI chatbot that connects to multiple state-of-the-art language models through the OpenRouter API. It streams responses in real time, maintains conversation history, and presents everything in a polished dark-themed interface.

Built as part of an AI Engineer portfolio to demonstrate practical skills in LLM integration, prompt engineering, streaming APIs, and production-ready UI design.

---

## Features

- **⚡ Real-time Streaming** — Responses appear word-by-word instantly, just like ChatGPT
- **🤖 Multi-Model Support** — Switch between 6 free LLMs from the sidebar at any time
- **💬 Conversation Memory** — Full chat history maintained throughout the session
- **🎨 Professional Dark UI** — Custom CSS with animated background, styled message bubbles, and branded design
- **🔒 Secure API Handling** — API key loaded from `.env` file or Streamlit Secrets (never exposed in code)
- **📱 Responsive Layout** — Works on desktop and tablet
- **🧹 Clear Chat** — Reset conversation with one click

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit + Custom CSS |
| LLM API | OpenRouter (OpenAI-compatible) |
| Streaming | OpenAI Python SDK (`stream=True`) |
| Fonts | Instrument Serif, Geist Mono, Outfit |
| Config | python-dotenv |

---

## Models Available

| Model | Provider | Notes |
|-------|----------|-------|
| Auto · Best Available | OpenRouter | Automatically picks best model |
| GLM 4.5 Air | ZhipuAI | Fast, free |
| DeepSeek R1 | DeepSeek | Strong reasoning, free |
| DeepSeek V3 | DeepSeek | Latest version, free |
| Gemini 2.0 Flash | Google | Fast multimodal, free |
| Llama 3.3 70B | Meta | Powerful open-source, free |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/marisha119-AI/aria-chatbot.git
cd aria-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the project root:

```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Get your free API key at [openrouter.ai](https://openrouter.ai) → Sign in → API Keys → Create Key.

### 4. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Project Structure

```
aria-chatbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # API key (not committed to Git)
├── .gitignore          # Excludes .env and cache files
└── README.md           # This file
```

---

## requirements.txt

```
streamlit
openai
python-dotenv
```

---

## Deployment on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select this repo → set `app.py` as the main file
4. Go to **Settings → Secrets** and add:

```toml
OPENROUTER_API_KEY = "sk-or-v1-your-key-here"
```

5. Click **Deploy** — your app will be live in under a minute!

---

---

## About the Developer

**Marisha Dwivedi** — AI Engineer building practical AI products and sharing the journey publicly.

- 🐙 GitHub: [@marisha119-AI](https://github.com/marisha119-AI)
- 💼 LinkedIn: [Add your LinkedIn URL here]
- 🚀 Portfolio: [Add your portfolio URL here]

---

## License

MIT License — free to use, modify, and distribute.

---

_Built with ❤️ as part of an AI Engineer portfolio · 2026_
