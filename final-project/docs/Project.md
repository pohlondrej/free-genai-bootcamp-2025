# Project Specification

## Business Overview
// TODO

## Design Overview
Project should follow a modular architecture:

```
project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── plugins/
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

Each plugin should have a self-contained backend and frontend, allowing for easy deployment and extensibility.

## Technology Stack
### Backend
- Python
- FastAPI

### Frontend
- Angular

### AI/LLM
- Ollama
- Gemini API