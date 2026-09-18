import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models.booking import Booking
from app.database.models.table import Table
from app.schemas.booking import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new booking",
)
def create_booking(
    payload: BookingCreate,
    db: Session = Depends(get_db),
):
    # 1. Verify table exists
    table = db.query(Table).filter(Table.id == payload.table_id).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with id '{payload.table_id}' does not exist",
        )

    # 2. Check party size capacity
    if payload.party_size > table.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Party size ({payload.party_size}) exceeds table capacity ({table.capacity})",
        )

    booking_id = payload.id or str(uuid.uuid4())

    # 3. Check ID uniqueness
    existing = db.query(Booking).filter(Booking.id == booking_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Booking with id '{booking_id}' already exists",
        )

    # 4. Check for overlapping reservations on the same table
    overlapping = (
        db.query(Booking)
        .filter(
            Booking.table_id == payload.table_id,
            Booking.status != "cancelled",
            and_(
                Booking.start_time < payload.end_time,
                Booking.end_time > payload.start_time,
            ),
        )
        .first()
    )
    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Table is already booked during the requested time window",
        )

    # 5. Create booking record
    booking = Booking(
        id=booking_id,
        table_id=payload.table_id,
        guest_name=payload.guest_name,
        guest_phone=payload.guest_phone,
        party_size=payload.party_size,
        start_time=payload.start_time,
        end_time=payload.end_time,
        status=payload.status,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get(
    "",
    response_model=List[BookingResponse],
    summary="List bookings",
)
def list_bookings(
    table_id: Optional[str] = Query(default=None, description="Filter bookings by table ID"),
    status: Optional[str] = Query(default=None, description="Filter bookings by status (e.g., confirmed, cancelled)"),
    limit: int = Query(default=100, ge=1, le=1000, description="Max number of items to return"),
    offset: int = Query(default=0, ge=0, description="Number of items to skip"),
    db: Session = Depends(get_db),
):
    query = db.query(Booking)
    if table_id:
        query = query.filter(Booking.table_id == table_id)
    if status:
        query = query.filter(Booking.status == status)

    bookings = query.order_by(Booking.start_time.asc()).offset(offset).limit(limit).all()
    return bookings


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
    summary="Get a booking by ID",
)
def get_booking(
    booking_id: str,
    db: Session = Depends(get_db),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id '{booking_id}' not found",
        )
    return booking
