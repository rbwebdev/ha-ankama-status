# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Home Assistant custom integration that monitors Ankama game server statuses (Dofus 3, Wakfu, Waven, Dofus Touch, Dofus Retro) via the public API at `https://status.cdn.ankama.com/export.json`. HACS-compatible. Written in Python, requires HA 2023.1.0+.

## Development

No build system, test framework, or CI/CD pipeline is configured. The integration is installed by copying `custom_components/ankama_status/` into a Home Assistant instance's `config/custom_components/` directory.

To enable debug logging in Home Assistant:
```yaml
logger:
  logs:
    custom_components.ankama_status: debug
```

## Architecture

All source lives in `custom_components/ankama_status/`.

**Data flow:** Ankama API → `AnkamaStatusCoordinator` (in `sensor.py`) → `AnkamaServerSensor` entities → HA state machine

Key patterns:
- **DataUpdateCoordinator** (`sensor.py`): Single coordinator polls the API at a configurable interval (default 300s, range 60-3600s) and shares data with all sensor entities. This prevents redundant API calls.
- **Config Entry flow** (`config_flow.py`): UI-based setup with game filter selection and scan interval. Validates API connectivity during setup. Prevents duplicate instances.
- **CoordinatorEntity inheritance**: Each `AnkamaServerSensor` inherits from `CoordinatorEntity` for automatic update management.
- **Game filtering**: Applied at entity creation time — only sensors matching the selected game tag are created.
- **Device grouping**: Sensors are grouped by game type (e.g., all Dofus 3 servers under one device).

**File responsibilities:**
- `__init__.py` — Integration setup/teardown, registers the sensor platform
- `sensor.py` — `AnkamaStatusCoordinator` (API fetching) and `AnkamaServerSensor` (entity logic, state, attributes, icons)
- `config_flow.py` — User configuration UI, API validation, options schema
- `const.py` — Domain name, API URL, default interval, status constants (`Up`/`Maintenance`/`Down`)
- `strings.json` / `translations/fr.json` — UI strings in English/French

**Entity ID format:** `sensor.ankama_status_{game}_{server_name_en_lowercase}`

**Sensor states:** `Up`, `Maintenance`, `Down` — icons change dynamically based on status.

## API Response Format

The API returns a flat JSON array. Each entry has `tags` (list including game identifier like `dofus2`), `names` (dict with `de`/`en`/`es`/`fr`/`pt` keys), and `status` (string).

## Notes

- The integration uses `aiohttp` (provided by HA) for async HTTP with a 30-second timeout.
- Primary documentation (README.md) is in French.
- No external pip requirements — only HA built-in libraries.
