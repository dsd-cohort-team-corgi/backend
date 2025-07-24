from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.provider import Provider
from app.models.provider_inventory import (
    ProviderInventory,
    ProviderInventoryCreate,
    ProviderInventoryUpdate
)
from app.utils.auth import get_current_user_id
from app.utils.user_helpers import get_user_scoped_record

router = APIRouter(
    prefix="/provider_inventory",
    tags=["provider_inventory"]
)

@router.post("/", response_model=ProviderInventory)
def create_provider_inventory(
        inventory_data: ProviderInventoryCreate,
        supabase_user_id: UUID = Depends(get_current_user_id),
        session: Session = Depends(get_session)
):
    # Make sure the user has a provider profile
    db_provider = get_user_scoped_record(session, Provider, supabase_user_id)
    if not db_provider:
        raise HTTPException(status_code=400, detail="No provider profile found for user")

    # Create the provider's inventory
    provider_inventory = ProviderInventory(
        **inventory_data.model_dump(),
        supabase_user_id = supabase_user_id,
        provider_id = db_provider.id,
    )
    session.add(provider_inventory)
    session.commit()
    session.refresh(provider_inventory)
    return provider_inventory


@router.get("/", response_model=list[ProviderInventory])
def read_all_provider_inventory(session: Session = Depends(get_session)):
    return session.exec(select(ProviderInventory)).all()


@router.get("/{inventory_id}", response_model=ProviderInventory)
def read_provider_inventory(inventory_id: UUID, session: Session = Depends(get_session)):
    item = session.get(ProviderInventory, inventory_id)
    if not item:
        raise HTTPException(status_code=404, detail="Provider inventory not found")
    return item


@router.put("/{inventory_id}", response_model=ProviderInventory)
def update_provider_inventory(
        inventory_id: UUID,
        updates: ProviderInventoryUpdate,
        session: Session = Depends(get_session)
):
    item = session.get(ProviderInventory, inventory_id)
    if not item:
        raise HTTPException(status_code=404, detail="Provider inventory not found")
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{inventory_id}")
def delete_provider_inventory(inventory_id: UUID, session: Session = Depends(get_session)):
    item = session.get(ProviderInventory, inventory_id)
    if not item:
        raise HTTPException(status_code=404, detail="Provider inventory not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
