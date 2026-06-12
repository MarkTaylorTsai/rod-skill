# ROD Skills 整合指南

[English](integration.md)

本文件說明如何將 ROD skills 整合到支援 Manifest / Skill 載入的 AI Agent runtime。

## Skills 與入口

本 repo 包含三個 manifest 入口：

- `skill.json`：ROD Architecture 的向後相容預設入口。
- `skills/rod-architecture/skill.json`：first-class ROD Architecture skill。
- `skills/rod-goal-loop/skill.json`：first-class ROD Goal Loop skill。

root alias 的目的，是讓舊整合只讀取 `skill.json` 時仍然取得 architecture/development guidance。
它不是第三個不同概念的 skill。

## Skill 選擇規則

使用 ROD Architecture 的情境：

- 建立新系統
- 進行結構性修改
- 設計 evolvable surfaces
- 定義 Stable Core 邊界
- 規劃 prompts、workflows、RAG/KAG、policies 或 release gates

使用 ROD Goal Loop 的情境：

- 修復 bugs
- 讓失敗測試通過
- 優化效能或品質
- 改善 prompts、RAG/KAG、workflows、policies 或 eval metrics
- 使用者給出可衡量的完成目標

除非有可衡量的 Goal Contract，否則不要把 ROD Goal Loop 用在開放式架構設計。

## 基本整合流程

1. 依任務選擇適合的 manifest。
2. 讀取選定的 `skill.json`。
3. 驗證必要欄位：`id`、`name`、`version`、`description`、`entrypoint`、`security`。
4. 解析 Manifest 中的環境變數佔位符，例如 `${ROD_SKILL_MODE:-standard}`。
5. 讀取 `entrypoint.path` 指向的 `SKILL.md`。
6. 將該 `SKILL.md` 注入 Agent，作為 skill、development mode 或 system workflow guideline。

## 環境變數策略

ROD Skills 預設不需要 API Key。若整合層需要外部模型、向量資料庫、私有服務或其他敏感資源，
請使用環境變數或平台 Secret Manager。

不要提交：

- `.env`
- API keys
- access tokens
- private keys
- production credentials
- raw sensitive payloads

建議提交：

- `.env.example`
- config schemas
- redacted sample configs
- 不含敏感值的 defaults

## Manifest 驗證

安裝 helper 後可執行：

```bash
rod-skill validate skill.json
rod-skill validate skills/rod-architecture/skill.json
rod-skill validate skills/rod-goal-loop/skill.json
```

渲染環境變數後的 manifests：

```bash
rod-skill render skill.json
rod-skill render skills/rod-architecture/skill.json
rod-skill render skills/rod-goal-loop/skill.json
```

## 輸出格式

ROD Architecture 應輸出：

```text
ROD Architecture Summary:
- Changed:
- Stable Core protected:
- Evolvable Surfaces:
- Fitness:
- Observability:
- Rollback:
- Remaining gaps:
```

ROD Goal Loop 應輸出：

```text
ROD Goal Loop Summary:
- Goal:
- Final decision:
- Changed:
- Surface:
- Risk:
- Iterations:
- Verification:
- Completion evidence:
- Rollback:
- Remaining gaps:
```

Goal Loop 的 final decision 必須是 `complete`、`blocked`、`needs_review`、`reverted`、`unsafe`
或 `budget_reached` 之一。
