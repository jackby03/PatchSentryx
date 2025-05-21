import asyncio

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from contexts.auth.interfaces import auth_router
from contexts.inventory.interfaces.collection_router import router as collection_router
from contexts.inventory.interfaces.item_router import router as item_router
from contexts.users.interfaces import user_router
from contexts.users.interfaces.consumers.user_consumer import (
    consume_create_user_commands,
)
from core.database import Base, close_db, engine, init_db
from core.messaging import close_rabbitmq_connection

# Initialize FastAPI app with docs always enabled
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend project demonstrating Hexagonal Architecture, CQRS, and Bundle-Contexts with FastAPI.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed origins: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Event Handlers ---
@app.on_event("startup")
async def startup_event():
    print("Starting up ContextFlow application...")
    await init_db()
    # Initialize RabbitMQ connection pool (if using a shared pool)
    # await init_rabbitmq()
    print("Application startup complete.")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down ContextFlow application...")
    await close_db()  # Close database connections gracefully
    await close_rabbitmq_connection()  # Close RabbitMQ connection
    print("Application shutdown complete.")


# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Custom handler for Pydantic validation errors
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )


# Add other custom exception handlers here (e.g., for domain-specific errors)
# @app.exception_handler(DomainError)
# async def domain_exception_handler(request: Request, exc: DomainError):
#     return JSONResponse(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         content={"message": str(exc)},
#     )

# --- Routers ---
# Include user and auth routers
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(
    collection_router, prefix="/inventory/collections", tags=["Inventory Collections"]
)
app.include_router(item_router, prefix="/inventory/items", tags=["Inventory Items"])


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint providing basic app info."""
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "environment": settings.ENVIRONMENT,
        "docs_url": app.docs_url,
    }


# --- Optional: Function to create tables (useful for testing/dev) ---
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created (if they didn't exist).")


if __name__ == "__main__":
    # Example of how to run create_tables before starting uvicorn for local dev
    import asyncio

    asyncio.run(create_tables())
    # Then run uvicorn command manually:
    # uvicorn app.main:app --reload
