# Technical Specifications
## Business Goal
## Technical Requirements
- The backend will be built using Ktor
- The database will be SQLite3
- The API will always return JSON
- There will be no authentication or authorization
- Everything will be treated as a single user
## Database Schema
There will be the following tables:
- words - stored vocabulary words
    - id integer
    - japanese string
    - romaji string
    - english string
    - parts json
- word_groups - join table for words and groups, many-to-many
    - id integer
    - word_id integer
    - group_id integer
- groups - thematic groups of words
    - id integer
    - name string
- study_sessions - records of study sessions grouping word_review_items
    - id integer
    - group_id integer
    - created_at datetime
    - study_activity_id integer
- study_activities - a specific study activity, linking a study session to group
    - id integer
    - study_session_id integer
    - group_id integer
    - created_at datetime
- word_review_items - a record of word practice, determining if the word was correct or not
    - word_id integer
    - study_session_id integer
    - correct boolean
    - created_at datetime

### API Endpoints
#### GET `/api/words`
- pagination with 100 items per page
##### JSON Response
```json
{
  "items": [
    {
      "japanese": "こんにちは",
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
    "items_per_page": 100
  }
}
```
#### GET `/api/words/:id`
##### JSON Response
```json
{
  "id": 1,
  "japanese": "こんにちは",
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
#### GET `/api/groups`
- pagination with 100 items per page
##### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "name": "Basic Greetings",
      "word_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 10,
    "items_per_page": 100
  }
}
```
#### GET `/api/groups/:id`
##### JSON Response
```json
{
  "id": 1,
  "name": "Basic Greetings",
  "stats": {
    "total_word_count": 20
  }
}
```
#### GET `/api/groups/:id/words`
- pagination with 100 items per page
##### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "japanese": "こんにちは",
      "romaji": "konnichiwa",
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 3
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 10,
    "items_per_page": 100
  }
}
```
#### GET `/api/groups/:id/study_sessions`
##### JSON Response
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
    "items_per_page": 100
  }
}
```
#### GET `/api/dashboard/last_study_session`
##### JSON Response
```json
{
  "id": 1,
  "group_id": 1,
  "created_at": "2022-01-01T00:00:00Z",
  "study_activity_id": 1
}
```
#### GET `/api/dashboard/study_progress`
- The frontend will calculate the progress bar based on words studied out of total available words.
##### JSON Response
```json
{
  "total_words_studied": 20,
  "total_available_words": 100
}
```
#### GET `/api/dashboard/quick_stats`
##### JSON Response
```json
{
  "success_rate": 90.0,
  "total_study_sessions": 5,
  "total_active_groups": 4,
  "study_streak_days": 10
}
```
#### GET `/api/study_activities`
##### JSON Response
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
#### GET `/api/study_activities/:id`
##### JSON Response
```json
{
  "id": 1,
  "name": "Vocabulary Quiz",
  "thumbnail_url": "https://example.com/thumbnail.jpg",
  "description": "Lorem Ipsum Bla Bla Bla"
}
```
#### GET `/api/study_activities/:id/study_sessions`
##### JSON Response
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
#### GET `/api/study_sessions`
- pagination with 100 items per page
##### JSON Response
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
#### GET `/api/study_sessions/:id`
##### JSON Response
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
#### GET `/api/study_sessions/:id/words`
- pagination with 100 items per page
##### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "japanese": "こんにちは",
      "romaji": "konnichiwa",
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 3
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 20,
    "items_per_page": 100
  }
}
```
#### GET `/api/settings`
##### JSON Response
```json
{
  "language": "Japanese",
  "study_mode": "Flashcards",
  "daily_goal": 50,
  "notification_enabled": true
}
```
#### POST `/api/study_activities`
##### Request params:
- group_id integer
- study_activity_id integer
##### JSON Response
```json
{
  "id": 323,
  "group_id": 12
}
```
#### POST `/api/reset_history`
##### JSON Response
```json
{
  "success": true,
  "message": "Study history has been reset"
}
```
#### POST `/api/full_reset`
##### JSON Response
```json
{
  "success": true,
  "message": "System has been fully reset"
}
```
#### POST `/api/study_sessions/:id/words/:word_id/review`
##### Request params:
- id (study session id) integer
- word_id integer
- correct boolean
##### Request Payload
```json
{
  "correct": true
}
```
##### JSON Response
```json
{
  "success": true,
  "word_id": 1,
  "study_session_id": 23,
  "correct": true,
  "created_at": "2022-01-01T00:20:00Z"
}
```