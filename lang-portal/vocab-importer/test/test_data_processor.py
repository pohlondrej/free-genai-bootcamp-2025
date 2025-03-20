import pytest
import json
from textwrap import dedent
from src.data_processor import DataProcessor

def test_filter_by_level():
    # Sample test data
    test_subjects = [
        {
            "object": "kanji",
            "data": {"level": 1, "hidden_at": None, "characters": "一"}
        },
        {
            "object": "kanji",
            "data": {"level": 3, "hidden_at": None, "characters": "見"}
        },
        {
            "object": "vocabulary",
            "data": {"level": 2, "hidden_at": None, "characters": "二つ"}
        },
        {
            "object": "kanji",
            "data": {"level": 4, "hidden_at": None, "characters": "私"}
        },
        {
            "object": "vocabulary",
            "data": {"level": 3, "hidden_at": "2024-01-01", "characters": "隠す"}
        }
    ]
    
    # Test filtering at level 3
    processor = DataProcessor(user_level=3)
    filtered = processor.filter_by_level(test_subjects)
    
    assert len(filtered) == 3, "Should only include 3 items (level ≤ 3 and not hidden)"
    assert all(s["data"]["level"] <= 3 for s in filtered), "All items should be level 3 or lower"
    assert all(s["data"]["hidden_at"] is None for s in filtered), "Should not include hidden items"
    
    # Test with lower level
    processor_level_1 = DataProcessor(user_level=1)
    filtered_level_1 = processor_level_1.filter_by_level(test_subjects)
    assert len(filtered_level_1) == 1, "Should only include 1 item at level 1"
    
    # Test with max level (60)
    processor_max = DataProcessor(user_level=60)
    filtered_max = processor_max.filter_by_level(test_subjects)
    assert len(filtered_max) == 4, "Should include all non-hidden items at max level"
    assert sorted([s["data"]["characters"] for s in filtered_max]) == ["一", "二つ", "私", "見"], \
        "Should include all non-hidden items in the correct order"
    
    # Test with empty list
    assert processor.filter_by_level([]) == [], "Should handle empty list"

def test_transform_kanji():
    processor = DataProcessor(user_level=60)  # Level doesn't matter for transformation
    
    # Test kanji with actual Wanikani API response
    test_kanji_json = dedent(r"""
    {
        "id": 440,
        "object": "kanji",
        "url": "https://api.wanikani.com/v2/subjects/440",
        "data_updated_at": "2025-02-26T21:10:49.346405Z",
        "data": {
            "created_at": "2012-02-27T19:55:19.000000Z",
            "level": 1,
            "slug": "一",
            "hidden_at": null,
            "document_url": "https://www.wanikani.com/kanji/%E4%B8%80",
            "characters": "一",
            "meanings": [
                {
                    "meaning": "One",
                    "primary": true,
                    "accepted_answer": true
                }
            ],
            "auxiliary_meanings": [
                {
                    "meaning": "1",
                    "type": "whitelist"
                }
            ],
            "readings": [
                {
                    "reading": "いち",
                    "primary": true,
                    "accepted_answer": true,
                    "type": "onyomi"
                },
                {
                    "reading": "いつ",
                    "primary": false,
                    "accepted_answer": true,
                    "type": "onyomi"
                },
                {
                    "reading": "ひと",
                    "primary": false,
                    "accepted_answer": false,
                    "type": "kunyomi"
                },
                {
                    "reading": "かず",
                    "primary": false,
                    "accepted_answer": false,
                    "type": "nanori"
                }
            ],
            "component_subject_ids": [1],
            "amalgamation_subject_ids": [
                2467, 2468, 2477, 2510, 2544, 2588, 2627, 2660, 2665, 2672,
                2679, 2721, 2730, 2751, 2959, 3048, 3256, 3335, 3348, 3349,
                3372, 3481, 3527, 3528, 3656, 3663, 4133, 4173, 4258, 4282,
                4563, 4615, 4701, 4823, 4906, 5050, 5224, 5237, 5349, 5362,
                5838, 6010, 6029, 6150, 6169, 6209, 6210, 6346, 6584, 6614,
                6723, 6811, 6851, 7037, 7293, 7305, 7451, 7561, 7617, 7734,
                7780, 7927, 8209, 8214, 8414, 8456, 8583, 8709, 8896, 8921,
                9056, 9103, 9268, 9286, 9305, 9306, 9331
            ],
            "visually_similar_subject_ids": [],
            "meaning_mnemonic": "Lying on the <radical>ground</radical> is something that looks just like the ground, the number <kanji>One</kanji>. Why is this One lying down? It's been shot by the number two. It's lying there, bleeding out and dying. The number One doesn't have long to live.",
            "meaning_hint": "To remember the meaning of <kanji>One</kanji>, imagine yourself there at the scene of the crime. You grab <kanji>One</kanji> in your arms, trying to prop it up, trying to hear its last words. Instead, it just splatters some blood on your face. \"Who did this to you?\" you ask. The number One points weakly, and you see number Two running off into an alleyway. He's always been jealous of number One and knows he can be number one now that he's taken the real number one out.",
            "reading_mnemonic": "As you're sitting there next to <kanji>One</kanji>, holding him up, you start feeling a weird sensation all over your skin. From the wound comes a fine powder (obviously coming from the special bullet used to kill One) that causes the person it touches to get extremely <reading>itchy</reading> (いち).",
            "reading_hint": "Make sure you feel the ridiculously <reading>itchy</reading> sensation covering your body. It climbs from your hands, where you're holding the number <kanji>One</kanji> up, and then goes through your arms, crawls up your neck, goes down your body, and then covers everything. It becomes uncontrollable, and you're scratching everywhere, writhing on the ground. It's so itchy that it's the most painful thing you've ever experienced (you should imagine this vividly, so you remember the reading of this kanji).",
            "lesson_position": 25,
            "spaced_repetition_system_id": 2
        }
    }
    """)
    
    test_kanji = json.loads(test_kanji_json)
    transformed = processor.transform_kanji(test_kanji)
    
    assert transformed["id"] == 440, "Should preserve the original ID"
    assert transformed["kanji_level"] == "WK_1", "Should format level as WK_1"
    assert transformed["symbol"] == "一", "Should preserve the kanji character"
    assert transformed["meanings"] == "One", "Should only include primary meaning"
    assert transformed["primary_reading"] == "いち", "Should use primary reading"
    assert transformed["primary_reading_type"] == "onyomi", "Should preserve reading type"

def test_transform_vocabulary():
    processor = DataProcessor(user_level=60)  # Level doesn't matter for transformation
    
    # Test vocabulary with actual Wanikani API response
    test_vocab_json = dedent(r"""
    {
        "id": 2467,
        "object": "vocabulary",
        "url": "https://api.wanikani.com/v2/subjects/2467",
        "data_updated_at": "2023-06-26T22:54:13.669641Z",
        "data": {
            "created_at": "2012-02-28T08:04:47.000000Z",
            "level": 1,
            "slug": "一つ",
            "hidden_at": null,
            "document_url": "https://www.wanikani.com/vocabulary/一つ",
            "characters": "一つ",
            "meanings": [
                {
                    "meaning": "One Thing",
                    "primary": true,
                    "accepted_answer": true
                }
            ],
            "readings": [
                {
                    "reading": "ひとつ",
                    "primary": true,
                    "accepted_answer": true
                }
            ],
            "parts_of_speech": [
                "numeral"
            ],
            "component_subject_ids": [
                440
            ],
            "meaning_mnemonic": "This word consists of <kanji>One</kanji> and つ, which is the counter for things. Put them together and you get <vocabulary>One Thing</vocabulary>.",
            "reading_mnemonic": "When you see the つ after <kanji>One</kanji> you know it's going to be the つ-counter word for one, which is <reading>ひとつ</reading>.",
            "context_sentences": [
                {
                    "en": "Please give me one.",
                    "ja": "一つください。"
                },
                {
                    "en": "There's one more thing.",
                    "ja": "もう一つあります。"
                }
            ]
        }
    }
    """)
    
    test_vocab = json.loads(test_vocab_json)
    transformed = processor.transform_vocabulary(test_vocab)
    
    assert transformed["id"] == 2467, "Should preserve the original ID"
    assert transformed["word_level"] == "WK_1", "Should format level as WK_1"
    assert transformed["japanese"] == "一つ", "Should preserve the vocabulary"
    assert transformed["kana"] == "ひとつ", "Should use primary reading"
    assert transformed["english"] == "One Thing", "Should use primary meaning"
    assert transformed["romaji"] == "", "Romaji should be empty for now"
