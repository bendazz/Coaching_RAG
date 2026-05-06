import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
import chromadb
from google import genai

load_dotenv()
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
chroma_client = chromadb.PersistentClient("./chroma_db")

collections = {}
for name in ["opponents_2026", "roster_2026", "scouting_2027"]:
    collections[name] = chroma_client.get_collection(name)

class Question(BaseModel):
    question: str
    collection: Literal["opponents_2026", "roster_2026", "scouting_2027"]

app = FastAPI()

@app.post("/ask")
def ask(payload: Question):
    collection = collections[payload.collection]
    results = collection.query(query_texts=[payload.question], n_results=8)
    chunks = results["documents"][0]

    context = "\n\n".join(chunks)
    prompt = f"""Answer the coach's question using only the context below.
If the answer is not in the context, say so plainly.

Context:
{context}

Question: {payload.question}"""

    response = gemini_client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt,
    )

    return response.text


app.mount("/", StaticFiles(directory="static", html=True), name="static")