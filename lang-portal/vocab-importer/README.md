# Vocabulary Importer

A tool to import kanji and vocabulary from Wanikani into SQLite format for the language portal.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Wanikani API key as an environment variable (optional):
```bash
export WANIKANI_API_KEY='your-api-key-here'
```

## Usage

### As a Command Line Tool

Run the importer to generate a migration file:
```bash
python main.py
```

This will:
1. Fetch kanji and vocabulary from Wanikani API
2. Filter items based on your current level
3. Generate a `migration.sql` file in the current directory

### As a Module

You can also use the importer as a module in your Python code:

```python
from vocab_importer.main import import_vocabulary

# Basic usage (uses WANIKANI_API_KEY environment variable)
result = import_vocabulary()

# Specify API key and output directory
result = import_vocabulary(
    api_key='your-api-key-here',
    output_dir='/path/to/output'
)

# The result contains import statistics
print(f"Imported {result['kanji_count']} kanji")
print(f"Imported {result['vocab_count']} vocabulary items")
print(f"User level: {result['user_level']}")
print(f"Migration file: {result['output_file']}")
```

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
