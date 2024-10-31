from functools import wraps
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base  
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:nedu@localhost:5432/chatsimple")
# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session maker
async_session = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

def db_session(f):
    """Decorator to handle database sessions in Flask routes."""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        async with async_session() as session:
            return await f(session, *args, **kwargs)
    return decorated_function

# Initialize the database
async def init_db():
    async with engine.begin() as conn:
        # Create all tables (if they do not exist)
        await conn.run_sync(Base.metadata.create_all)
        print("Initializing database")



if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())