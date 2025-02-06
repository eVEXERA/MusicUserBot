"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import json


def load(lang):
    return json.loads(open(f"./lang/{lang}.json", "r"))
