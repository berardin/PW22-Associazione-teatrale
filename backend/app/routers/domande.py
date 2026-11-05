from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.domanda import DomandaIn, DomandaOut
from app.services import domanda_service as service

router = APIRouter(prefix="/domande", tags=["domande"])


@router.post("", response_model=DomandaOut, status_code=status.HTTP_201_CREATED)
def presenta_domanda(dati: DomandaIn, db: Session = Depends(get_db)):
    """Presentazione pubblica di una domanda di iscrizione all'associazione."""
    try:
        return service.presenta_domanda(db, dati)
    except service.DomandaEsistente as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))
    except service.InformativaMancante:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, detail="Servizio non disponibile"
        )
