# ROD Skill 整合指南

本文件說明如何將 ROD Skill 整合到支援 Manifest / Skill 的 AI Agent runtime。

## 基本整合流程

1. 讀取 `skill.json`。
2. 驗證必要欄位：`id`、`name`、`version`、`description`、`entrypoint`、`security`。
3. 解析 Manifest 中的環境變數佔位符，例如 `${ROD_SKILL_MODE:-standard}`。
4. 讀取 `entrypoint.path` 指向的 `SKILL.md`。
5. 將 `SKILL.md` 注入到 Agent 的技能、開發模式或系統流程中。
6. 在執行會影響行為、品質、安全、資料、workflow、RAG/KAG、policy 或 release 的任務時啟用 ROD。

## 環境變數策略

ROD Skill 本身不需要 API Key。若你的整合層需要外部模型、向量資料庫或私有服務，請使用環境變數或平台 Secret Manager。

不要提交：

- `.env`
- API keys
- access tokens
- private keys
- production credentials
- raw sensitive payloads

建議提交：

- `.env.example`
- config schema
- redacted sample config
- 不含敏感值的 defaults

## Manifest 驗證

安裝 helper 後可執行：

```bash
rod-skill validate skill.json
```

渲染環境變數後的 Manifest：

```bash
rod-skill render skill.json
```

## Agent 使用建議

當任務屬於以下類型，建議啟用 ROD Standard 或 Strict Mode：

- feature / bug fix / refactor
- prompt、workflow、policy、RAG/KAG 或 config 改動
- auth、permission、secrets、migration、production release gate
- AI 輸出品質、安全、grounding 或 citation 行為變更

對於 typo、格式、註解、單純文件修正，可使用 Lightweight Mode。

## 輸出格式

ROD-guided 任務完成時，Agent 應輸出：

```text
ROD Summary:
- Changed:
- Surface:
- Risk:
- Fitness:
- Rollback:
- Remaining gaps:
```

這可讓使用者快速知道改了什麼、風險在哪、如何驗證，以及如何回滾。
