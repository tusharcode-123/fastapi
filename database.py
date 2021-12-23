from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI,Response,status,HTTPException
import psycopg2
import time
from psycopg2.extras import RealDictCursor
app = FastAPI()


class post(BaseModel):
    title:str
    body:str
    publish:bool = True
 

while True:
    try:
        conn = psycopg2.connect(host='localhost', user='postgres',database='fastapi',password="tyuiop@123",cursor_factory=RealDictCursor)
        
        cur = conn.cursor()
        print("database connect success")
        break
    except Exception as error:
        print("error occurs")
        time.sleep(2)



@app.get("/")
def root():
    return {"message": "this is my first blog"}


@app.get("/post")
def get_post():
    cur.execute("""SELECT * FROM post""")
    my_post= cur.fetchall()
    return {"message": my_post}

@app.post("/create",status_code=status.HTTP_201_CREATED)
def createpost(post:post):
    cur.execute(""" insert into post (title,body,publish) values (%s,%s,%s) RETURNING *""",(post.title,post.body,post.publish))
    post_id = cur.fetchone()
    conn.commit()
    return {"mess":post_id}


@app.get("/post/{id}")
def get_post(id:int):
    cur.execute(""" select * from post where id = %s""",(str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="not found")
    return {"message":post }

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cur.execute(""" delete from post where id = %s RETURNING *""",(str(id),))
    index = cur.fetchone()
    conn.commit()
    if index == None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def update_post(id:int,post:post):
    cur.execute(""" update post set title = %s , body = %s , publish = %s where id = %s RETURNING *""",(post.title,post.body,post.publish,str(id)))
    index = cur.fetchone()
    conn.commit()
    if index == None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="not found")
    return {'message':index}