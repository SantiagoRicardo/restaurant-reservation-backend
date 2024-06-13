from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
import crud
from schemas import ReservationCreate, Reservation, UserCreate, User
from datetime import datetime, timedelta
from typing import List

# Configuración
SECRET_KEY = "svddfd$%sdc51856"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(email: str):
    user = crud.get_user_by_email(email)
    return user

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user or not verify_password(password, user['password']):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email=email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.rol == "cliente":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires

    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    user.password = get_password_hash(user.password)
    return crud.create_user(user)

@app.post("/reservations/", response_model=Reservation)
def create_reservation_endpoint(reservation: ReservationCreate):
    result = crud.create_reservation(reservation.model_dump())
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/reservations/{reservation_id}", response_model=Reservation)
def read_reservation_endpoint(reservation_id: int):
    reservation = crud.get_reservation(reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@app.get("/reservations/", response_model=List[Reservation])
def read_reservations_endpoint(skip: int = 0, limit: int = 10):
    reservations = crud.get_reservations(skip=skip, limit=limit)
    return reservations

@app.put("/reservations/{reservation_id}", response_model=Reservation)
def update_reservation_endpoint(reservation_id: int, reservation: ReservationCreate, current_user: User = Depends(get_current_active_user)):
    if current_user.rol not in ["gerente", "empleado"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated_reservation = crud.update_reservation(reservation_id, reservation.dict())
    if updated_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return updated_reservation

@app.delete("/reservations/{reservation_id}")
def delete_reservation_endpoint(reservation_id: int, current_user: User = Depends(get_current_active_user)):
    if current_user.rol != "gerente":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    reservation = crud.delete_reservation(reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation
