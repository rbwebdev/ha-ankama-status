"""Constants for the Ankama Status integration."""

DOMAIN = "ankama_status"
ANKAMA_API_URL = "https://status.cdn.ankama.com/export.json"

DEFAULT_SCAN_INTERVAL = 300  # 5 minutes

# Status mapping
STATUS_ONLINE = "Up"
STATUS_MAINTENANCE = "Maintenance"
STATUS_OFFLINE = "Down"
