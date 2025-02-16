from fastapi import FastAPI, Request, UploadFile, File
from comps.cores.proto.api_protocol import ChatCompletionRequest, ChatCompletionResponse, ChatCompletionResponseChoice, ChatMessage, UsageInfo
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List
import torch
import os
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Assuming you have these loaded globally (as in the T5 example)
MODEL_NAME = os.getenv("HF_MODEL_NAME", "t5-small")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
model.eval()

@app.post("/")
async def handle_request(request: Request, files: List[UploadFile] = File(default=None)):
    data = await request.form()
    chat_request = ChatCompletionRequest.parse_obj(data)
    file_summaries = []

    if files:
        for file in files:
            file_path = f"/tmp/{file.filename}"
            import aiofiles
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(await file.read())
            # Assuming read_text_from_file is defined elsewhere
            # docs = read_text_from_file(file, file_path)
            # os.remove(file_path)
            # if isinstance(docs, list):
            #     file_summaries.extend(docs)
            # else:
            #     file_summaries.append(docs)
            file_summaries.append(f"File {file.filename} processed.") # Placeholder

    if file_summaries:
        prompt = chat_request.messages[0].content + "\n".join(file_summaries) # Use the message content
    else:
        prompt = chat_request.messages[0].content # Use the message content

    try:
        input_text_processed = "generate faq: " + prompt  # Add a prompt
        inputs = tokenizer(input_text_processed, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=200)  # Generate text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        choices = [ChatCompletionResponseChoice(
            index=0,
            message=ChatMessage(role="assistant", content=generated_text),
            finish_reason="stop"
        )]
        usage = UsageInfo()  # You might want to calculate actual usage
        return ChatCompletionResponse(model="faqgen", choices=choices, usage=usage)

    except Exception as e:
        # Handle exceptions properly
        choices = [ChatCompletionResponseChoice(
            index=0,
            message=ChatMessage(role="assistant", content=f"Error: {str(e)}"),
            finish_reason="error"
        )]
        usage = UsageInfo()
        return ChatCompletionResponse(model="faqgen", choices=choices, usage=usage)

# Run the app using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)