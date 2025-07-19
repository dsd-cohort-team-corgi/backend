from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.service import Service, ServiceCreate, ServiceUpdate, ServiceEnum
from app.db.session import get_session
from app.utils.crud_helpers import get_all, get_one, create_one, update_one, delete_one

# TODO from app.utils.auth import get_current_user  # optional for auth-locking

router = APIRouter(prefix="/services", tags=["services"], responses={404: {"description": "Not found"}})


# GET all services
@router.get("/", response_model=list[Service])
async def read_services(session: Session = Depends(get_session)):
    return get_all(session, Service)


# GET one service by ID
@router.get("/{service_id}", response_model=Service)
async def read_service(service_id: UUID, session: Session = Depends(get_session)):
    return get_one(session, Service, service_id)


# GET service by category
@router.get("/category/{category_name}", response_model=list[Service])
async def read_service_category(category_name: str, session: Session = Depends(get_session)):
    # creates an array of all the values in the Service Enum (right side of enum)
    valid_categories = [category.value for category in ServiceEnum]

    if category_name not in valid_categories:
        # return []
        raise HTTPException(
            status_code=400,
            detail=f"invalid category, valid categories are: {valid_categories}",
        )
    try:
        # fetches the value from the enum based on the category name passed and was validated
        enum_name = None
        for category in ServiceEnum:
            if category.value == category_name:
                enum_name = category.name
                break
        statement = select(Service).where(Service.category == enum_name)
        result = session.exec(statement)
        return result.all()

    except:
        raise HTTPException(status_code=400, detail=f"{Service.__name__} not found")


# CREATE a service
@router.post("/", response_model=Service)
async def create_service(service: ServiceCreate, session: Session = Depends(get_session)):
    return create_one(session, Service, service.dict())


# UPDATE a service
@router.patch("/{service_id}", response_model=Service)
async def update_service(
    service_id: UUID,
    update_data: ServiceUpdate,
    session: Session = Depends(get_session),
):
    return update_one(session, Service, service_id, update_data.dict(exclude_unset=True))


# DELETE a service
@router.delete("/{service_id}", response_model=dict)
async def delete_service(service_id: UUID, session: Session = Depends(get_session)):
    return delete_one(session, Service, service_id)
