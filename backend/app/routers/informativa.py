from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.informativa import InformativaOut
from app.services.informativa import InformativaMancante, informativa_in_vigore

router = APIRouter(prefix="/informativa", tags=["informativa"])


@router.get("", response_model=InformativaOut)
def leggi_informativa(db: Session = Depends(get_db)):
    """Informativa privacy attualmente in vigore (pubblica)."""
    try:
        return informativa_in_vigore(db)
    except InformativaMancante:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, detail="Servizio non disponibile"
        )
