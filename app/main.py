from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import user, todo  # 👈 Import user routes

app = FastAPI(title="To-Do List API")

# Create all tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user.router)
app.include_router(todo.router)

# CORS Middleware (if using frontend or testing from browser tools)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do List API!"}