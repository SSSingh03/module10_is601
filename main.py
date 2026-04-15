from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session
import uvicorn
import logging

from app.operations import add, subtract, multiply, divide
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# Templates
templates = Jinja2Templates(directory="templates")


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Calculator models
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator("a", "b")
    @classmethod
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Both a and b must be numbers.")
        return value


class OperationResponse(BaseModel):
    result: float


class ErrorResponse(BaseModel):
    error: str


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = "; ".join(
        [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    )
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(
        status_code=400,
        content={"error": error_messages}
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.error(f"ValueError on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )


# Routes
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/add", response_model=OperationResponse)
async def add_route(operation: OperationRequest):
    result = add(operation.a, operation.b)
    return {"result": result}


@app.post("/subtract", response_model=OperationResponse)
async def subtract_route(operation: OperationRequest):
    result = subtract(operation.a, operation.b)
    return {"result": result}


@app.post("/multiply", response_model=OperationResponse)
async def multiply_route(operation: OperationRequest):
    result = multiply(operation.a, operation.b)
    return {"result": result}


@app.post("/divide", response_model=OperationResponse)
async def divide_route(operation: OperationRequest):
    try:
        result = divide(operation.a, operation.b)
        return {"result": result}
    except ValueError:
        raise HTTPException(status_code=400, detail="Cannot divide by zero!")


# USER ENDPOINT
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username exists")

    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email exists")

    new_user = User(
        first_name=getattr(user, "first_name", None),
        last_name=getattr(user, "last_name", None),
        username=user.username,
        email=user.email,
        password=User.hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)