# Manifest Contract

本文說明本 repo 使用的可攜式 `skill.json` contract。這份 contract 刻意保持 platform-neutral；
特定 skill registry 或 agent platform 可能要求額外欄位或更嚴格的驗證。

## 必填欄位

- `manifest_version`：本 package 使用的 manifest contract 版本。
- `id`：穩定、machine-readable 的 skill identifier。
- `name`：人類可讀的 skill 名稱。
- `version`：skill package 版本。
- `description`：清楚說明何時、為何使用此 skill。
- `entrypoint`：描述 instruction entrypoint 的物件。
- `entrypoint.type`：必須是 `markdown`。
- `entrypoint.path`：Markdown instruction file 路徑，通常是 `SKILL.md`。
- `security`：描述 secrets 與 data handling 預期的物件。
- `security.secret_handling_policy`：說明 secrets 應如何處理的必填文字。

## 建議欄位

- `display_name`：方便 review 的顯示名稱。
- `license`：授權識別。
- `language`：主要 instruction 語言。
- `tags`：搜尋與分類標籤。
- `runtime`：runtime 需求，包含 shell、network、filesystem write。
- `configuration`：非敏感預設值與環境變數 placeholders。
- `capabilities`：skill 提供的 machine-readable behaviors。
- `files`：屬於 skill package 的檔案，包含必要 entrypoints。
- `compatibility`：已知 agent runtime 假設。
- `source`：repository、homepage 與 issue tracker 連結。

## 檔案要求

`entrypoint.path` 必須指向存在的 Markdown 檔案。`files` 中任何標示 `required: true`
的檔案，也必須存在於 repository。

## 安全要求

Manifests 與 examples 不應包含真實 secrets、tokens、private keys、production credentials、
private endpoints 或 sensitive payloads。請改用 `${ENV_VAR}` 或 `${ENV_VAR:-default}`
這類環境變數 placeholders。

## Schema

本 repo 提供 `schemas/skill.schema.json` 作為此 contract 的可攜式 JSON Schema。它記錄本
package 使用的預期形狀，但特定平台或 registry 仍可能要求自己的官方 schema。
