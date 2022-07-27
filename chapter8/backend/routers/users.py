from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models import UserBase, LoginBase, CurrentUser

from authentication import AuthHandler

router = APIRouter()

# instantiate the Auth Handler
auth_handler = AuthHandler()

# register user
# validate the data and create a user if the username and the email are valid and available


@router.post("/register", response_description="Register user")
async def register(request: Request, newUser: UserBase = Body(...)) -> UserBase:

    # hash the password before inserting it into MongoDB
    newUser.password = auth_handler.get_password_hash(newUser.password)

    newUser = jsonable_encoder(newUser)

    # check existing user or email 409 Conflict:
    if (
        existing_email := await request.app.mongodb["users"].find_one(
            {"email": newUser["email"]}
        )
        is not None
    ):
        raise HTTPException(
            status_code=409, detail=f"User with email {newUser['email']} already exists"
        )

    # check existing user or email 409 Conflict:
    if (
        existing_username := await request.app.mongodb["users"].find_one(
            {"username": newUser["username"]}
        )
        is not None
    ):
        raise HTTPException(
            status_code=409,
            detail=f"User with username {newUser['username']} already exists",
        )

    user = await request.app.mongodb["users"].insert_one(newUser)
    created_user = await request.app.mongodb["users"].find_one(
        {"_id": user.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


# post user
@router.post("/login", response_description="Login user")
async def login(request: Request, loginUser: LoginBase = Body(...)) -> str:

    # find the user by email
    user = await request.app.mongodb["users"].find_one({"email": loginUser.email})

    # check password
    if (user is None) or (
        not auth_handler.verify_password(loginUser.password, user["password"])
    ):
        raise HTTPException(status_code=401, detail="Invalid email and/or password")
    token = auth_handler.encode_token(user["_id"])
    response = JSONResponse(
        content={"token": token, "user": CurrentUser(**user).dict()}
    )

    return response


# me route
@router.get("/me", response_description="Logged in user data")
async def me(request: Request, userId=Depends(auth_handler.auth_wrapper)):

    currentUser = await request.app.mongodb["users"].find_one({"_id": userId})
    result = CurrentUser(**currentUser).dict()
    result["id"] = userId

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
