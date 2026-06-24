# 👾 Senpai Bot

A fun, friendly Telegram chatbot powered by **Pyrogram**, **MongoDB Atlas**, and **Groq AI**.

## ✨ Features

- **🚀 /start System** — Welcome messages with media, inline keyboards, and friend GC buttons
- **📢 Broadcast** — `/broadcast` (groups) and `/broadcast -user` (users + groups) with failure reports
- **🤖 AI Chat** — Groq-powered AI conversations with memory and a Hinglish-style Senpai persona
- **🎭 Sticker System** — Auto-save user sticker packs and reply with stickers
- **📝 Auto Registration** — Automatically register users/groups in MongoDB
- **🔤 SmallCaps** — Unicode small-caps text converter for bot replies

## 📁 Project Structure

```
ChatBot/
├── config.py              # All bot configuration
├── main.py                # Entry point
├── requirements.txt
├── sample.env
│
├── database/
│   ├── connection.py      # Motor async MongoDB connection
│   ├── users.py           # User and group storage
│   └── chat_history.py    # AI conversation memory
│
├── plugins/
│   ├── start.py           # /start commands for private/group chats
│   ├── register.py        # Silent auto-registration
│   ├── broadcast.py       # Owner broadcast utility
│   └── ai_chat.py         # AI chat logic, stickers, reset
│
├── utils/
│   ├── keyboards.py       # Inline keyboard builders
│   ├── helpers.py         # Media and helper utilities
│   ├── smallcaps.py       # SmallCaps converter
│   └── sticker_helper.py  # Sticker pack persistence
│
└── data/
    └── strings.py         # String constants used by plugins
```

## 🛠️ Installation

This bot is optimized for **Python 3.14**.

### A. VPS / Ubuntu Installation

1. Update packages:
   ```bash
   sudo apt update
   ```

2. Install Python 3.14 and venv support:
   ```bash
   sudo apt install python3.14 python3.14-venv python3.14-distutils -y
   ```

3. Create a virtual environment:
   ```bash
   python3.14 -m venv venv
   ```

4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

6. Copy the sample environment file:
   ```bash
   cp sample.env .env
   ```

7. Edit `.env` or `config.py` with your credentials:
   - `API_ID`, `API_HASH`, `BOT_TOKEN`
   - `OWNER_ID`
   - `MONGO_URI`
   - `GROQ_API_KEY`
   - `BOT_USERNAME`

8. Run the bot:
   ```bash
   python3.14 main.py
   ```

### B. Alternative `pyenv` Installation

If Python 3.14 is not available via your package manager:

```bash
curl https://pyenv.run | bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
pyenv install 3.14.0
pyenv local 3.14.0
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### C. Notes for VPS

- Use a virtual environment to isolate dependencies.
- Ensure your VPS can reach MongoDB Atlas and Telegram servers.
- Allow outbound access to Groq and Telegram APIs if a firewall is active.

## 📋 Commands

| Command | Where | Description |
|---------|-------|-------------|
| `/start` | DM / Group | Send welcome message with buttons |
| `/broadcast` | DM (Owner) | Broadcast to all registered groups |
| `/broadcast -user` | DM (Owner) | Broadcast to all registered users + groups |
| `/reset` | DM | Clear AI chat history |
| `/loadstickers` | DM (Owner) | Load the bot sticker pack |

## ⚙️ Requirements

- Python 3.14
- MongoDB Atlas cluster
- Groq API key
- Telegram Bot Token + API credentials
- `requirements.txt` dependencies installed

## 📌 Tips

- Keep your `.env` file secret and never share it.
- For long-running bot deployment, use a process manager such as `systemd`, `pm2`, or `supervisord`.
- If the bot does not start, check logs for missing environment variables or connection issues.
