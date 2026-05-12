#!/usr/bin/env python3
"""Validate the encounter-rate and economy rebalance invariants."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WILD_JSON = ROOT / "src" / "data" / "wild_encounters.json"
BATTLE_COMMANDS = ROOT / "src" / "battle_script_commands.c"
ITEM_C = ROOT / "src" / "item.c"

EXPECTED_RATES = {
    "land_mons": [15, 15, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5],
    "water_mons": [50, 25, 10, 10, 5],
    "rock_smash_mons": [50, 25, 10, 10, 5],
    "fishing_mons": [70, 30, 60, 25, 15, 40, 25, 20, 10, 5],
}

EXPECTED_DEFINES = {
    "WILD_EXP_PERCENT": "160",
    "TRAINER_EXP_PERCENT": "130",
    "ITEM_PRICE_PERCENT": "60",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def require_define(source: str, name: str, value: str) -> None:
    if not re.search(rf"^#define\s+{name}\s+{value}\b", source, re.MULTILINE):
        fail(f"missing expected define {name} {value}")


def validate_encounter_rates() -> None:
    with WILD_JSON.open() as f:
        data = json.load(f)

    fields = data["wild_encounter_groups"][0]["fields"]
    seen = set()
    for field in fields:
        field_type = field["type"]
        if field_type not in EXPECTED_RATES:
            continue

        rates = field["encounter_rates"]
        expected = EXPECTED_RATES[field_type]
        seen.add(field_type)
        if rates != expected:
            fail(f"{field_type} rates {rates} do not match expected {expected}")

        if field_type == "fishing_mons":
            for group_name, indexes in field["groups"].items():
                total = sum(rates[index] for index in indexes)
                if total != 100:
                    fail(f"{field_type}.{group_name} totals {total}, expected 100")
        else:
            total = sum(rates)
            if total != 100:
                fail(f"{field_type} totals {total}, expected 100")

        routine_bad_rates = sorted(rate for rate in set(rates) if rate in (2, 3, 4))
        if routine_bad_rates:
            fail(f"{field_type} still uses below-floor routine rates {routine_bad_rates}")

    missing = sorted(set(EXPECTED_RATES) - seen)
    if missing:
        fail(f"missing encounter fields: {missing}")


def validate_economy_constants() -> None:
    battle_source = BATTLE_COMMANDS.read_text()
    item_source = ITEM_C.read_text()

    require_define(battle_source, "WILD_EXP_PERCENT", EXPECTED_DEFINES["WILD_EXP_PERCENT"])
    require_define(battle_source, "TRAINER_EXP_PERCENT", EXPECTED_DEFINES["TRAINER_EXP_PERCENT"])
    require_define(item_source, "ITEM_PRICE_PERCENT", EXPECTED_DEFINES["ITEM_PRICE_PERCENT"])

    if "GetWildBattleMoneyReward" not in battle_source:
        fail("wild battle money reward helper is missing")
    if "GetWildBattleMoneyReward()" not in battle_source:
        fail("wild battle money reward is not wired into payout flow")


def main() -> None:
    validate_encounter_rates()
    validate_economy_constants()
    print("Rebalance validation passed.")


if __name__ == "__main__":
    main()
