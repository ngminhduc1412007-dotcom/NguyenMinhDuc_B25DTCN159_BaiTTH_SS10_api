from datetime import datetime
from sqlalchemy.orm import Session
from models import ClassroomModel
from schemas import CreateClassroom

def get_all_classes_service(db: Session):
    list_classes = db.query(ClassroomModel).all()
    return list_classes

def get_class_by_id_service(id: int, db: Session):
    class_in_db = db.query(ClassroomModel).filter(ClassroomModel.id == id).first()
    return class_in_db

def create_class_service(new_class: CreateClassroom, db: Session):
    classroom_data = new_class.model_dump()
    if classroom_data.get("created_at") is None:
        classroom_data["created_at"] = datetime.now()

    classroom = ClassroomModel(**classroom_data)
    try:
        db.add(classroom)
        db.commit()
        db.refresh(classroom)
        return classroom
    except Exception:
        db.rollback()
        raise