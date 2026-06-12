# ROD Skills — Ratchet-Oriented Development

[English](README.md)

ROD（Ratchet-Oriented Development）協助 AI Agent 以可觀察、可測試、可回滾、可持續改進的方式修改軟體。
本 repo 現在提供兩個 first-class skills：一個用於架構設計，一個用於有明確目標的修復或優化。

核心精神是：**AI 可以提出修改，但 fitness checks 必須證明修改有效，policy 必須允許，release 必須可回滾，baseline 只能往前推進。**

## 包含的 Skills

本 repo 包含兩個相關的 ROD skills：

1. **ROD Architecture**
   用於建立新系統或進行結構性修改，協助 Agent 及早設計 Stable Core 邊界、Evolvable Surfaces、
   fitness checks、observability、rollback paths 與 promotion gates。

2. **ROD Goal Loop**
   用於使用者提出修復、優化、品質改善、效能改善或「做到測試通過」這類目標時。它會建立
   Goal Contract，並透過 Observe、Diagnose、Plan、Patch、Verify、Compare、Decide 循環，
   直到目標完成或遇到停止條件。

根目錄的 `SKILL.md` 與 `skill.json` 保留為 ROD Architecture 的向後相容預設入口。

## 核心功能

- 加入 Ratchet-Oriented Architecture 指引，協助新系統一開始就區分受保護的 Stable Core 與可版本化的
  Evolvable Surfaces。
- 加入 Goal Contract loop，用於可衡量的修復、優化與驗證任務。
- 協助 AI Agent 區分 Stable Core 與 Evolvable Surfaces。
- 將有意義的改動轉換成小型、可觀察、可測試、可回滾的 patch。
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
│   ├── integration.md
│   └── integration.zh-TW.md
├── skills/
│   ├── rod-architecture/
│   │   ├── SKILL.md
│   │   └── skill.json
│   └── rod-goal-loop/
│       ├── SKILL.md
│       └── skill.json
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
├── README.zh-TW.md
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

### 4. 驗證 Manifests

```bash
rod-skill validate skill.json
rod-skill validate skills/rod-architecture/skill.json
rod-skill validate skills/rod-goal-loop/skill.json
```

或：

```bash
python -m rod_skill.cli validate skill.json
python -m rod_skill.cli validate skills/rod-architecture/skill.json
python -m rod_skill.cli validate skills/rod-goal-loop/skill.json
```

## 安全提示：環境變數與敏感憑證

請不要把 API Key、Token、私鑰、帳密、production endpoint、內部路徑或任何敏感資訊寫死在
`skill.json`、`SKILL.md`、程式碼或 README 中。

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

本專案目前不需要任何 API Key。若你在自己的 Agent 平台中加入外部 API、模型供應商或私有資料庫，
請一律使用環境變數或 secret manager 載入，不要 hardcode。

## 使用範例

### 範例一：用 ROD Architecture 做結構設計

**Input**

```text
設計一個新的 AI support system，讓 prompts、retrieval settings 與 workflow rules 都能安全演進。
```

**預期 ROD Architecture Summary**

```text
ROD Architecture Summary:
- Changed: Proposed initial ROD-friendly project structure and registries.
- Stable Core protected: Auth, tenant boundaries, secrets, audit logs, and promotion paths.
- Evolvable Surfaces: Prompts, retrieval config, workflow rules, evals, and feature flags.
- Fitness: Unit tests, retrieval evals, workflow scenario tests, and citation checks.
- Observability: Trace IDs, structured workflow events, retrieval metrics, and eval reports.
- Rollback: Versioned configs and prompt/workflow registry rollback.
- Remaining gaps: Production release approval policy still needs owner review.
```

### 範例二：用 ROD Architecture 設計 RAG 配置

**Input**

```text
規劃 legal QA 的 top_k、reranking 與 citation policy 要如何配置化並可測試。
```

**預期 ROD Architecture Summary**

```text
ROD Architecture Summary:
- Changed: Designed retrieval settings as versioned Evolvable Surfaces.
- Stable Core protected: Jurisdiction filters, citation policy gates, and audit logs.
- Evolvable Surfaces: top_k, reranker model, rerank_top_n, freshness boost, and authority boost.
- Fitness: Recall@K, citation support, jurisdiction match, latency, and unsupported claim rate.
- Observability: retrieval_performed, citation_gate_failed, and eval_case_created events.
- Rollback: Restore previous retrieval config version.
- Remaining gaps: More jurisdiction-specific golden cases are needed.
```

### 範例三：用 ROD Goal Loop 修復測試

**Input**

```text
Fix the failing test suite and keep iterating until tests pass or you find a blocker.
```

**預期 ROD Goal Loop Summary**

```text
ROD Goal Loop Summary:
- Goal: Test suite passes without weakening tests.
- Final decision: complete
- Changed:
- Surface:
- Risk:
- Iterations:
- Verification:
- Completion evidence:
- Rollback:
- Remaining gaps:
```

### 範例四：輸出解析後 Manifest

**Input**

```bash
rod-skill render skills/rod-architecture/skill.json
```

**Output**

```json
{
  "id": "rod-architecture",
  "name": "ROD Architecture",
  "version": "0.2.0",
  "entrypoint": {
    "type": "markdown",
    "path": "skills/rod-architecture/SKILL.md"
  }
}
```

實際輸出會包含完整 Manifest 欄位；若 Manifest 中含有 `${ROD_SKILL_MODE:-standard}` 這類設定，
工具會使用目前環境變數或預設值解析。

## 整合方式

依任務選擇 manifest：

- 使用 root `skill.json` 取得向後相容的 ROD Architecture 行為。
- 使用 `skills/rod-architecture/skill.json` 處理新系統、架構設計、結構性修改與重構規劃。
- 使用 `skills/rod-goal-loop/skill.json` 處理可衡量的修復、優化、品質、效能、prompt、RAG/KAG、workflow 或測試修復目標。

請在整合層保留環境變數替換，不要在任何 manifest 中寫入密鑰。

更多細節請見 [`docs/integration.md`](docs/integration.md)。

## 開發

執行測試：

```bash
pytest -q
```

驗證 manifests：

```bash
rod-skill validate skill.json
rod-skill validate skills/rod-architecture/skill.json
rod-skill validate skills/rod-goal-loop/skill.json
```

## License

MIT License. See [`LICENSE`](LICENSE).
