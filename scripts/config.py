API_BASE_URL = "https://api.clashroyale.com/v1/players/%23{tag}"

# The font-family name used inside the SVG template.
# The injected @font-face rule will declare this same name pointing at the .otf file.
FONT_FAMILY_PLACEHOLDER = "Itim"

PLACEHOLDER_MAP = {
    "player_name": "{{player_name}}",
    "trophies": "{{trophies}}",
    "exp_level": "{{exp_level}}",
    "clan_name": "{{clan_name}}",
    "wins": "{{wins}}",
    "cards_found": "{{cards_found}}",
    "best_trophies": "{{best_trophies}}",
}

DEFAULT_TEMPLATE = "banner/banner.svg"
DEFAULT_OUT = "card_filled.svg"
