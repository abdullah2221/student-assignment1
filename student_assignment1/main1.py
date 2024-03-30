from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from concurrent.futures import ProcessPoolExecutor  # For thread safety

app = FastAPI()

executor = ProcessPoolExecutor()  # Create a thread pool

class Book(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())) 
    title: str
    author: str
    publisher: str

book_data:dict = {}  # Can be replaced with a persistent storage solution

@app.post("/book")
async def add_book(book: Book):
    async def add_book_async():
        if book.id in book_data:
            raise HTTPException(status_code=409, detail="Book with this ID already exists")
        book_data[book.id] = book
        return book

    return await executor.submit(add_book_async)  # type: ignore[misc]

@app.get("/book")
async def get_books():
    async def get_books_async():
        return list(book_data.values())

    return await executor.submit(get_books_async)  # Submit task to thread pool
