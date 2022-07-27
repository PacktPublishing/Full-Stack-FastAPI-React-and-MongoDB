from enum import Enum
from fastapi import FastAPI, Path

app = FastAPI()
class AccountType(str, Enum):
    FREE = "free"
    PRO = "pro"

@app.get("/account/{acc_type}/{months}")
async def account( acc_type:AccountType, months:int = Path(..., ge=3,le=12)):
    
    return {
            "message":"Account created",
            "account_type":acc_type,
            "months":months
            }
