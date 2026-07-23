# Hermes Agent × NCHC GenAI Portal

> 繁體中文版：[README.zh-TW.md](README.zh-TW.md)

Hermes Agent is an open-source AI assistant you can chat with directly in your terminal, or connect to Telegram, Discord, Slack, and other messaging platforms. This fork comes pre-configured to talk to **NCHC's GenAI Portal** — install it, add your API key, and you're ready to go.

## Quick Start

**1. Clone this repo**

```bash
git clone https://github.com/princesswinnie1122/hermes-agent-nchc.git
cd hermes-agent-nchc
```

**2. Add your NCHC API key**

```bash
cp .env.example .env
```

Open `.env` in a text editor, find the `NCHC GenAI Portal` section near the top, uncomment the line below, and paste in your own key:

```
NCHC_API_KEY=your-nchc-api-key-here
```

> Don't have a key yet? Ask your NCHC account administrator, or apply through the GenAI Portal.

**3. Run the setup script**

```bash
./setup-hermes.sh
```

This installs everything Hermes needs (isolated to its own environment — it won't touch anything else on your machine), sets NCHC as the default model provider, and adds the `hermes` command to your terminal.

Since NCHC is already configured, this script won't ask you to run the setup wizard afterward.

**4. Start chatting**

```bash
source ~/.bashrc   # or ~/.zshrc — reload your shell
hermes
```

You should land in a chat prompt — just type your question.

### Switching models

Type `/model` followed by a model name at any point in the conversation — it switches instantly without losing your session:

```
/model Llama-3.3-70B-Instruct
```

NCHC's Portal actually hosts 50+ models, but most are speech-recognition, embedding, or reranker models that aren't meant for chat. We've picked out 8 that work well as a chat assistant, grouped by what they're good at. If you're not sure, just stick with the default.

**Coding:**

| Model | When to use it |
| --- | --- |
| `Devstral-2-123B-Instruct-2512` (default) | First choice for coding, debugging, and complex tasks — 256K context, so you can paste in a whole codebase |
| `Devstral-Small-2507` | Also for coding, smaller and faster — switch here for quick, simple coding questions |

**Everyday chat, writing, translation, general Q&A:**

| Model | When to use it |
| --- | --- |
| `Llama-3.3-70B-Instruct` | General-purpose — good for everyday conversation, writing, and translation; the most broadly reliable pick |
| `Llama-4-Maverick-17B-128E-Instruct-FP8` | A newer general-purpose model, also good for chat and writing — try it alongside Llama-3.3 and see which style you prefer |

**Deeper analysis / complex reasoning:**

| Model | When to use it |
| --- | --- |
| `Mistral-Large-3-675B-Instruct-2512` | The largest general model in this list — good for careful analysis and long-document comprehension |
| `gpt-oss-120b` | OpenAI's open-weight model, also geared toward multi-step reasoning |
| `NVIDIA-Nemotron-3-Super-120B-A12B` | NVIDIA's model, also positioned for complex reasoning tasks |

**Fast, for simple questions you don't want to wait on:**

| Model | When to use it |
| --- | --- |
| `Microsoft-Phi-4` | Small and fast — good for quick, simple questions where you don't need the bigger models |

> The three "complex reasoning" models above aren't ranked against each other — we haven't run a formal benchmark comparing them, so they're just listed together; try them and see which one's style fits your task. You're not limited to these 8, either — Portal also hosts Taiwan-localized models like `Gemma-3-TAIDE-12b-Chat` and `TAIDE-LX-7B-Chat` with a better feel for Chinese, and any of them work with `/model <model-name>`.

### Troubleshooting

- **Not sure the install worked?** Run `hermes doctor` — it checks your setup and tells you what's wrong.
- **Want to see which model/provider is active?** Run `hermes status`.
- **Want to use it from Telegram, Discord, etc.?** Run `hermes gateway` and follow the prompts.
- **Never commit a filled-in `.env` or `config.yaml`** — both are already excluded via `.gitignore`, so normal use won't accidentally leak your key.

> ⚠️ **Don't run the bare `hermes setup` command.** It's the generic wizard for a completely unconfigured install, and its first option — selected by default if you just press Enter — is "Quick Setup (Nous Portal)", which will silently replace your NCHC setup with a Nous Portal OAuth login. If you want to change something specific, use a narrower command instead: `hermes model` (switch model), `hermes setup gateway` (messaging platforms), or `hermes setup tools` (tools).

- **Getting a 401 / "API key" error even though you filled in `.env`?** Hermes actually reads API keys from `~/.hermes/.env`, not this repo's own `.env` — `setup-hermes.sh` copies your key over automatically the first time it runs, but if you change the key later, either re-run `./setup-hermes.sh` or edit `~/.hermes/.env` directly. You can sanity-check the key itself, independent of Hermes, with:
  ```bash
  python3 scripts/test_nchc_api.py
  ```

### License

This is a fork of [Nous Research's Hermes Agent](https://github.com/NousResearch/hermes-agent), released under the MIT License — see [LICENSE](LICENSE).
