# Project Specification

## Project Structure
- `main.py` - Main script to run the importer
- `wanikani_client.py` - Client for Wanikani API
- `data_processor.py` - Processes and filters the data
- `sql_generator.py` - Generates SQL migration scripts
- `test/` - Test files
  - `test_data_processor.py` - Tests for data processing
  - `test_sql_generator.py` - Tests for SQL generation

## Wanikani API
[API Reference](https://docs.api.wanikani.com/20170710/)
### Get All Subjects
#### Request
```bash
curl "https://api.wanikani.com/v2/subjects" \
  -H "Wanikani-Revision: 20170710" \
  -H "Authorization: Bearer <api_token_here>"
```
#### Response
```json
{
  "object": "collection",
  "url": "https://api.wanikani.com/v2/subjects?types=kanji",
  "pages": {
    "per_page": 1000,
    "next_url": "https://api.wanikani.com/v2/subjects?page_after_id=1439\u0026types=kanji",
    "previous_url": null
  },
  "total_count": 2027,
  "data_updated_at": "2018-04-09T18:08:59.946969Z",
  "data": [
    {
      "id": 440,
      "object": "kanji",
      "url": "https://api.wanikani.com/v2/subjects/440",
      "data_updated_at": "2018-03-29T23:14:30.805034Z",
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
        "readings": [
          {
            "type": "onyomi",
            "primary": true,
            "accepted_answer": true,
            "reading": "いち"
          },
          {
            "type": "kunyomi",
            "primary": false,
            "accepted_answer": false,
            "reading": "ひと"
          },
          {
            "type": "nanori",
            "primary": false,
            "accepted_answer": false,
            "reading": "かず"
          }
        ],
        "component_subject_ids": [
          1
        ],
        "amalgamation_subject_ids": [
          56,
          88,
          91
        ],
        "visually_similar_subject_ids": [],
        "meaning_mnemonic": "Lying on the <radical>ground</radical> is something that looks just like the ground, the number <kanji>One</kanji>. Why is this One lying down? It's been shot by the number two. It's lying there, bleeding out and dying. The number One doesn't have long to live.",
        "meaning_hint": "To remember the meaning of <kanji>One</kanji>, imagine yourself there at the scene of the crime. You grab <kanji>One</kanji> in your arms, trying to prop it up, trying to hear its last words. Instead, it just splatters some blood on your face. \"Who did this to you?\" you ask. The number One points weakly, and you see number Two running off into an alleyway. He's always been jealous of number One and knows he can be number one now that he's taken the real number one out.",
        "reading_mnemonic": "As you're sitting there next to <kanji>One</kanji>, holding him up, you start feeling a weird sensation all over your skin. From the wound comes a fine powder (obviously coming from the special bullet used to kill One) that causes the person it touches to get extremely <reading>itchy</reading> (いち)",
        "reading_hint": "Make sure you feel the ridiculously <reading>itchy</reading> sensation covering your body. It climbs from your hands, where you're holding the number <kanji>One</kanji> up, and then goes through your arms, crawls up your neck, goes down your body, and then covers everything. It becomes uncontrollable, and you're scratching everywhere, writhing on the ground. It's so itchy that it's the most painful thing you've ever experienced (you should imagine this vividly, so you remember the reading of this kanji).",
        "lesson_position": 2,
        "spaced_repetition_system_id": 1
      }
    }
  ]
}
```
### Get user information
#### Request
```bash
curl "https://api.wanikani.com/v2/user" \
  -H "Wanikani-Revision: 20170710" \
  -H "Authorization: Bearer <api_token_here>"
```
#### Response
```json
{
  "object": "user",
  "url": "https://api.wanikani.com/v2/user",
  "data_updated_at": "2018-04-06T14:26:53.022245Z",
  "data": {
    "id": "5a6a5234-a392-4a87-8f3f-33342afe8a42",
    "username": "example_user",
    "level": 5,
    "profile_url": "https://www.wanikani.com/users/example_user",
    "started_at": "2012-05-11T00:52:18.958466Z",
    "current_vacation_started_at": null,
    "subscription": {
      "active": true,
      "type": "recurring",
      "max_level_granted": 60,
      "period_ends_at": "2018-12-11T13:32:19.485748Z"
    },
    "preferences": {
      "default_voice_actor_id": 1,
      "extra_study_autoplay_audio": false,
      "lessons_autoplay_audio": false,
      "lessons_batch_size": 10,
      "lessons_presentation_order": "ascending_level_then_subject",
      "reviews_autoplay_audio": false,
      "reviews_display_srs_indicator": true,
      "reviews_presentation_order": "shuffled"
    }
  }
}
```

## Database tables
### words
```sql
INSERT INTO words (id, word_level, japanese, kana, romaji, english) VALUES
(7657, 'WK_1', 'こんにちは', 'こんにちは', 'Konnichiwa', 'Hello'),
(7658, 'WK_6', '亀', 'カメ', 'Kame', 'Turtle'),
(7659, 'WK_37', '日', 'ひ', 'Hi', 'Day')
```

### kanji
```sql
INSERT INTO kanji (id, kanji_level, symbol, meanings, primary_reading, primary_reading_type) VALUES
(248, 'WK_3', '和', 'Japan', 'わ', 'onyomi'),
(249, 'WK_53', '人', 'Person|People|Human', 'ひと', 'kunyomi'),
(250, 'WK_27', '子', 'Child|Kid', 'こ', 'kunyomi')
```

## Requirements
- Convert data from Wanikani API to SQLite script
- Must use Python
- No backend/frontend, just an import tool
- Must have unit test coverage that mocks the Wanikani API
- Must handle pagination of the Wanikani API
- Must handle errors from the Wanikani API
- Must handle rate limiting from the Wanikani API
- Only import kanji and words
- Only request subjects at the current user's level or below
- Only import kanji and words that are not hidden

## Wanikani constraints
- Levels are 1-60

## Technology
- Python 3.10
- SQLite
- Unit testing with pytest
