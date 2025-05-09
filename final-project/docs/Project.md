# Project Specification

## Business Overview
The language learning school wants to provide a platform for their students to practice their Japanese language skills. To keep things interesting and engaging, the school wants to use AI/LLM to generate random Japanese sentences and provide feedback on their performance. The school is planning to make the platform public and allow other schools to use it as well, which requires a modular, scalable, and extensible architecture.

## Design Overview
Project should follow a modular architecture:

```
project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── games/
│   │   └── ...
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/
│   │   │   └── ...
│   │   └── ...
│   ├── Dockerfile
│   └── angular.json
├── modules/
│   ├── onboarding/
│   │   ├── backend/
│   │   ├── frontend/
│   └── ...
├── plugins/
│   ├── example-plugin/
│   │   ├── backend/
│   │   │   ├── app/
│   │   │   │   ├── __init__.py
│   │   │   │   └── api.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   ├── frontend/
│   │   │   ├── src/
│   │   │   │   ├── component.ts
│   │   │   │   ├── module.ts
│   │   │   │   └── ...
│   │   │   ├── Dockerfile
│   │   │   └── angular.json
│   │   └── docker-compose.yml
│   └── ...
├── docker-compose.yml
└── README.md
```

- Each plugin should have a self-contained backend and frontend, allowing for easy deployment and extensibility.
- A "plugin" is essentially a study activity.

## Technology Stack
### Backend
- Python
- FastAPI
- SQLite

### Frontend
- Angular

### AI/LLM
- Ollama
- Gemini API

## Ports
- 80: NGINX
- 8000: Core API
- 8001: Crawler API
- 8002: Flashcards API
- 8003: DuoRadio API
- 4200: Core Frontend