# Hermes Agent × NCHC GenAI Portal

> English version: [README.md](README.md)

Hermes Agent 是一個開源的 AI 助理，可以在終端機（terminal）裡直接跟它對話，也可以接到 Telegram、Discord、Slack 等通訊軟體上使用。這份 fork 已經內建好 NCHC GenAI Portal 的連線設定，安裝完成、填入 API key 之後就能直接開始使用。


## 快速開始

### 1. 下載這個專案

```bash
git clone https://github.com/princesswinnie1122/hermes-agent-nchc.git
cd hermes-agent-nchc
```

### 2. 填入你的 NCHC API key

```bash
cp .env.example .env
```

用文字編輯器打開 `.env`，找到最上面 `NCHC GenAI Portal` 那一段，把下面這行前面的 `#` 拿掉，並換成你自己的 key：

```
NCHC_API_KEY=你的-nchc-api-key
```

> 還沒有 API key？請洽詢你的 NCHC 帳號管理員或 GenAI Portal 平台申請。

### 3. 執行安裝腳本

```bash
./setup-hermes.sh
```

這個腳本會自動：
- 安裝 Hermes Agent 所需要的環境（不會動到你電腦上其他軟體）
- 把 NCHC 設定為預設的模型來源
- 把 `hermes` 指令加進你的終端機

因為 NCHC 已經預先設定好了，這個腳本裝完不會再問你要不要跑設定精靈（setup wizard）。

### 4. 開始對話

```bash
source ~/.bashrc   # 或 source ~/.zshrc，重新載入終端機設定
hermes
```

看到對話畫面就代表成功了！直接打字問它問題即可。

## 切換模型

在對話中輸入 `/model` 後面接模型名稱，可以隨時切換，不會中斷對話：

```
/model Llama-3.3-70B-Instruct
```

NCHC GenAI Portal 上其實有 50 幾個模型，但很多是語音辨識、嵌入向量這類不適合拿來「聊天」的模型。我們挑出了 8 個適合當對話助理用的,依照使用情境分類如下,不確定要選哪個的話,直接用預設的就好。

**寫程式：**

| 模型名稱 | 什麼時候用 |
| --- | --- |
| `Devstral-2-123B-Instruct-2512`（預設） | 寫程式、除錯、複雜任務的首選，支援 256K 超長上下文，可以一次丟整包程式碼進去 |
| `Devstral-Small-2507` | 同樣是寫程式用，體積較小、回應較快，簡單、快速的程式問題可以換這個 |

**日常聊天、寫作、翻譯、一般問答：**

| 模型名稱 | 什麼時候用 |
| --- | --- |
| `Llama-3.3-70B-Instruct` | 泛用型，日常對話、寫作、翻譯都適合，是最通用穩定的選擇 |
| `Llama-4-Maverick-17B-128E-Instruct-FP8` | 較新的泛用模型，日常對話、寫作皆可，可以跟 Llama-3.3 交叉比較看哪個回答你比較喜歡 |

**需要深入分析、複雜推理的問題：**

| 模型名稱 | 什麼時候用 |
| --- | --- |
| `Mistral-Large-3-675B-Instruct-2512` | 這幾個裡面規模最大的通用模型,適合需要仔細分析、長文件閱讀理解的任務 |
| `gpt-oss-120b` | OpenAI 開源模型，同樣適合需要多步驟推理的問題 |
| `NVIDIA-Nemotron-3-Super-120B-A12B` | NVIDIA 的模型，也是主打複雜推理任務 |

**想要速度快、簡單問題不想等：**

| 模型名稱 | 什麼時候用 |
| --- | --- |
| `Microsoft-Phi-4` | 體積小、回應快，適合快速、簡單的問題,不用大砲打小鳥 |

> 上面三個「複雜推理」模型能力上沒有嚴格排名——我們沒有針對這 3 個做過正式評測比較，先都列出來，你可以自己試試看哪個回答風格比較合你的任務。如果想用清單以外的模型（例如 Portal 上還有台灣在地化的 `Gemma-3-TAIDE-12b-Chat`、`TAIDE-LX-7B-Chat` 等中文語感較好的模型），一樣可以直接打 `/model <模型名稱>` 切換，不限於上面列的 8 個。

## 常見問題

- **裝好之後不知道有沒有成功？** 執行 `hermes doctor`，它會檢查設定並告訴你哪裡有問題。
- **想確認目前用的是哪個模型/供應商？** 執行 `hermes status`。
- **想換到別的通訊軟體（Telegram、Discord…）使用？** 執行 `hermes gateway`，照畫面指示設定。
- **`.env` 或 `config.yaml` 裡的 API key 絕對不要上傳到 GitHub** —— 這兩個檔案已經被 `.gitignore` 排除，正常使用不會不小心 commit 上去。

> ⚠️ **不要執行沒有帶參數的 `hermes setup`。** 它是給「完全沒設定過」的使用者用的通用精靈，第一個選項預設是「Quick Setup (Nous Portal)」——如果你按下 Enter 選了它，會直接把你已經設定好的 NCHC 換成 Nous Portal 的 OAuth 登入，等於重新設定一次。如果你想調整其他東西，請用比較精準的指令，例如 `hermes model`（換模型）、`hermes setup gateway`（設定通訊軟體）、`hermes setup tools`（設定工具）。

- **明明填了 `.env` 卻還是出現 401 / API key 錯誤？** Hermes 實際上是讀 `~/.hermes/.env` 這個檔案，不是這個 repo 資料夾裡的 `.env`——`setup-hermes.sh` 第一次執行時會自動把你的 key 同步過去，但如果你之後換了新的 key，記得重新跑一次 `./setup-hermes.sh`，或是直接編輯 `~/.hermes/.env`。也可以用下面這個獨立的小工具，不透過 hermes，直接測試 key 本身能不能用：
  ```bash
  python3 scripts/test_nchc_api.py
  ```

### 授權

本專案 fork 自 [Nous Research 的 Hermes Agent](https://github.com/NousResearch/hermes-agent)，以 MIT 授權條款釋出，詳見 [LICENSE](LICENSE)。

