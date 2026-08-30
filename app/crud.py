from ast import List

from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from starlette import status

app = FastAPI()

class Message(BaseModel):
    id: int
    content: str

message_db: list[Message] = [Message(id=0, content="First post in FastAPI")]

@app.get("/messages", response_model=List[Message])
async def read_messages() -> list[Message]:
    return message_db

@app.get("/messages/{message_id}", response_model=Message)
async def read_message(message_id: int) -> Message:
    for message in message_db:
        if message_id == message.id:
            return message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

@app.post("/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(message: Message) -> Message:
    if any(msg.id == message.id for msg in message_db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message already exists")
    message_db.append(message)
    return message

@app.put("/messages/{message_id}", status_code=status.HTTP_200_OK, response_model=Message)
async def update_message(message_id: int, message: Message) -> Message:
    if message.id != message_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The ID in the request does not match the ID in the message")
    for i, message in enumerate(message_db):
        if message.id == message.id:
            message_db[i] = message
            return message
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