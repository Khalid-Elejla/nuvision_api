from fastapi import FastAPI
from api import auth, data_sources, projects, locations, processing

app = FastAPI()

# Include routers from API modules
app.include_router(auth.router, prefix="/api", tags=['auth'])
app.include_router(projects.router, prefix="/api",tags=['projects'])
app.include_router(locations.router, prefix="/api",tags=['locations'])
app.include_router(data_sources.router, prefix="/api",tags=['data_sources'])
# app.include_router(processing.router, prefix="/api",tags=['processing'])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
