from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI(title="PyKV Secure Store")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# STORAGE
users = {}
store = {}

# MODELS
class UserRegister(BaseModel):
    username: str
    password: str

class KeyValue(BaseModel):
    key: str
    value: str

# JWT CONFIG
SECRET_KEY = "pykv-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/register")
def register(user: UserRegister):
    if user.username in users: raise HTTPException(400, "User exists")
    users[user.username] = user.password
    return {"message": "Success"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if users.get(form_data.username) != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_token(form_data.username), "token_type": "bearer"}

@app.post("/set")
def set_val(kv: KeyValue, user: str = Depends(get_current_user)):
    store[kv.key] = kv.value
    return {"message": "Stored"}

@app.get("/list")
def list_all(user: str = Depends(get_current_user)):
    return store

@app.get("/get/{key}")
def get_val(key: str, user: str = Depends(get_current_user)):
    val = store.get(key)
    if val is None: raise HTTPException(404, "Not found")
    return {"key": key, "value": val}

@app.delete("/delete/{key}")
def del_val(key: str, user: str = Depends(get_current_user)):
    if key in store:
        del store[key]
        return {"message": "Deleted"}
    raise HTTPException(404, "Not found")