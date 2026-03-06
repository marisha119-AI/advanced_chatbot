import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_api_key():
    try:
        key = st.secrets["OPENROUTER_API_KEY"]
        if key: return key
    except: pass
    return os.getenv("OPENROUTER_API_KEY", "")

api_key = get_api_key()

st.set_page_config(
    page_title="ARIA · AI Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');

:root {
    --bg:      #0c0c0e;
    --surface: #111114;
    --border:  rgba(255,255,255,0.07);
    --accent:  #e8ff47;
    --muted:   #555560;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: var(--bg) !important;
    font-family: 'Outfit', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }

.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.013) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.013) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none; z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed; top: -180px; left: 50%;
    transform: translateX(-50%);
    width: 800px; height: 500px;
    background: radial-gradient(ellipse,
        rgba(232,255,71,0.04) 0%,
        rgba(71,217,255,0.025) 45%,
        transparent 70%);
    pointer-events: none; z-index: 0;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding: 26px 20px !important; }
section[data-testid="stSidebar"] * { color: #b0b0b8 !important; }

.s-logo { font-family:'Instrument Serif',serif; font-size:2rem; color:white!important; letter-spacing:-0.5px; margin-bottom:2px; }
.s-logo em { color:var(--accent)!important; font-style:italic; }
.s-tag { font-family:'Geist Mono',monospace; font-size:0.58rem; letter-spacing:0.2em; text-transform:uppercase; color:var(--muted)!important; margin-bottom:22px; }
.s-div { height:1px; background:var(--border); margin:16px 0; }
.s-lbl { font-family:'Geist Mono',monospace; font-size:0.57rem; letter-spacing:0.22em; text-transform:uppercase; color:#333340!important; margin-bottom:8px; }
.s-row { display:flex; justify-content:space-between; align-items:center; padding:7px 0; border-bottom:1px solid rgba(255,255,255,0.04); font-size:0.75rem; }
.s-k { color:#3a3a48!important; }
.s-v { color:#c8c8d0!important; font-family:'Geist Mono',monospace; font-size:0.7rem; }
.dot { display:inline-block; width:6px; height:6px; background:#22c55e; border-radius:50%; margin-right:5px; animation:blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }

/* WELCOME */
.welcome { text-align:center; padding:60px 20px 40px; position:relative; z-index:1; }
.w-eye { font-family:'Geist Mono',monospace; font-size:0.6rem; letter-spacing:0.3em; text-transform:uppercase; color:var(--muted); margin-bottom:18px; display:flex; align-items:center; justify-content:center; gap:14px; }
.w-eye::before,.w-eye::after { content:''; width:44px; height:1px; background:rgba(255,255,255,0.06); }
.w-title { font-family:'Instrument Serif',serif; font-size:4.2rem; color:white; letter-spacing:-2px; line-height:1; margin-bottom:14px; }
.w-title em { color:var(--accent); font-style:italic; }
.w-sub { font-size:0.9rem; color:var(--muted); font-weight:300; margin-bottom:44px; }

.cards { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; max-width:640px; margin:0 auto; }
.card { background:#111114; border:1px solid rgba(255,255,255,0.05); border-radius:14px; padding:16px 18px; text-align:left; transition:border-color 0.2s; }
.card:hover { border-color:rgba(232,255,71,0.18); }
.c-i { font-size:1.1rem; margin-bottom:8px; }
.c-t { font-size:0.81rem; font-weight:600; color:#c0c0c8; margin-bottom:3px; }
.c-d { font-size:0.72rem; color:#3a3a48; line-height:1.45; }

/* MESSAGES */
.chat-area { max-width:760px; margin:0 auto; padding:4px 20px 0; position:relative; z-index:1; }
.msg { margin:16px 0; animation:up 0.22s ease; }
@keyframes up { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)} }
.msg-top { display:flex; align-items:center; gap:9px; margin-bottom:8px; }
.av { width:28px; height:28px; border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:0.7rem; font-family:'Geist Mono',monospace; font-weight:600; flex-shrink:0; }
.av-u { background:#1b1b22; border:1px solid rgba(255,255,255,0.07); color:#b8b8c0!important; }
.av-a { background:rgba(232,255,71,0.1); border:1px solid rgba(232,255,71,0.22); color:var(--accent)!important; }
.m-name { font-family:'Geist Mono',monospace; font-size:0.58rem; letter-spacing:0.14em; text-transform:uppercase; color:#2e2e3c; }
.m-ts { font-family:'Geist Mono',monospace; font-size:0.54rem; color:#1e1e2a; margin-left:auto; }

.bub-u { background:#15151c; border:1px solid rgba(255,255,255,0.05); border-radius:4px 16px 16px 16px; padding:13px 17px; font-size:0.91rem; color:#d4d4dc; line-height:1.72; word-break:break-word; }
.bub-a { background:#0d0f14; border:1px solid rgba(232,255,71,0.06); border-left:2px solid var(--accent); border-radius:0 16px 16px 16px; padding:15px 19px; font-size:0.91rem; color:#ccccd4; line-height:1.82; word-break:break-word; }

/* CHAT INPUT — white bg, black text */
.stChatInput { position:relative; z-index:2; }
.stChatInput > div {
    background:#ffffff !important;
    border:2px solid #e0e0e0 !important;
    border-radius:16px !important;
    max-width:760px !important;
    margin:14px auto 0 !important;
}
.stChatInput > div:focus-within {
    border-color:#b8cc00 !important;
    box-shadow:0 0 0 3px rgba(184,204,0,0.12) !important;
}
.stChatInput textarea {
    color:#111111 !important;
    background:#ffffff !important;
    font-family:'Outfit',sans-serif !important;
    font-size:0.93rem !important;
    caret-color:#333 !important;
}
.stChatInput textarea::placeholder { color:#999 !important; }

/* MARKDOWN */
.stMarkdown p { color:#ccccd4!important; line-height:1.8!important; }
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color:#eeeef4!important; margin:14px 0 6px!important; }
.stMarkdown strong { color:#eeeef4!important; }
.stMarkdown a { color:var(--accent)!important; }
.stMarkdown ul,.stMarkdown ol { color:#c4c4cc!important; padding-left:20px!important; }
.stMarkdown li { margin:4px 0!important; }
.stMarkdown code { background:#1c1c2c!important; color:#a6e3a1!important; border-radius:5px!important; padding:2px 7px!important; font-family:'Geist Mono',monospace!important; font-size:0.84rem!important; }
.stMarkdown pre { background:#11111e!important; border:1px solid rgba(255,255,255,0.06)!important; border-radius:12px!important; padding:16px!important; overflow-x:auto!important; }
.stMarkdown pre code { color:#cdd6f4!important; background:transparent!important; padding:0!important; }

/* SELECTBOX */
section[data-testid="stSidebar"] div[data-baseweb="select"] { background:#17171d!important; border:1px solid rgba(255,255,255,0.07)!important; border-radius:10px!important; }
section[data-testid="stSidebar"] div[data-baseweb="select"] * { background:#17171d!important; color:#e0e0e8!important; }
div[data-baseweb="popover"],div[data-baseweb="menu"] { background:#17171d!important; border:1px solid rgba(255,255,255,0.09)!important; border-radius:12px!important; }
div[data-baseweb="menu"] li { color:#c4c4cc!important; background:#17171d!important; }
div[data-baseweb="menu"] li:hover { background:rgba(232,255,71,0.07)!important; color:var(--accent)!important; }
div[data-baseweb="menu"] li[aria-selected="true"] { background:rgba(232,255,71,0.1)!important; color:var(--accent)!important; }

/* BUTTON */
.stButton > button { background:rgba(232,255,71,0.06)!important; color:var(--accent)!important; border:1px solid rgba(232,255,71,0.16)!important; border-radius:10px!important; font-family:'Geist Mono',monospace!important; font-size:0.72rem!important; letter-spacing:0.08em!important; transition:all 0.2s!important; }
.stButton > button:hover { background:rgba(232,255,71,0.12)!important; border-color:rgba(232,255,71,0.32)!important; }

/* FOOTER */
.foot { text-align:center; padding:20px; font-family:'Geist Mono',monospace; font-size:0.54rem; letter-spacing:0.16em; text-transform:uppercase; color:#1c1c24; position:relative; z-index:1; }
.foot span { color:rgba(232,255,71,0.35); }
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "messages"  not in st.session_state: st.session_state.messages  = []
if "msg_count" not in st.session_state: st.session_state.msg_count = 0

MODELS = {
    "openrouter/auto":                         "Auto · Best Available",
    "z-ai/glm-4.5-air:free":                  "GLM 4.5 Air · Free",
    "deepseek/deepseek-r1:free":               "DeepSeek R1 · Free",
    "deepseek/deepseek-chat-v3-0324:free":    "DeepSeek V3 · Free",
    "google/gemini-2.0-flash-exp:free":        "Gemini 2.0 Flash · Free",
    "meta-llama/llama-3.3-70b-instruct:free":  "Llama 3.3 70B · Free",
}

SYSTEM = """You are ARIA (Advanced Reasoning Intelligence Assistant).
- Direct, precise, helpful. No filler phrases.
- Use markdown: headers, bullets, code blocks when useful.
- Always specify language in code blocks.
- Give complete, accurate answers."""

# SIDEBAR
with st.sidebar:
    st.markdown('<div class="s-logo">ARI<em>A</em></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-tag">Advanced Reasoning Intelligence · 2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="s-div"></div>', unsafe_allow_html=True)

    st.markdown('<div class="s-lbl">Model</div>', unsafe_allow_html=True)
    model = st.selectbox("", list(MODELS.keys()),
        format_func=lambda x: MODELS[x], label_visibility="collapsed")

    st.markdown('<div class="s-div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-lbl">Session</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="s-row"><span class="s-k">Status</span><span class="s-v"><span class="dot"></span>Online</span></div>
    <div class="s-row"><span class="s-k">Messages</span><span class="s-v">{st.session_state.msg_count}</span></div>
    <div class="s-row"><span class="s-k">Speed</span><span class="s-v">⚡ Streaming</span></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="s-div"></div>', unsafe_allow_html=True)
    if st.button("🗑  Clear Chat", use_container_width=True):
        st.session_state.messages  = []
        st.session_state.msg_count = 0
        st.rerun()

    st.markdown('<div class="s-div"></div>', unsafe_allow_html=True)
    st.markdown("""<div style="font-size:0.74rem;color:#2e2e3a!important;line-height:1.9;">
        Built by <span style="color:#e8ff47!important;font-weight:600;">Marisha Dwivedi</span><br>
        AI Engineer · 2026<br>
        <a href="https://github.com/marisha119-AI" style="color:#383848!important;text-decoration:none;">GitHub ↗</a>
    </div>""", unsafe_allow_html=True)

# NO KEY GUARD
if not api_key:
    st.markdown("""
    <div style="background:#170808;border:1px solid #7f1d1d;border-radius:16px;
                padding:28px;text-align:center;max-width:460px;margin:80px auto;position:relative;z-index:1;">
        <div style="font-size:1.6rem;">⚠️</div>
        <div style="color:#fca5a5;font-weight:600;margin-top:10px;">API Key Missing</div>
        <div style="color:#555;font-size:0.82rem;margin-top:8px;">
            Add <code style="color:#f87171;background:#2a0808;padding:2px 6px;border-radius:4px;">OPENROUTER_API_KEY</code> to your .env file
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

# WELCOME SCREEN
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <div class="w-eye">AI Assistant · OpenRouter · 2026</div>
        <div class="w-title">Hello, I'm <em>ARIA</em></div>
        <div class="w-sub">Ask me anything — code, analysis, writing, math, research</div>
        <div class="cards">
            <div class="card"><div class="c-i">⚡</div><div class="c-t">Write Code</div><div class="c-d">Python, JS, SQL, APIs, scripts</div></div>
            <div class="card"><div class="c-i">🔬</div><div class="c-t">Analyze & Research</div><div class="c-d">Deep dives, comparisons, summaries</div></div>
            <div class="card"><div class="c-i">✍️</div><div class="c-t">Write & Edit</div><div class="c-d">Emails, reports, posts, proposals</div></div>
            <div class="card"><div class="c-i">🧮</div><div class="c-t">Math & Logic</div><div class="c-d">Step-by-step reasoning, problem solving</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

# CHAT HISTORY
ts = datetime.now().strftime("%H:%M")
st.markdown('<div class="chat-area">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg">
            <div class="msg-top">
                <div class="av av-u">You</div>
                <div class="m-name">User</div>
                <div class="m-ts">{ts}</div>
            </div>
            <div class="bub-u">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg">
            <div class="msg-top">
                <div class="av av-a">✦</div>
                <div class="m-name">ARIA</div>
                <div class="m-ts">{ts}</div>
            </div>
            <div class="bub-a">""", unsafe_allow_html=True)
        st.markdown(msg["content"])
        st.markdown("</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# CHAT INPUT
if prompt := st.chat_input("Message ARIA..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.msg_count += 1

    st.markdown(f"""
    <div class="chat-area"><div class="msg">
        <div class="msg-top"><div class="av av-u">You</div><div class="m-name">User</div></div>
        <div class="bub-u">{prompt}</div>
    </div></div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-area"><div class="msg">
        <div class="msg-top"><div class="av av-a">✦</div><div class="m-name">ARIA</div></div>
    </div></div>""", unsafe_allow_html=True)

    api_msgs = [{"role": "system", "content": SYSTEM}]
    api_msgs += [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=api_msgs,
            temperature=0.7,
            max_tokens=2000,
            stream=True,
            timeout=30
        )

        full = ""
        slot = st.empty()

        for chunk in stream:
            try:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    full += delta.content
                    slot.markdown(
                        f'<div class="chat-area"><div class="bub-a">{full}▋</div></div>',
                        unsafe_allow_html=True
                    )
            except (IndexError, AttributeError):
                continue

        slot.empty()
        st.session_state.messages.append({"role": "assistant", "content": full})
        st.rerun()

    except Exception as e:
        err = str(e)
        if "429" in err: reply = "⚠️ Rate-limited — switch model in sidebar."
        elif "401" in err: reply = "⚠️ Invalid API key — check your .env file."
        elif "404" in err: reply = "⚠️ Model not found — switch to Auto."
        else: reply = f"⚠️ {err}"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# FOOTER
st.markdown('<div class="foot">ARIA · Built by <span>Marisha Dwivedi</span> · 2026</div>', unsafe_allow_html=True)