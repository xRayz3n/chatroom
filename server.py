from __future__ import annotations
from typing import Union, List, Dict, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


chatrooms = {}

class Message(BaseModel):
    sender: str = Field(...,example="ILuvUnicorns")
    message: str = Field(...,example="unicorns are amazing")
    
class Chatroom(BaseModel):
    name: str = Field(...,example="Unicorn enthusiasts")
    description: Optional[str] = Field(None, example="Talk about your dream unicorn")
    messages: List[Message] = []


class Chatroom:
    def __init__(self, desc: str, room_name: str):
        self.desc = desc
        self.room_name = room_name
        self.messages = []

# Create a chatroom
@app.post("/chatrooms", status_code=status.HTTP_201_CREATED)
def create_chatroom(chatroom: Chatroom):
    if chatroom.name in chatrooms:
        raise HTTPException(status_code=400, detail="Chatroom already exists")
    
    chatrooms[chatroom.name] = chatroom
    return(f"Chatroom {chatroom.name} created")
    
# List Chatrooms
@app.get("/chatrooms")
def get_chatrooms():
    return list(chatrooms)


# Send a message
@app.post("/chatrooms/{chatroom_name}/messages", status_code=status.HTTP_201_CREATED)
def post_message(chatroom_name: str, message: Message):
    if chatroom_name not in chatrooms:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    
    chatrooms[chatroom_name].messages.append((message.sender, message.message))
    return {"detail": "Message added"}

# Get the list of messages
@app.get("/chatrooms/{chatroom_name}/messages")
def get_messages(chatroom_name: str):
    if chatroom_name not in chatrooms:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    return chatrooms[chatroom_name].messages

        


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
