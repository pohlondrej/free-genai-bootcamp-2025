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
- What models should I actually use for FAQ generation?
    - Answer: Copilot suggest playing with t5-small. Never heard of it. What is it?
        - Answer: It's a really small model, which is apparently really good for text-to-text use cases.
- "No module named comps"
    - 'comps' is not installed, add it to requirements.
        - Oh wait, there is no 'comps'. It has to be 'opea-comps'. Of course.
- Error 500: Field required [type=missing, input_value=FormData([]), input_type=FormData]
    - Need more complex prompt. For example: 
```curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "messages=[{\"role\": \"user\", \"content\": \"Summarize this document\"}]" \
  -F "files=@document.pdf" \
  http://localhost:8000/
```
- AttributeError: 'str' object has no attribute 'content'
    - The error AttributeError: 'str' object has no attribute 'content' arises because the request.form() method returns a dictionary where the values are strings.