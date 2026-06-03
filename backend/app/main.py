from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.weather import router

app = FastAPI(
    title="Weather Ranking API"
)

# Include the weather router under the /api/v1 prefix to organize API endpoints and allow for future expansion with additional routes or versions without cluttering the main application file. 
# This keeps the codebase modular and maintainable.
app.include_router(
    router,
    prefix="/api/v1"
)

# Allow CORS for all origins, methods, and headers (suitable for development only) to enable frontend applications to access the API without restrictions. 
# In production, this should be configured more securely to allow only trusted origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for dev only
    allow_methods=["*"],
    allow_headers=["*"],
)