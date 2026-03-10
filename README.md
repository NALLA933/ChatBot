# 👾 Senpai Bot

A fun, friendly Telegram chatbot powered by **Pyrogram**, **MongoDB Atlas**, and **Groq AI**.

## ✨ Features

- **🚀 /start System** — Welcome messages with media, inline keyboards, friend GC buttons
- **📢 Broadcast** — `/broadcast` (groups) and `/broadcast -user` (users + groups) with failed reports
- **🤖 AI Chat** — Groq-powered conversational AI with memory (Hinglish-friendly Senpai persona)
- **🎭 Sticker System** — Auto-saves user sticker packs, random sticker replies
- **📝 Auto Registration** — Silent user/group registration via MongoDB
- **🔤 SmallCaps** — Unicode small-caps text converter

## 📁 Structure

```
senpai_bot/
├── config.py              # All bot configuration
├── main.py                # Entry point
├── requirements.txt
├── sample.env
│
├── database/
│   ├── connection.py      # Motor async MongoDB
│   ├── users.py           # Users + Groups collections
│   └── chat_history.py    # AI chat memory
│
├── plugins/
│   ├── start.py           # /start handler (DM + Group)
│   ├── register.py        # Silent auto-registration
│   ├── broadcast.py       # /broadcast system
│   └── ai_chat.py         # AI chat + stickers + /reset
│
├── utils/
│   ├── keyboards.py       # Inline keyboards
│   ├── helpers.py         # Media detection & sending
│   ├── smallcaps.py       # SmallCaps converter
│   └── sticker_helper.py  # Sticker pack management
│
└── data/
    └── strings.py         # Broadcast string constants
```

## 🛠️ Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Edit `config.py`** with your:
   - `API_ID`, `API_HASH`, `BOT_TOKEN` (from [my.telegram.org](https://my.telegram.org))
   - `OWNER_ID` (your Telegram user ID)
   - `MONGO_URI` (MongoDB Atlas connection string)
   - `GROQ_API_KEY` (from [console.groq.com](https://console.groq.com))
   - `BOT_USERNAME` (without @)

3. **Run the bot:**
   ```bash
   python main.py
   ```

## 📋 Commands

| Command | Where | Description |
|---------|-------|-------------|
| `/start` | DM / Group | Welcome message with buttons |
| `/broadcast` | DM (Owner) | Broadcast to all groups |
| `/broadcast -user` | DM (Owner) | Broadcast to all users + groups |
| `/reset` | DM | Clear AI chat memory |
| `/loadstickers` | DM (Owner) | Load bot sticker pack |

## ⚙️ Requirements

- Python 3.10+
- MongoDB Atlas cluster
- Groq API key
- Telegram Bot Token + API credentials
