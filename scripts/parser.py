def parse_player(data: dict) -> dict:
    clan = data.get("clan") or {}

    # Prefer current Path of Legend season trophies, fall back to all-time best
    season = data.get("currentPathOfLegendSeasonResult") or {}
    best_trophies = season.get("trophies") or data.get("bestTrophies", 0)

    return {
        "player_name": data.get("name", "N/A"),
        "trophies": data.get("trophies", 0),
        "exp_level": data.get("expLevel", 0),
        "clan_name": clan.get("name", "No Clan"),
        "wins": data.get("wins", 0),
        "cards_found": len(data.get("cards", [])),
        "best_trophies": best_trophies,
    }
