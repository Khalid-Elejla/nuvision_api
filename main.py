from fastapi import FastAPI
from api import auth, data_source, projects, locations, processing

app = FastAPI()

# Include routers from API modules
app.include_router(auth.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
#app.include_router(locations.router, prefix="/api")
# app.include_router(videos.router, prefix="/api")
# app.include_router(processing.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
