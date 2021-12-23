from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional
from random import randrange
app = FastAPI()

class post(BaseModel):
    title:str
    body:str
    publish:bool = True
    # rating:Optional[int] = None


my_post = [{'title':"this is first post",'body':'this is body','id':1},
{'title':"this is second post",'body':'this is second body','id':2}]

def getpost(id):
    for i in my_post:
        if i['id']==int(id):
            return i

def deletepost(id):
    for i,p in enumerate(my_post):
        if p['id']== id:
            return i


@app.get("/")
def root():
    return {"message": "this is my first blog"}


# @app.post("/create")
# def createpost(payload:dict=Body(...)):
#     print(payload)
#     return {"mess":f"title:{payload['title']} , body:{payload['body']}"}


# @app.post("/create")
# def createpost(payload:post):
#     print(payload)
#     print(payload.dict())
#     return {"mess":payload}

@app.post("/create",status_code=status.HTTP_201_CREATED)
def createpost(payload:post):
    post_id=payload.dict()
    post_id['id']=randrange(1,10)
    my_post.append(post_id)
    return {"mess":post_id}



@app.get("/post/{id}")
def get_post(id:int):
    post = getpost(id)
    if not post:
        # response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="not found")
    return {"message":post }


@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = deletepost(id)
    if index == None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="not found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def update_post(id:int,post:post):
    index = deletepost(id)
    if index == None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="not found")
    postupdate = post.dict()
    postupdate['id']=id
    my_post[index]=postupdate
    return {'message':postupdate}