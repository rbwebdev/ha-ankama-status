# Ankama Game Servers Status - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

🇫🇷 [Version française](README_FR.md)

Home Assistant custom integration to monitor Ankama game server statuses (Dofus 3, Wakfu, Waven, Dofus Touch, Dofus Retro).

## 🎮 Features

- ✅ Real-time monitoring of all Ankama servers
- ✅ One sensor per game server
- ✅ States: Up, Maintenance, Down
- ✅ Detailed attributes: multilingual names, tags, game type
- ✅ Configurable update interval (default 5 minutes)
- ✅ Optional game filtering
- ✅ Automations based on state changes
- ✅ Grouped by game in the UI

## 📦 Installation

### Via HACS (recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the 3 dots in the top right corner and select "Custom repositories"
4. Add this repository URL: `https://github.com/rbwebdev/ha-ankama-status`
5. Category: Integration
6. Click on "Ankama Game Servers Status" in the list
7. Click "Download"
8. Restart Home Assistant

### Manual installation

1. Download this repository
2. Copy the `custom_components/ankama_status` folder into your `config/custom_components/` directory
3. Restart Home Assistant

## ⚙️ Configuration

### Via the UI (recommended)

1. Go to `Settings` > `Devices & Services`
2. Click `+ Add Integration`
3. Search for "Ankama"
4. Configure options:
   - **Filter by game**: Choose a specific game or "All games"
   - **Update interval**: Refresh frequency (60-3600 seconds, default: 300)

### Configuration options

| Option | Description | Default |
|--------|-------------|---------|
| `game_filter` | Filter servers by game (`all`, `dofus2`, `wakfu`, `waven`, `dofusTouch`, `dofusRetro`) | `all` |
| `scan_interval` | Update interval in seconds | `300` |

## 🎯 Usage

### Created sensors

The integration automatically creates one sensor per detected game server. Sensors are named as follows:
```
sensor.dofus2_brial
sensor.wakfu_ogrest
sensor.waven_europe
```

### Possible states

- `Up`: Server online
- `Maintenance`: Server under maintenance
- `Down`: Server offline

### Sensor attributes

Each sensor has the following attributes:
- `server_name_en`: Name in English
- `server_name_fr`: Name in French
- `server_name_es`: Name in Spanish
- `server_name_de`: Name in German
- `server_name_pt`: Name in Portuguese
- `game`: Game type (dofus2, wakfu, etc.)
- `tags`: Associated tags list

## 🤖 Automation examples

### Notification when a server comes back online

```yaml
automation:
  - alias: "Dofus server online notification"
    trigger:
      - platform: state
        entity_id: sensor.dofus2_brial
        to: "Up"
        from: "Maintenance"
    action:
      - service: notify.mobile_app
        data:
          title: "🎮 Dofus Server"
          message: "Server Brial is back online!"
```

### Notification for all Wakfu servers

```yaml
automation:
  - alias: "Wakfu servers notification"
    trigger:
      - platform: state
        entity_id:
          - sensor.wakfu_ogrest
          - sensor.wakfu_rubilax
          - sensor.wakfu_pandora
        to: "Up"
    action:
      - service: notify.mobile_app
        data:
          title: "🎮 Wakfu Server"
          message: "Server {{ trigger.to_state.name }} is online!"
```

### Alert if a server goes offline

```yaml
automation:
  - alias: "Server offline alert"
    trigger:
      - platform: state
        entity_id: sensor.dofus2_brial
        to: "Down"
    action:
      - service: persistent_notification.create
        data:
          title: "⚠️ Server offline"
          message: "Server {{ trigger.to_state.name }} has been offline since {{ relative_time(trigger.to_state.last_changed) }}"
```

### Lovelace card to display all servers

```yaml
type: entities
title: Ankama Servers
entities:
  - entity: sensor.dofus2_brial
  - entity: sensor.dofus2_mikhal
  - entity: sensor.wakfu_ogrest
  - entity: sensor.waven_europe
state_color: true
```

### Conditional card (show only servers under maintenance)

```yaml
type: conditional
conditions:
  - entity: sensor.dofus2_brial
    state: Maintenance
card:
  type: entities
  title: ⚠️ Servers under maintenance
  entities:
    - sensor.dofus2_brial
```

## 🔧 Development

### Project structure

```
custom_components/ankama_status/
├── __init__.py           # Integration entry point
├── config_flow.py        # UI configuration
├── const.py              # Constants
├── manifest.json         # Integration metadata
├── sensor.py             # Sensor logic
├── strings.json          # Translations (English)
└── translations/
    └── fr.json          # Translations (French)
```

### API used

The integration uses the public Ankama API:
```
https://status.cdn.ankama.com/export.json
```

Response format:
```json
[
  {
    "tags": ["dofus2", "game-server"],
    "names": {
      "de": "Brial",
      "en": "Brial",
      "es": "Brial",
      "fr": "Brial",
      "pt": "Brial"
    },
    "status": "Up"
  }
]
```

## 🐛 Debugging

To enable debug logging, add to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.ankama_status: debug
```

## 📝 Changelog

### Version 1.0.1
- 📄 English README is now the primary README (French version moved to README_FR.md)

### Version 1.0.0
- 🎉 Initial release
- ✅ Support for all Ankama games
- ✅ UI configuration
- ✅ Automatic updates
- ✅ FR/EN translations

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or a pull request.

## 📄 License

MIT License

## 👏 Credits

- Data provided by [Ankama](https://www.ankama.com)
- Built for [Home Assistant](https://www.home-assistant.io)
- Coded with [Claude](https://claude.ai)

## ⚠️ Disclaimer

This integration is unofficial and is not affiliated with Ankama. It uses the public Ankama API to provide server status information.
