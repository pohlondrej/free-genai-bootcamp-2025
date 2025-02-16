# OPEA Comps - FAQGen
## Business Goal
Our company wants to automate FAQ creation from documentation and support data. This will reduce repetitive inquiries, improve customer satisfaction with instant answers, and the our support team to handle complex issues, boosting efficiency. The solution needs to use Docker, so that it can be easily deployed both locally and in various cloud services.

## Technical Uncertainties
- What are the technical requirements on CPU and GPU?
- What input formats are supported? PDF, websites, SQLite database files, videos, ...?
- How large models are required for adequate output?
- Is fine-tuning going to be required?
- How will the solution integrate to existing company systems?
- How can we prevent possible data breaches, e.g. if some users upload classified documents?

## Q&A
- What models do I need? Where do I find them on HuggingFace?
- Incorrect path_or_model_id: ''. Please provide either the path to a local folder or the repo_id of a model on the Hub.
    - Answer: missing environment variables in the Dockerfile
- `docker run -p 8000:8000 -e HF_MODEL_NAME="bert-base-uncased" faqgen` gives "404 not found" error
    - Answer: wrong endpoint; should have accessed http://localhost:8000/generate (which actually worked, so now I have a Bert model running in a container...sweet!)