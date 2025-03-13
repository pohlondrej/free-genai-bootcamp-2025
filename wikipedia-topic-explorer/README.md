# Wikipedia Topic Explorer and Japanese Vocabulary Builder

This app is a demonstration of AI agentic workflow. It will create short, informative summaries about any given topic in Japanese, along with a vocabulary list of key terms used in the summary.

## Features

- Generate summaries of Wikipedia articles in Japanese
- Generate vocabulary lists of key terms used in the summary
- Crawl the web for images related to the topic

## Technical Documentation
For detailed technical specifications and architecture, see [Project Documentation](docs/Project.md).

## Workflow

1. User provides a topic in English
2. App uses Wikipedia API to fetch the article in English
3. LLM simplifies the article to the point a 9-year-old could understand
4. LLM translates the simplified article into Japanese, using only JLPT N5 vocabulary, grammar and Kanji
5. LLM generates a vocabulary list of key terms used in the summary
6. App crawls the web (using DuckDuckGo API) for images related to the topic
7. App presents the summary, vocabulary list, kanji list, and images to the user in the frontend

## Setup
TODO

## Usage
TODO