# app/crud.py

# Required imports
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from typing import Generic, TypeVar, List

T = TypeVar("T")

def handle_not_found(obj: T):
    """
    Utility function to raise a 404 error if the queried object is not found.
    """
    if not obj:
        raise HTTPException(status_code=404, detail="There's nothing here...")

class CRUD(Generic[T]):
    """
    Generic CRUD operations class for synchronous database operations.
    """

    def __init__(self, model: T):
        self.model = model

    def create(self, obj_data: dict, db: Session) -> T:
        obj = self.model(**obj_data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def bulk_create(self, objs_data: List[dict], db: Session) -> List[T]:
        objects = [self.model(**obj_data) for obj_data in objs_data]
        db.add_all(objects)
        db.commit()
        return objects

    def retrieve(self, db: Session, obj_id: int) -> T:
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        handle_not_found(obj)
        return obj
    
    def get_related(self, db: Session, parent_id: int) -> List[T]:
        related = db.query(self.model).filter(self.model.parent_id == parent_id).all()
        return related

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def list_by_parent_id(self, db: Session, parent_id: int, skip: int = 0, limit: int = 100) -> List[T]:
        return db.query(self.model).filter(self.model.parent_id == parent_id).offset(skip).limit(limit).all()

    def update(self, db: Session, obj_id: int, obj_data: dict, skip_fields: set = None) -> T:
        obj = db.query(self.model).filter(self.model.id == obj_id).first()

        # Replace this with your actual 'handle_not_found' function
        if obj is None:
            raise ValueError("Object not found")
        
        # Default fields to skip if none are provided
        if skip_fields is None:
            skip_fields = {'id', 'created', 'updated'}

        for key, value in obj_data.items():
            if value is not None and key not in skip_fields:
                setattr(obj, key, value)

        db.commit()
        db.refresh(obj)
        return obj

    def bulk_update(self, updates: List[dict], db: Session) -> List[T]:
        updated_objects = []
        for update_data in updates:
            obj_id = update_data.pop("id")
            obj = self.update(db, obj_id, update_data)
            updated_objects.append(obj)
        return updated_objects

    def delete(self, db: Session, obj_id: int) -> None:
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        handle_not_found(obj)
        db.delete(obj)
        db.commit()

    def add_link(self, db: Session, association_table, **kwargs) -> T:
        relation = association_table(**kwargs)
        db.add(relation)
        db.commit()
        db.refresh(relation)
        return relation

    def remove_link(self, db: Session, association_table, relation_id: int) -> None:
        relation = db.query(association_table).filter(association_table.id == relation_id).first()
        handle_not_found(relation)
        db.delete(relation)
        db.commit()
