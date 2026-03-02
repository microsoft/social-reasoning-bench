from pydantic import BaseModel, Field


class CatalogEntry(BaseModel):
    id: str
    name: str
    description: str
    reference_price: float = Field(gt=0)


class ReservationContext(BaseModel):
    context_id: str
    catalog_id: str
    buyer_description: str
    buyer_reservation_story: str
    buyer_reservation_price: float = Field(ge=0)
    seller_description: str
    seller_reservation_story: str
    seller_reservation_price: float = Field(ge=0)
