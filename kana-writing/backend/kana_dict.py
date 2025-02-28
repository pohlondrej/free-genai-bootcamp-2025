from typing import List, Dict
import random

KANA_WORDS: List[Dict[str, str]] = [
    {"kana": "ひらがな", "romaji": "hiragana"},
    {"kana": "かたかな", "romaji": "katakana"},
    {"kana": "にほんご", "romaji": "nihongo"},
    {"kana": "おはよう", "romaji": "ohayou"},
    {"kana": "ありがとう", "romaji": "arigatou"},
    {"kana": "さようなら", "romaji": "sayounara"},
    {"kana": "こんにちは", "romaji": "konnicha"},
    {"kana": "すみません", "romaji": "sumimasen"},
    {"kana": "たべもの", "romaji": "tabemono"},
    {"kana": "のみもの", "romaji": "nomimono"},
    {"kana": "がっこう", "romaji": "gakkou"},
    {"kana": "せんせい", "romaji": "sensei"},
    {"kana": "でんわ", "romaji": "denwa"},
    {"kana": "れんしゅう", "romaji": "renshuu"},
    {"kana": "きょうかしょ", "romaji": "kyoukasho"},
    {"kana": "しゅくだい", "romaji": "shukudai"},
    {"kana": "えんぴつ", "romaji": "enpitsu"},
    {"kana": "かんじ", "romaji": "kanji"},
    {"kana": "ともだち", "romaji": "tomodachi"},
    {"kana": "せいと", "romaji": "seito"},
]

def get_random_word() -> Dict[str, str]:
    return random.choice(KANA_WORDS)
