# Boundless AI

A Python terminal chatbot powered by Groq (Llama 3.1 8B). Features layered memory, multi-mode reasoning (Logic / Dynamic / Architect Fusion), and an admin panel.

## How to run

Start the **"Start application"** workflow. The app runs in the console.

- **Login:** enter username/password at the prompt (admin: `hamed` / `5115902`, or press Enter for guest mode)
- **API key:** automatically read from the `GROQ_API_KEY` secret — no need to type it each time
- **Exit:** type `exit` or `خروج`
- **Admin menu:** type `menu` when logged in as admin

## Stack

- Python 3
- Groq API (llama-3.1-8b-instant) via `groq_connector.py`
- Local memory, reasoning, and orchestration modules in `core/` and `memory/`

## Secrets required

| Secret | Description |
|--------|-------------|
| `GROQ_API_KEY` | Your Groq API key (get one free at https://console.groq.com) |

## User preferences

- Keep the existing project structure and Python stack
