# app.api.py

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form, Body
from app.database import SessionLocal
from app.crud import CRUD
from app.models import Art
from app.utilities import upload_image, extract_colours
from sqlalchemy.orm import Session
from app.schemas import ArtCreate, ArtRead, ArtUpdate, ArtType, ArtReadDetail
from typing import List, Optional
from io import BytesIO
from PIL import Image

router = APIRouter()

# Create instances of CRUD operations for Art and Audio
art_crud = CRUD(Art)
# audio_crud = CRUD(Audio)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/art/", response_model=ArtRead)
async def create_art(
    title: str = Form(...),
    art_type: str = Form(...),
    description: str = Form(None),
    parent_id: int = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Read the original image stream
    original_image_stream = await file.read()
    original_image_byte_stream = BytesIO(original_image_stream)

    # Upload the original image to Cloudinary
    upload_result = upload_image(original_image_stream)
    if upload_result is None:
        raise HTTPException(status_code=400, detail="Image upload failed")
        
    image_url, auto_tags = upload_result
    
    # Get the dominant colours (let extract_colours handle resizing)
    colours = extract_colours(original_image_byte_stream)

    # Prepare the data
    art_data = {
        "title": title,
        "type": art_type,
        "description": description,
        "colours": colours,
        "tags": auto_tags,
        "parent_id": parent_id,
        "url": image_url
    }

    # Save to database
    art_crud = CRUD(Art)  # Assuming CRUD(Art) is imported and initialised
    created_art = art_crud.create(art_data, db)

    # Convert SQLAlchemy model instance to a Pydantic model
    return ArtRead(
        id=created_art.id,
        title=created_art.title,
        description=created_art.description,
        type=created_art.type.value if created_art.type else None,
        colours=created_art.colours,
        url=created_art.url,
        tags=created_art.tags,
        parent_id=created_art.parent_id,
        created=created_art.created,
        updated=created_art.updated
    )


# Retrieve all artwork
@router.get("/art/", response_model=List[ArtRead])
def list_artworks(skip: int = 0, limit: int = 100, parent_id: Optional[int] = None, db: Session = Depends(get_db)):
    if parent_id is not None:
        artworks = art_crud.list_by_parent_id(db, parent_id, skip=skip, limit=limit)
    else:
        artworks = art_crud.list(db, skip=skip, limit=limit)
    # Convert each SQLAlchemy model instance in the list to a dictionary and handle Enums
    return [ArtRead(
            id=art.id,
            title=art.title,
            description=art.description,
            type=art.type.value if art.type else None,  # Convert Enum to string
            url=art.url,
            colours=art.colours,
            created=art.created,
            parent_id=art.parent_id,
            tags=art.tags,
            updated=art.updated
        ) for art in artworks]

# Retrieve artwork by ID
@router.get("/art/{id}/", response_model=ArtRead)
def retrieve_artwork(id: int, db: Session = Depends(get_db)):
    art = art_crud.retrieve(db, id)
    return ArtRead(
        id=art.id,
        title=art.title,
        description=art.description,
        type=art.type.value if art.type else None,
        url=art.url,
        colours=art.colours,
        created=art.created,
        parent_id=art.parent_id,
        tags=art.tags,
        updated=art.updated
    )

# Update artwork by ID
@router.put("/art/{id}/", response_model=ArtRead)
def update_artwork(id: int, art: ArtUpdate, db: Session = Depends(get_db)):
    updated_art = art_crud.update(db, id, art.model_dump())
    # Convert SQLAlchemy model instance to a Pydantic model
    return ArtRead(
        id=updated_art.id,
        title=updated_art.title,
        description=updated_art.description,
        url=updated_art.url,
        type=updated_art.type.value if updated_art.type else None,
        colours=updated_art.colours,
        created=updated_art.created,
        parent_id=updated_art.parent_id,
        tags=updated_art.tags,
        updated=updated_art.updated
    )

# Delete artwork by ID
@router.delete("/art/{id}/")
def delete_artwork(id: int, db: Session = Depends(get_db)):
    art_crud.delete(db, id)
    return {"status": "Artwork sucessfully terminated."}



# Updated endpoint for retrieving artwork by ID and related artworks
@router.get("/art/{id}/detail", response_model=ArtReadDetail)
def retrieve_artwork(id: int, db: Session = Depends(get_db)):
    # Retrieve the main artwork by ID
    art = art_crud.retrieve(db, id)
    if art is None:
        raise HTTPException(status_code=404, detail="Artwork not found")

    # Retrieve related artworks using the parent_id
    related_artworks = art_crud.get_related(db, art.id)

    # Populate the response model
    return ArtReadDetail(
        id=art.id,
        title=art.title,
        description=art.description,
        type=art.type.value if art.type else None,
        url=art.url,
        colours=art.colours,
        created=art.created,
        parent_id=art.parent_id,
        tags=art.tags,
        updated=art.updated,
        related_artwork=[
            {
                "id": related.id,
                "title": related.title,
                "description": related.description,
                "type": related.type.value if related.type else None,
                "url": related.url,
                "colours": related.colours,
                "created": related.created,
                "parent_id": related.parent_id,
                "tags": related.tags,
                "updated": related.updated
            } for related in related_artworks
        ]
    )