# Vocabulary Importer

A tool to import kanji and vocabulary from Wanikani into SQLite format for the language portal.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Wanikani API key as an environment variable:
```bash
export WANIKANI_API_KEY='your-api-key-here'
```

## Usage

Run the importer to generate a migration file:
```bash
python main.py
```

This will:
1. Fetch kanji and vocabulary from Wanikani API
2. Filter items based on your current level
3. Generate a `migration.sql` file with the SQL statements

## Development

### Running Tests

Run all tests:
```bash
python -m pytest test/ -v
```

Run a specific test file:
```bash
python -m pytest test/test_data_processor.py -v
```
