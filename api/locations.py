# from fastapi import APIRouter, Depends, HTTPException
# from typing import List
# from database.models.location import Location
# from database.models.user import User
# from .auth import get_current_user

# router = APIRouter()

# # Mock database for demonstration
# locations_db = []

# # Create location endpoint
# @router.post("/locations/", response_model=Location)
# async def create_location(location: Location, current_user: User = Depends(get_current_user)):
#     # Create location logic (e.g., save to database)
#     locations_db.append(location)
#     return location

# # Get all locations endpoint
# @router.get("/locations/", response_model=List[Location])
# async def read_locations(current_user: User = Depends(get_current_user)):
#     return locations_db

# # Get location by ID endpoint
# @router.get("/locations/{location_id}", response_model=Location)
# async def read_location(location_id: int, current_user: User = Depends(get_current_user)):
#     location = next((l for l in locations_db if l.id == location_id), None)
#     if location is None:
#         raise HTTPException(status_code=404, detail="Location not found")
#     return location

# # Update location endpoint
# @router.put("/locations/{location_id}", response_model=Location)
# async def update_location(location_id: int, location: Location, current_user: User = Depends(get_current_user)):
#     # Update location logic (e.g., update in database)
#     index = next((i for i, l in enumerate(locations_db) if l.id == location_id), None)
#     if index is None:
#         raise HTTPException(status_code=404, detail="Location not found")
#     locations_db[index] = location
#     return location

# # Delete location endpoint
# @router.delete("/locations/{location_id}")
# async def delete_location(location_id: int, current_user: User = Depends(get_current_user)):
#     # Delete location logic (e.g., delete from database)
#     global locations_db
#     locations_db = [l for l in locations_db if l.id != location_id]
#     return {"message": "Location deleted successfully"}
