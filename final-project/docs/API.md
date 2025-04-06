# API Endpoints
## GET `/api/words`
- pagination with 30 items per page
### JSON Response
```json
{
  "items": [
    {
      "word_level": "N1",
      "japanese": "こんにちは",
      "kana": "こんにちは",
      "romaji": "konnichiwa",
      "english": "hello",
      "correct_count": 3,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 2,
    "total_items": 200,
    "items_per_page": 30
  }
}
```
## GET `/api/words/:id`
### JSON Response
```json
{
  "id": 1,
  "word_level": "N1",
  "japanese": "こんにちは",
  "kana": "こんにちは",
  "romaji": "konnichiwa",
  "english": "hello",
  "stats": {
    "correct_count": 3,
    "wrong_count": 2
  },
  "groups": [
    {
      "id": 1,
      "name": "Basic Greetings"
    }
  ]
}
```
## GET `/api/kanji/`
### JSON Response
```json
{
  "items": [
    {
      "kanji_level": "N1",
      "symbol": "大",
      "primary_reading": "たい",
      "primary_meaning": "big",
      "correct_count": 3,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 2,
    "total_items": 200,
    "items_per_page": 30
  }
}
```
## GET `/api/kanji/:id`
### JSON Response
```json
{
  "id": 1,
  "symbol": "大",
  "kanji_level": "N1",
  "primary_reading": "たい",
  "primary_reading_type": "onyomi",
  "primary_meaning": "big",
  "stats": {
    "correct_count": 3,
    "wrong_count": 2
  },
  "groups": [
    {
      "id": 1,
      "name": "Wanikani Level 1"
    }
  ]
}
```
## GET `/api/groups`
- pagination with 30 items per page
### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "name": "Basic Greetings",
      "item_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 10,
    "items_per_page": 30
  }
}
```
## GET `/api/groups/:id`
### JSON Response
```json
{
  "id": 1,
  "name": "Basic Greetings",
  "stats": {
    "total_item_count": 20
  }
}
```
## GET `/api/groups/:id/items`
- pagination with 30 items per page
### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "type": "word",
      "japanese": "こんにちは",
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 3
    },
    {
      "id": 32,
      "type": "kanji",
      "japanese": "大",
      "english": "big",
      "correct_count": 2,
      "wrong_count": 10
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 100,
    "items_per_page": 30
  }
}
```
## GET `/api/groups/:id/study_sessions`
- pagination with 30 items per page
### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2022-01-01T00:00:00Z",
      "end_time": "2022-01-01T00:20:00Z",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 5,
    "items_per_page": 30
  }
}
```
## GET `/api/dashboard/last_study_session`
### JSON Response
```json
{
  "id": 1,
  "group_id": 1,
  "activity_name": "Vocabulary Quiz",
  "created_at": "2022-01-01T00:00:00Z",
  "correct_count": 1,
  "wrong_count": 3
}
```
## GET `/api/dashboard/study_progress`
- The frontend will calculate the progress bar based on words studied out of total available words.
### JSON Response
```json
{
  "total_words_studied": 20,
  "total_available_words": 100
}
```
## GET `/api/dashboard/quick_stats`
### JSON Response
```json
{
  "success_rate": 90.0,
  "total_study_sessions": 5,
  "total_active_groups": 4,
  "study_streak_days": 10
}
```
## GET `/api/study_activities`
### JSON Response
```json
[
  {
    "id": 1,
    "study_session_id": 1,
    "group_id": 1,
    "created_at": "2022-01-01T00:00:00Z"
  }
]
```
## GET `/api/study_activities/:id`
### JSON Response
```json
{
  "id": 1,
  "name": "Vocabulary Quiz",
  "thumbnail_url": "https://example.com/thumbnail.jpg",
  "description": "Lorem Ipsum Bla Bla Bla"
}
```
## GET `/api/study_activities/:id/study_sessions`
### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2022-01-01T00:00:00Z",
      "end_time": "2022-01-01T00:20:00Z",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "items_per_page": 20
  }
}
```
## GET `/api/study_sessions`
- pagination with 30 items per page
### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2022-01-01T00:00:00Z",
      "end_time": "2022-01-01T00:20:00Z",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 30,
    "items_per_page": 20
  }
}
```
## GET `/api/study_sessions/:id`
### JSON Response
```json
{
  "id": 1,
  "activity_name": "Vocabulary Quiz",
  "group_name": "Basic Greetings",
  "start_time": "2022-01-01T00:00:00Z",
  "end_time": "2022-01-01T00:20:00Z",
  "review_items_count": 20
}
```
## GET `/api/study_sessions/:id/items`
- pagination with 30 items per page
### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "type": "word",
      "japanese": "こんにちは",
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 3
    },
    {
      "id": 32,
      "type": "kanji",
      "japanese": "大",
      "english": "big",
      "correct_count": 2,
      "wrong_count": 10
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 20,
    "items_per_page": 30
  }
}
```
## GET `/api/settings`
### JSON Response
```json
{
  "language": "Japanese",
  "study_mode": "Flashcards",
  "daily_goal": 50,
  "notification_enabled": true
}
```
## POST `/api/study_activities`
### Request params:
- group_id integer
- study_activity_id integer
### JSON Response
```json
{
  "id": 323,
  "group_id": 12
}
```
## POST `/api/reset_history`
### JSON Response
```json
{
  "success": true,
  "message": "Study history has been reset"
}
```
## POST `/api/full_reset`
### JSON Response
```json
{
  "success": true,
  "message": "System has been fully reset"
}
```
