from typing import List
from fastapi import APIRouter, Depends
from models.ticket import Ticket
from services.ticket_service import get_or_create_tickets_for_version
from api.dependencies.auth import auth_v1, auth_v2

router = APIRouter()

@router.get(
    "/v1/tickets",
    response_model=List[Ticket],
    # This is important for beanie to use your field aliases ("Create Date") in the JSON response
    response_model_by_alias=True,
    summary="Endpoint V1 for Tickets",
    dependencies=[Depends(auth_v1)]
)
async def get_tickets_v1():
    """
    **Endpoint 1:** Retrieves a list of mock tickets.
    On first run, it generates tickets and saves them to the database.
    On subsequent runs, it returns the persisted tickets from the database.
    """
    # The logic is now handled by the service layer
    return await get_or_create_tickets_for_version("v1")


@router.get(
    "/v2/tickets",
    response_model=List[Ticket],
    # This is important for beanie to use your field aliases in the JSON response
    response_model_by_alias=True,
    summary="Endpoint V2 for Tickets",
    dependencies=[Depends(auth_v2)]
)
async def get_tickets_v2():
    """
    **Endpoint 2:** Retrieves a different list of mock tickets.
    On first run, it generates tickets and saves them to the database.
    On subsequent runs, it returns the persisted tickets from the database.
    """
    # The logic is now handled by the service layer
    return await get_or_create_tickets_for_version("v2")

