from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, data_sources, projects, locations, processing

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers from API modules
app.include_router(auth.router, prefix="/api", tags=['auth'])
app.include_router(projects.router, prefix="/api",tags=['projects'])
app.include_router(locations.router, prefix="/api",tags=['locations'])
app.include_router(data_sources.router, prefix="/api",tags=['data_sources'])
# app.include_router(processing.router, prefix="/api",tags=['processing'])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
