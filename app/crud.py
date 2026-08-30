from ast import List

from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from starlette import status

app = FastAPI()

class MessageCreate(BaseModel):
    content: str

class Message(BaseModel):
    id: int
    content: str

message_db: list[Message] = [Message(id=0, content="First post in FastAPI")]

@app.get("/messages", response_model=list[Message])
async def read_messages() -> list[Message]:
    return message_db

@app.get("/messages/{message_id}", response_model=Message)
async def read_message(message_id: int) -> Message:
    for message in message_db:
        if message_id == message.id:
            return message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

@app.post("/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(message_create: MessageCreate) -> Message:
    # Генерируем новый ID на основе максимального существующего
    next_id = max((msg.id for msg in message_db), default=-1) + 1
    new_message = Message(id = next_id, content = message_create.content)
    message_db.append(new_message)
    return new_message

@app.put("/messages/{message_id}", status_code=status.HTTP_200_OK, response_model=Message)
async def update_message(message_id: int, message_create: MessageCreate) -> Message:
    for i, message in enumerate(message_db):
        if message.id == message.id:
            new_message = Message(id=message_id, content = message_create.content)
            message_db[i] = new_message
            return new_message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

@app.delete("/messages/{message_id}", status_code=status.HTTP_200_OK)
async def delete_message(message_id: int) -> dict:
    for i, message in enumerate(message_db):
        if message.id == message_id:
            message_db.pop(i)
            return {"detail": f"Message ID={message_id} deleted!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

@app.delete("/messages", status_code=status.HTTP_200_OK)
async def delete_messages() -> dict:
    message_db.clear()
    return {"detail": "All messages deleted!"}