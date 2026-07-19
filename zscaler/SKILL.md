---
name: zscaler
description: >-
  Manage Zscaler ZPA, ZIA, and ZIdentity via the official Python SDK (users,
  groups, URL categories, URL filtering policies, forwarding/Dedicated IP rules,
  IP groups, activation). Use when the user mentions Zscaler, ZIA, ZPA,
  Dedicated IP, forwarding rules, URL filtering, or invokes /zscaler_*.
disable-model-invocation: true
---

# zscaler

## When to use

Use for Zscaler admin API work. Trigger phrases: "ZIA users", "create forwarding rule", "URL filtering policy", "Dedicated IP", "URL category", "activate ZIA", `/zscaler_zia_*`, `/zscaler_zpa_*`.

## Working directory

`~/.ai-pro-skills/zscaler`

## Shared environment (see AI-Skills README)

- **Python**: run through the shared venv — `~/.ai-pro-skills/.venv/bin/python cli.py …`. Install the Zscaler SDK once into the shared venv from the skill dir: `~/.ai-pro-skills/install.sh pip init .` (installs this skill's `requirements.txt`; do not create a per-skill `.venv`).
- **Config**: this skill keeps its **own** `config.json` — placed **next to the installed `SKILL.md`** (the chosen client's skill folder: `~/.cursor/skills/…`, `./.cursor/skills/…` for a project, `$HERMES_HOME/.../…`, etc.), exactly where a `.env` would go. Generate it there with `/zscaler_setup`. Never commit real tokens.

```bash
~/.ai-pro-skills/.venv/bin/python cli.py test
```

## Slash commands

### Global

| Slash | CLI | Description |
|-------|-----|-------------|
| `/zscaler_setup` | `python cli.py setup` | Interactive token setup |
| `/zscaler_test` | `python cli.py test [all\|zpa\|zia\|zidentity]` | Connection test |

### ZPA

| Slash | CLI | Description |
|-------|-----|-------------|
| `/zscaler_zpa_segments` | `python cli.py zpa segments` | List application segments |
| `/zscaler_zpa_groups` | `python cli.py zpa groups` | List segment groups |

### ZIdentity

| Slash | CLI | Description |
|-------|-----|-------------|
| `/zscaler_zidentity_groups` | `python cli.py zidentity groups` | List groups |
| `/zscaler_zidentity_users` | `python cli.py zidentity users` | List users |

### ZIA — users / groups

| Slash | CLI | Description |
|-------|-----|-------------|
| `/zscaler_zia_users` | `python cli.py zia users` | List users |
| `/zscaler_zia_groups` | `python cli.py zia groups` | List user groups |
| `/zscaler_zia_departments` | `python cli.py zia departments [--search T]` | List departments |
| `/zscaler_zia_get-user` | `python cli.py zia get-user --username EMAIL` | Get user |
| `/zscaler_zia_set-groups` | `python cli.py zia set-groups …` | Set/add/remove user groups |

### ZIA — URL categories

| Slash | CLI | Description |
|-------|-----|-------------|
| `/zscaler_zia_url-categories` | `python cli.py zia url-categories` | List categories |
| `/zscaler_zia_create-url-category` | `python cli.py zia create-url-category --name N --url …` | Create category |
| `/zscaler_zia_add-url` | `python cli.py zia add-url --category-name N --url …` | Add URLs |
| `/zscaler_zia_remove-url` | `python cli.py zia remove-url --category-name N --url …` | Remove URLs |

### ZIA — URL filtering policies

| Slash | CLI | Description |
|-------|-----|-------------|
| `/zscaler_zia_url-filtering-rules` | `python cli.py zia url-filtering-rules [--search T]` | List rules |
| `/zscaler_zia_get-url-filtering-rule` | `python cli.py zia get-url-filtering-rule --rule-name N` | Get rule |
| `/zscaler_zia_create-url-filtering-rule` | `python cli.py zia create-url-filtering-rule …` | Create rule |
| `/zscaler_zia_update-url-filtering-rule` | `python cli.py zia update-url-filtering-rule …` | Update rule |
| `/zscaler_zia_delete-url-filtering-rule` | `python cli.py zia delete-url-filtering-rule …` | Delete rule |

Updatable fields: `--category-id`/`--category-name`, `--request-method`, `--group-id`/`--group-name`, `--rule-user-id`/`--rule-username`, `--order` (rule number), `--filter-action`.

```bash
python cli.py zia create-url-filtering-rule \
  --name "Block Adult" \
  --filter-action BLOCK \
  --category-id OTHER_ADULT_MATERIAL \
  --group-name "Vo2 - Canada" \
  --order 5

python cli.py zia update-url-filtering-rule \
  --rule-name "Block Adult" \
  --filter-action ALLOW \
  --request-method GET --request-method POST \
  --order 3
```

### ZIA — forwarding / Dedicated IP

| Slash | CLI | Description |
|-------|-----|-------------|
| `/zscaler_zia_forwarding-rules` | `python cli.py zia forwarding-rules [--search T]` | List rules |
| `/zscaler_zia_get-forwarding-rule` | `python cli.py zia get-forwarding-rule --rule-name N` | Get rule |
| `/zscaler_zia_create-forwarding-rule` | `python cli.py zia create-forwarding-rule …` | Create rule (default `ENATDEDIP`) |
| `/zscaler_zia_delete-forwarding-rule` | `python cli.py zia delete-forwarding-rule …` | Delete rule |
| `/zscaler_zia_dedicated-ips` | `python cli.py zia dedicated-ips` | List Dedicated IP gateways |

Typical Dedicated IP create (group + URL category + gateway):

```bash
python cli.py zia create-forwarding-rule \
  --name "SF Canada - use dedicated ip" \
  --gateway-name "Canada - Gateway" \
  --group-name "Vo2 - Canada" \
  --category-id CUSTOM_03
```

### ZIA — IP groups (firewall)

| Slash | CLI | Description |
|-------|-----|-------------|
| `/zscaler_zia_dest-ip-groups` | `python cli.py zia dest-ip-groups` | List dest IP groups |
| `/zscaler_zia_get-dest-ip-group` | `python cli.py zia get-dest-ip-group …` | Get dest group |
| `/zscaler_zia_create-dest-ip-group` | `python cli.py zia create-dest-ip-group …` | Create dest group |
| `/zscaler_zia_update-dest-ip-group` | `python cli.py zia update-dest-ip-group …` | Update dest group |
| `/zscaler_zia_delete-dest-ip-group` | `python cli.py zia delete-dest-ip-group …` | Delete dest group |
| `/zscaler_zia_source-ip-groups` | `python cli.py zia source-ip-groups` | List source IP groups |
| `/zscaler_zia_get-source-ip-group` | `python cli.py zia get-source-ip-group …` | Get source group |
| `/zscaler_zia_create-source-ip-group` | `python cli.py zia create-source-ip-group …` | Create source group |
| `/zscaler_zia_update-source-ip-group` | `python cli.py zia update-source-ip-group …` | Update source group |
| `/zscaler_zia_delete-source-ip-group` | `python cli.py zia delete-source-ip-group …` | Delete source group |

### ZIA — activation

| Slash | CLI | Description |
|-------|-----|-------------|
| `/zscaler_zia_activation-status` | `python cli.py zia activation-status` | Pending / active |
| `/zscaler_zia_activate` | `python cli.py zia activate` | Activate pending changes |

## How to run

1. `cd ~/.ai-pro-skills/zscaler`; use the shared venv (`~/.ai-pro-skills/.venv/bin/python`).
2. Ensure `config.json` **next to the installed `SKILL.md`** (from `config.example.json`) or run `/zscaler_setup`.
3. Map `/{skill}_{product}_{action}` to `~/.ai-pro-skills/.venv/bin/python cli.py <product> <action> …`.
4. After ZIA create/update/delete, run `/zscaler_zia_activate` (or remind the user).
5. Return JSON/CLI output to the user.

## Notes

- Rule names max **31** characters for forwarding rules.
- API wire field for Dedicated IP is `dedicatedIPGateway` (handled by the CLI).
- Never commit `config.json` tokens.
- Full human docs: `README.md` / `README-FR.md`.
