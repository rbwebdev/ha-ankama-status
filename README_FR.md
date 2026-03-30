# Ankama Game Servers Status - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

🇬🇧 [English version](README.md)

Intégration Home Assistant pour surveiller l'état des serveurs de jeu Ankama (Dofus 3, Wakfu, Waven, Dofus Touch, Dofus Retro).

## 🎮 Fonctionnalités

- ✅ Surveillance en temps réel de tous les serveurs Ankama
- ✅ Un sensor par serveur de jeu
- ✅ États : Up, Maintenance, Down
- ✅ Attributs détaillés : noms multilingues, tags, type de jeu
- ✅ Mise à jour configurable (par défaut 5 minutes)
- ✅ Filtrage par jeu (optionnel)
- ✅ Automatisations basées sur les changements d'état
- ✅ Groupement par jeu dans l'interface

## 📦 Installation

### Via HACS (recommandé)

1. Ouvrez HACS dans Home Assistant
2. Cliquez sur "Integrations"
3. Cliquez sur les 3 points en haut à droite et sélectionnez "Custom repositories"
4. Ajoutez l'URL de ce repository : `https://github.com/rbwebdev/ha-ankama-status`
5. Catégorie : Integration
6. Cliquez sur "Ankama Game Servers Status" dans la liste
7. Cliquez sur "Download"
8. Redémarrez Home Assistant

### Installation manuelle

1. Téléchargez ce repository
2. Copiez le dossier `custom_components/ankama_status` dans votre dossier `config/custom_components/`
3. Redémarrez Home Assistant

## ⚙️ Configuration

### Via l'interface utilisateur (recommandé)

1. Allez dans `Paramètres` > `Appareils et services`
2. Cliquez sur `+ Ajouter une intégration`
3. Recherchez "Ankama"
4. Configurez les options :
   - **Filtrer par jeu** : Choisissez un jeu spécifique ou "Tous les jeux"
   - **Intervalle de mise à jour** : Fréquence de rafraîchissement (60-3600 secondes, défaut : 300)

### Options de configuration

| Option | Description | Défaut |
|--------|-------------|--------|
| `game_filter` | Filtrer les serveurs par jeu (`all`, `dofus2`, `wakfu`, `waven`, `dofusTouch`, `dofusRetro`) | `all` |
| `scan_interval` | Intervalle de mise à jour en secondes | `300` |

## 🎯 Utilisation

### Sensors créés

L'intégration crée automatiquement un sensor pour chaque serveur de jeu détecté. Les sensors sont nommés selon le format :
```
sensor.dofus2_brial
sensor.wakfu_ogrest
sensor.waven_europe
```

### États possibles

- `Up` : Serveur en ligne
- `Maintenance` : Serveur en maintenance
- `Down` : Serveur hors ligne

### Attributs des sensors

Chaque sensor possède les attributs suivants :
- `server_name_en` : Nom en anglais
- `server_name_fr` : Nom en français
- `server_name_es` : Nom en espagnol
- `server_name_de` : Nom en allemand
- `server_name_pt` : Nom en portugais
- `game` : Type de jeu (dofus2, wakfu, etc.)
- `tags` : Liste des tags associés

## 🤖 Exemples d'automatisations

### Notification quand un serveur revient en ligne

```yaml
automation:
  - alias: "Notification serveur Dofus en ligne"
    trigger:
      - platform: state
        entity_id: sensor.dofus2_brial
        to: "Up"
        from: "Maintenance"
    action:
      - service: notify.mobile_app
        data:
          title: "🎮 Serveur Dofus"
          message: "Le serveur Brial est de nouveau en ligne !"
```

### Notification pour tous les serveurs Wakfu

```yaml
automation:
  - alias: "Notification serveurs Wakfu"
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
          title: "🎮 Serveur Wakfu"
          message: "Le serveur {{ trigger.to_state.name }} est en ligne !"
```

### Alerte si un serveur est hors ligne

```yaml
automation:
  - alias: "Alerte serveur hors ligne"
    trigger:
      - platform: state
        entity_id: sensor.dofus2_brial
        to: "Down"
    action:
      - service: persistent_notification.create
        data:
          title: "⚠️ Serveur hors ligne"
          message: "Le serveur {{ trigger.to_state.name }} est hors ligne depuis {{ relative_time(trigger.to_state.last_changed) }}"
```

### Carte Lovelace pour afficher tous les serveurs

```yaml
type: entities
title: Serveurs Ankama
entities:
  - entity: sensor.dofus2_brial
  - entity: sensor.dofus2_mikhal
  - entity: sensor.wakfu_ogrest
  - entity: sensor.waven_europe
state_color: true
```

### Carte conditionnelle (afficher uniquement les serveurs en maintenance)

```yaml
type: conditional
conditions:
  - entity: sensor.dofus2_brial
    state: Maintenance
card:
  type: entities
  title: ⚠️ Serveurs en maintenance
  entities:
    - sensor.dofus2_brial
```

## 🔧 Développement

### Structure du projet

```
custom_components/ankama_status/
├── __init__.py           # Point d'entrée de l'intégration
├── config_flow.py        # Configuration via l'UI
├── const.py              # Constantes
├── manifest.json         # Métadonnées de l'intégration
├── sensor.py             # Logique des sensors
├── strings.json          # Traductions (anglais)
└── translations/
    └── fr.json          # Traductions (français)
```

### API utilisée

L'intégration utilise l'API publique d'Ankama :
```
https://status.cdn.ankama.com/export.json
```

Format de réponse :
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

## 🐛 Débogage

Pour activer les logs de débogage, ajoutez dans votre `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.ankama_status: debug
```

## 📝 Changelog

### Version 1.0.1
- 📄 Le README anglais est maintenant le README principal (version française déplacée dans README_FR.md)

### Version 1.0.0
- 🎉 Version initiale
- ✅ Support de tous les jeux Ankama
- ✅ Configuration via l'UI
- ✅ Mise à jour automatique
- ✅ Traductions FR/EN

## 🤝 Contributions

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Licence

MIT License

## 👏 Crédits

- Données fournies par [Ankama](https://www.ankama.com)
- Développé pour [Home Assistant](https://www.home-assistant.io)
- Codé avec [Claude](https://claude.ai)

## ⚠️ Disclaimer

Cette intégration n'est pas officielle et n'est pas affiliée à Ankama. Elle utilise l'API publique d'Ankama pour fournir des informations sur l'état des serveurs.
