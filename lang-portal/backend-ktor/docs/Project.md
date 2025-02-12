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
[
    {
        "id": 1,
        "japanese": "こんにちは",
        "romaji": "konnichiwa",
        "english": "hello",
        "parts": ["greeting"]
    }
]
```
#### GET `/api/words/:id`
##### JSON Response
```json
{
    "id": 1,
    "japanese": "こんにちは",
    "romaji": "konnichiwa",
    "english": "hello",
    "parts": ["greeting"]
}
```
#### GET `/api/groups`
- pagination with 100 items per page
##### JSON Response
```json
[
    {
      "id": 1,
      "name": "Greetings"
    }
]
```
#### GET `/api/groups/:id`
##### JSON Response
```json
{
    "id": 1,
    "name": "Greetings"
}
```
#### GET `/api/groups/:id/words`
- pagination with 100 items per page
##### JSON Response
```json
[
    {
        "id": 1,
        "japanese": "こんにちは",
        "romaji": "konnichiwa",
        "english": "hello",
        "parts": ["greeting"]
    }
]
```
#### GET `/api/groups/:id/study_sessions`
##### JSON Response
```json
[
    {
        "id": 1,
        "group_id": 1,
        "created_at": "2022-01-01T00:00:00Z",
        "study_activity_id": 1
    }
]
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
##### JSON Response
```json
{
    "total_words": 100,
    "learned_words": 50,
    "percentage_completed": 50
}
```
#### GET `/api/dashboard/quick_stats`
##### JSON Response
```json
{
    "total_study_sessions": 10,
    "correct_answers": 80,
    "incorrect_answers": 20
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
    "study_session_id": 1,
    "group_id": 1,
    "created_at": "2022-01-01T00:00:00Z"
}
```
#### GET `/api/study_activities/:id/study_sessions`
##### JSON Response
```json
[
    {
        "id": 1,
        "group_id": 1,
        "created_at": "2022-01-01T00:00:00Z",
        "study_activity_id": 1
    }
]
```
#### GET `/api/study_sessions`
- pagination with 100 items per page
##### JSON Response
```json
[
    {
        "id": 1,
        "group_id": 1,
        "created_at": "2022-01-01T00:00:00Z",
        "study_activity_id": 1
    }
]
```
#### GET `/api/study_sessions/:id`
##### JSON Response
```json
{
    "id": 1,
    "group_id": 1,
    "created_at": "2022-01-01T00:00:00Z",
    "study_activity_id": 1
}
```
#### GET `/api/study_sessions/:id/words`
##### JSON Response
```json
[
    {
        "word_id": 1,
        "japanese": "勉強",
        "romaji": "benkyō",
        "english": "study",
        "parts": {"part": "verb"},
        "correct": true,
        "created_at": "2023-01-01T12:00:00Z"
    }
]
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
#### POST `/api/study_activities(group_id, study_activity_id)`
#### POST `/api/reset_history`
#### POST `/api/full_reset`
#### POST `/api/study_sessions/:id/words/:word_id/review(correct)`