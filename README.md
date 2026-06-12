# ROD Skill — Ratchet-Oriented Development

ROD（Ratchet-Oriented Development）是一個可整合到 AI Agent / Skill / Manifest 系統中的開發技能，用來協助新專案與既有專案用「可驗證、可回滾、可逐步提升」的方式進行軟體修改。

核心精神是：**AI 可以提出修改，但 fitness checks 必須證明修改有效，policy 必須允許，release 必須可回滾，baseline 只能往前推進。**

這個 repo 將 ROD Skill 包裝成可下載、可驗證、可整合的開源專案，包含：

- `SKILL.md`：完整技能說明與操作規則。
- `skill.json`：標準化 Manifest，供 Agent 平台或整合器讀取。
- `src/rod_skill/`：Manifest 載入、環境變數替換與基本驗證工具。
- `tests/`：針對 Manifest 與環境變數替換的測試。
- `config/`：預設設定範例。

## 核心功能

- 協助 AI Agent 區分 **Stable Core** 與 **Evolvable Surfaces**。
- 將有意義的改動轉換成小型、可觀察、可測試、可回滾的 patch。
- 對高風險區域採用 Strict Mode，例如 auth、permission、secrets、資料刪除、migration、release gate。
- 要求 prompt、workflow、RAG/KAG、policy、config、AI 輸出等行為改動具備 fitness checks。
- 支援 bug fix 轉換為 regression test 的工作模式。
- 提供 Manifest 驗證 CLI，方便整合前先檢查結構是否完整。

## 專案目錄結構

```text
rod-skill/
├── .github/
│   └── workflows/
│       └── ci.yml
├── config/
│   └── rod.defaults.json
├── docs/
│   └── integration.md
├── src/
│   └── rod_skill/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       └── manifest.py
├── tests/
│   ├── test_env_substitution.py
│   └── test_manifest.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── SKILL.md
├── pyproject.toml
└── skill.json
```

## 安裝與設定

### 1. 複製專案

```bash
git clone https://github.com/MarkTaylorTsai/rod-skill.git
cd rod-skill
```

### 2. 建立 Python 虛擬環境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安裝套件

一般使用：

```bash
pip install -e .
```

開發與測試：

```bash
pip install -e '.[dev]'
pytest -q
```

### 4. 驗證 Manifest

```bash
rod-skill validate skill.json
```

或：

```bash
python -m rod_skill.cli validate skill.json
```

## 安全提示：環境變數與敏感憑證

請不要把 API Key、Token、私鑰、帳密、production endpoint、內部路徑或任何敏感資訊寫死在 `skill.json`、`SKILL.md`、程式碼或 README 中。

建議做法：

1. 將敏感資訊放在本機 `.env` 或部署平台的 Secrets / Environment Variables。
2. 將 `.env` 加入 `.gitignore`，不要提交到 Git。
3. 專案中只提交 `.env.example`，用來提示需要哪些變數，但不要填真實值。
4. 在 Manifest 或外部 config 中使用 `${ENV_VAR}` 或 `${ENV_VAR:-default}` 形式，讓整合器於執行時替換。

範例：

```bash
cp .env.example .env
# 編輯 .env，但不要提交它
```

Linux / macOS 可用：

```bash
set -a
source .env
set +a
```

本專案目前不需要任何 API Key。若你在自己的 Agent 平台中加入外部 API、模型供應商或私有資料庫，請一律使用環境變數載入，不要 hardcode。

## 使用範例

### 範例一：要求 Agent 修改一段會影響行為的程式

**Input**

```text
請修正登入流程中偶爾允許未驗證使用者進入 dashboard 的問題。
```

**ROD Skill 期望 Output 摘要**

```text
ROD Summary:
- Changed: 修正 dashboard route 的驗證條件，未驗證使用者會被導向登入頁。
- Surface: permission / code
- Risk: high
- Fitness: 新增 allow/deny tests，確認已驗證使用者可進入、未驗證使用者不可進入。
- Rollback: revert 該 route guard patch 與新增測試。
- Remaining gaps: 尚未加入 audit event，可於下一個 patch 補上。
```

### 範例二：要求 Agent 調整 RAG 檢索設定

**Input**

```text
把法律問答的 top_k 從 5 調到 10，看看回答是否更完整。
```

**ROD Skill 期望 Output 摘要**

```text
ROD Summary:
- Changed: 將 rag_config.legal_qa.top_k 由 5 調整為 10。
- Surface: rag_config
- Risk: medium
- Fitness: 執行 retrieval eval，檢查 Recall@K、citation support、latency 與 unsupported claim rate。
- Rollback: 將 top_k 還原為 5。
- Remaining gaps: 需要累積更多 jurisdiction-specific golden cases。
```

### 範例三：驗證 skill.json 並輸出解析後 Manifest

**Input**

```bash
rod-skill render skill.json
```

**Output**

```json
{
  "id": "rod",
  "name": "ROD",
  "version": "0.1.0",
  "entrypoint": {
    "type": "markdown",
    "path": "SKILL.md"
  }
}
```

實際輸出會包含完整 Manifest 欄位；若 Manifest 中含有 `${ROD_SKILL_MODE:-standard}` 這類設定，工具會使用目前環境變數或預設值解析。

## 整合方式

1. 將 `skill.json` 與 `SKILL.md` 複製到你的 Agent 平台指定的 skills 目錄。
2. 讓 Agent runtime 讀取 `skill.json` 的 `entrypoint.path`。
3. 將 `SKILL.md` 的內容注入為系統技能、開發流程或工具使用規範。
4. 在整合層保留環境變數替換，不要在 Manifest 中寫入密鑰。

更多細節請見 [`docs/integration.md`](docs/integration.md)。

## 開發

執行測試：

```bash
pytest -q
```

執行 Manifest 驗證：

```bash
rod-skill validate skill.json
```

## License

MIT License. See [`LICENSE`](LICENSE).
