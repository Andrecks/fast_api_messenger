# import uvicorn
from fastapi import FastAPI, Body, Depends

from db_control import db_control
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
import phonenumbers
import uvicorn

db_class = db_control()

app = FastAPI()



def verify_phone_number(phone_number: str) -> bool:
    try:
        parsed_number = phonenumbers.parse(phone_number)
        return phonenumbers.is_valid_number(parsed_number) and phonenumbers.is_possible_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

# route handlers

# testing
@app.get("/", tags=["test"])
def greet():
    return {"hello": "world!."}


# # Get Posts
# @app.get("/posts", tags=["posts"])
# def get_posts():
#     return { "data": posts }


@app.get("/posts/{id}", tags=["posts"])
def get_single_post(id: int):
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }


@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    
    if db_class.check_user_exists(user.phone):
        return {
        "error": "указанный номер телефона уже зарегестрирован"
        }
    
    if verify_phone_number(user.phone):
        # users.append(user) # replace with db call, making sure to hash the password first
        return signJWT(user.phone)
    return {
        "error": "номер телефона указан некорректно"
    }
        


@app.post("/user/login", tags=["user"])
def user_login(user: UserSchema = Body(...)):
    if check_user(user.phone):
        return signJWT(user.phone)
    return {
        "error": "Wrong login details!"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", log_level="info", reload=True)