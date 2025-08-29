from fastapi import FastAPI
from contextlib import asynccontextmanager
import beanie
import motor.motor_asyncio
from core.config import settings
from models.ticket import Ticket
from api.endpoints import tickets

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's lifespan events.
    This function is executed once when the application starts up.
    """
    # Initialize the database client
    db_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)

    # Initialize Beanie with the Ticket document model
    await beanie.init_beanie(
        database=db_client.get_default_database(), document_models=[Ticket]
    )
    print("Database connection initialized.")
    yield
    # (Cleanup code could go here, after the yield)
    print("Closing database connection.")


# --- Basic Application Setup ---
app = FastAPI(
    title="Case Study Ticket API with MongoDB",
    description="An API that serves mock ticket data, persisted in a MongoDB database.",
    version="3.0.0",
    lifespan=lifespan # Use the new lifespan manager
)

# --- Include Routers ---
app.include_router(tickets.router, prefix="/api", tags=["Tickets"])


# --- Root Endpoint ---
@app.get("/", include_in_schema=False)
def root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Ticket API. See /docs for documentation."}
