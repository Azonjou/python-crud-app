from fastapi import FastAPI, HTTPException, Request, Form
from pydantic import BaseModel
from starlette import status
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

#Настройка Jinja2 и статических файлов
templates = Jinja2Templates(directory="app/templates") # указывает где искать html шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static") # подключает папку с css

#Модель для вхордных данных (запросов: создание и обновление)
class MessageCreate(BaseModel):
    content: str

#Модель для ответов и хранение в базе данных
class Message(BaseModel):
    id: int
    content: str

#Инициализируем messages_db как список объектов Message
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
        if message.id == message_id:
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

@app.get("/web/messages", response_class=HTMLResponse)  # response_model=HTMLResponse указывает фастапи, что ответ должен быть html a ne json
async def get_messages_page(request: Request):
    """ Рендерит шаблон index.html. передавая ему объект request,
     необходимый для jinja2, и список messages_db как переменную messages
     """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"messages": message_db},
    )

#Страница создания сообщенеия
@app.get("/web/messages/create", response_class=HTMLResponse)
async def get_create_message_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
    )

@app.post("/web/messages", response_class=HTMLResponse)
async def create_message(request: Request, content: str = Form(...)):
    # Генерируем новый ID на основе максимального существующего
    next_id = max((msg.id for msg in message_db), default=-1) + 1
    new_message = Message(id = next_id, content = content)
    message_db.append(new_message)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"messages": message_db},
    )

@app.get("/web/messages/{message_id}", response_class=HTMLResponse)
async def read_message(request: Request, message_id: int):
    for message in message_db:
        if message_id == message.id:
            return templates.TemplateResponse(
                request=request,
                name="detail.html",
                context={"message": message},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

@app.post("/web/messages/{message_id}", response_class=HTMLResponse)
async def update_web_message(request: Request, message_id: int, content: str = Form(...)):
    for message in message_db:
        if message.id == message_id:
            new_message = Message(id=message_id, content = content)
            message_db[message_id] = new_message
            return templates.TemplateResponse(
                request=request,
                name="detail.html",
                context={"message": new_message},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

























