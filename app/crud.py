from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from starlette import status

app = FastAPI()

message_db = {0: "First post in FastAPI"}
@app.get("/messages")
async def read_messages() -> dict:
    return message_db

@app.get("/messages/{message_id}")
async def read_message(message_id: int) -> str:
    try:
        return message_db[message_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Message not found")

@app.post("/messages", status_code=status.HTTP_201_CREATED)
async def create_message(message: str = Body(...)) -> str:
    current_index = max(message_db) + 1 if message_db else 0
    message_db[current_index] = message
    return "Message created!"


@app.put("/messages/{message_id}", status_code=status.HTTP_200_OK)
async def update_message(message_id: int, message: str = Body(...)) -> str:
    if message_id not in message_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    message_db[message_id] = message
    return "Message updated!"

@app.delete("/messages/{message_id}", status_code=status.HTTP_200_OK)
async def delete_message(message_id: int) -> str:
    if message_id not in message_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    message_db.pop(message_id)
    return f"Message ID={message_id} deleted!"

@app.delete("/messages", status_code=status.HTTP_200_OK)
async def delete_messages() -> str:
    message_db.clear()
    return "All messages deleted!"