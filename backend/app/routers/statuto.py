from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.statuto import StatutoOut
from app.services.statuto import StatutoMancante, statuto_in_vigore

router = APIRouter(prefix="/statuto", tags=["statuto"])


@router.get("", response_model=StatutoOut)
def leggi_statuto(db: Session = Depends(get_db)):
    """Statuto dell'associazione attualmente in vigore (pubblico)."""
    try:
        return statuto_in_vigore(db)
    except StatutoMancante:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, detail="Servizio non disponibile"
        )
