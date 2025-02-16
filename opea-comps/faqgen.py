from fastapi import FastAPI, Request, UploadFile, File
from comps.cores.proto.api_protocol import ChatCompletionRequest, ChatCompletionResponse, ChatCompletionResponseChoice, ChatMessage, UsageInfo
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List, Dict, Any
import torch
import os
import uvicorn
import json
from io import BytesIO
import pdfminer.high_level
from pdfminer.pdfparser import PDFSyntaxError

# Initialize FastAPI app
app = FastAPI()

# Assuming you have these loaded globally (as in the T5 example)
MODEL_NAME = os.getenv("HF_MODEL_NAME", "t5-small")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
model.eval()

async def read_pdf(file: UploadFile) -> str:
    """Extract text from a PDF file."""
    try:
        contents = await file.read()
        text = pdfminer.high_level.extract_text(BytesIO(contents))
        return text
    except PDFSyntaxError:
        return "Error: Could not decode PDF."
    except Exception as e:
        return f"Error reading PDF: {e}"

@app.post("/")
async def handle_request(request: Request, files: List[UploadFile] = File(default=None)):
    data: Dict[str, Any] = await request.form()
    messages_str = data.get('messages')
    messages = json.loads(messages_str)

    # Check the structure of the messages list
    print(f"Messages: {messages}")  # Print the messages list

    # Create ChatMessage objects from the dictionaries
    chat_messages = [ChatMessage(**msg) for msg in messages]

    # Check the structure of the chat_messages list
    print(f"Chat Messages: {chat_messages}")  # Print the chat_messages list

    file_summaries = []

    if files:
        for file in files:
            if file.filename.lower().endswith(".pdf"):
                text = await read_pdf(file)
                file_summaries.append(f"PDF Content from {file.filename}: {text}")
            else:
                contents = await file.read()
                text = contents.decode("utf-8")
                file_summaries.append(f"Text Content from {file.filename}: {text}")
    prompt = chat_messages[0].content
    if file_summaries:
        prompt = prompt + "\n".join(file_summaries)

    input_text_processed = "Generate a list of frequently asked questions and their answers based on the following document: " + prompt
    inputs = tokenizer(input_text_processed, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=200)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    choices = [ChatCompletionResponseChoice(
        index=0,
        message=ChatMessage(role="assistant", content=generated_text),
        finish_reason="stop"
    )]
    usage = UsageInfo()
    return ChatCompletionResponse(model="faqgen", choices=choices, usage=usage)

# Run the app using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)