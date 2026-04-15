from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, timedelta
from app.database import Base
from passlib.context import CryptContext
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "secret"
ALGORITHM = "HS256"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # ✅ FIX 1

    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # ---------------- PASSWORD ----------------
    @staticmethod
    def hash_password(password: str) -> str:
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    # ---------------- REGISTER ----------------
    @classmethod
    def register(cls, db, user_data: dict):
        password = user_data.get("password")

        # ✅ FIX 4: handle missing password correctly
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

        # check duplicates
        existing = db.query(cls).filter(
            (cls.email == user_data["email"]) |
            (cls.username == user_data["username"])
        ).first()

        if existing:
            raise ValueError("Username or email already exists")

        user_data["password"] = cls.hash_password(password)

        user = cls(**user_data)
        db.add(user)

        return user  # DO NOT COMMIT

    # ---------------- AUTH ----------------
    @classmethod
    def authenticate(cls, db, username_or_email: str, password: str):
        user = db.query(cls).filter(
            (cls.username == username_or_email) |
            (cls.email == username_or_email)
        ).first()

        if not user or not user.verify_password(password):
            return None

        # ✅ FIX 3: update last_login
        user.last_login = datetime.utcnow()
        db.commit()  # ✅ FIX 5 (prevents StaleDataError)

        token = cls.create_access_token({"sub": str(user.id)})

        return {
            "access_token": token,
            "token_type": "bearer",  # ✅ FIX 2
            "user": user
        }

    # ---------------- TOKEN ----------------
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        to_encode["exp"] = datetime.utcnow() + timedelta(hours=1)
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return int(payload.get("sub"))
        except Exception:
            return None

    # ---------------- STRING ----------------
    def __str__(self):
        return f"<User(name={self.first_name} {self.last_name}, email={self.email})>"