from __future__ import annotations
from typing import Union, List, Dict
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


chatrooms = {}

class Chatroom:
    def __init__(self, desc: str, room_name: str):
        self.desc = desc
        self.room_name = room_name
        self.users = [User]
        self.messages = []

class User:
    def __init__(self, userId: int, name: str):
        self.userId = userId
        self.name = name

class Message:
    def __init__(self, content: str, user: User):
        self.content = content
        self.user = user

# Create a chatroom
@app.post("/chatrooms", status_code=status.HTTP_201_CREATED)
def create_chatroom(name: str, description: str = ""):
    if name in chatrooms:
        raise HTTPException(status_code=400, detail="Chatroom already exists")
    
    chatrooms[name] = Chatroom(name, description)
    return("Chatroom created")
    
# List Chatrooms
@app.get("/chatrooms")
def get_chatrooms():
    return list(chatrooms)


# Send a message
@app.post("/chatrooms/{chatroom_name}/messages", status_code=status.HTTP_201_CREATED)
def post_message(chatroom_name: str, sender: str, message: str):
    if chatroom_name not in chatrooms:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    
    chatrooms[chatroom_name].messages.append((sender, message))
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
