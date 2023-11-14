from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
# from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='Cybesco19952023', cursor_factory=RealDictCursor)
        cursor = conn.cursor
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connection todatabase failed")
        print("Error: ", error)
        time.sleep(2)


my_posts = [
    {
        "title": "title of posts 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "favorite food",
        "content": "i like pizza",
        "id": 2
    }
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to my Api"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


# @app.post("/createposts")
# async def create_posts(payload=Body(...)):
#     print(payload)
#     return {
#         "new_posts": payload['title'],
#         "content": payload['content']
#     }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(dto: Post):
    # print(dto.rating)
    print(dto)
    # return {
    #     "data": "new post"
    # }
    dto_dict = dto.model_dump()
    dto_dict["id"] = randrange(0, 1000000)
    my_posts.append(dto_dict)
    return {
        "data": dto_dict
    }


# @app.get("/posts/latest")
# async def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    # print(type(id))
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not fund"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not fund")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist.")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, dto: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist.")

    post_dict = dto.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}
