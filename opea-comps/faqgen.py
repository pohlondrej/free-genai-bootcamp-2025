from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel
import torch
import os

app = FastAPI()

# Load model and tokenizer
MODEL_NAME = os.getenv("HF_MODEL_NAME", "bert-base-uncased")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()  # Set to evaluation mode
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

class InputText(BaseModel):
    text: str

@app.post("/generate")
async def generate(input_text: InputText):
    try:
        inputs = tokenizer(input_text.text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        # Process the outputs (replace with your actual logic)
        mean_output = outputs.last_hidden_state.mean().item()
        return {"result": mean_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)