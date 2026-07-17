---
name: zscaler
description: >-
  Manage Zscaler ZPA, ZIA, and ZIdentity via the official Python SDK (users,
  groups, URL categories, forwarding/Dedicated IP rules, IP groups, activation).
  Use when the user mentions Zscaler, ZIA, ZPA, Dedicated IP, forwarding rules,
  or invokes /zscaler_*.
disable-model-invocation: true
---

# zscaler

## When to use

Use for Zscaler admin API work. Trigger phrases: "ZIA users", "create forwarding rule", "Dedicated IP", "URL category", "activate ZIA", `/zscaler_zia_*`, `/zscaler_zpa_*`.

## Working directory

`~/.ai-pro-skills/zscaler`

Prefer the local venv:

```bash
source .venv/bin/activate   # if present
python cli.py …
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

1. `cd ~/.ai-pro-skills/zscaler`; activate `.venv` if present.
2. Ensure `config.json` (from `config.example.json`) or run `/zscaler_setup`.
3. Map `/{skill}_{product}_{action}` to `python cli.py <product> <action> …`.
4. After ZIA create/update/delete, run `/zscaler_zia_activate` (or remind the user).
5. Return JSON/CLI output to the user.

## Notes

- Rule names max **31** characters for forwarding rules.
- API wire field for Dedicated IP is `dedicatedIPGateway` (handled by the CLI).
- Never commit `config.json` tokens.
- Full human docs: `README.md` / `README-FR.md`.
