from datetime import date

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models import InformativaPrivacy


class InformativaMancante(Exception):
    """Nessuna informativa in vigore: configurazione errata."""


def informativa_in_vigore(db: Session) -> InformativaPrivacy:
    inf = db.scalar(
        select(InformativaPrivacy)
        .where(InformativaPrivacy.in_vigore_dal <= date.today())
        .order_by(desc(InformativaPrivacy.in_vigore_dal))
        .limit(1)
    )
    if inf is None:
        raise InformativaMancante("Nessuna informativa privacy in vigore")
    return inf
