"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import json


def load(lang):
    return json.load(open(f"./Language/{Language}.json", "r"))
