from datetime import date

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models import Statuto


class StatutoMancante(Exception):
    """Nessuno statuto in vigore: configurazione errata."""


def statuto_in_vigore(db: Session) -> Statuto:
    s = db.scalar(
        select(Statuto)
        .where(Statuto.in_vigore_dal <= date.today())
        .order_by(desc(Statuto.in_vigore_dal))
        .limit(1)
    )
    if s is None:
        raise StatutoMancante("Nessuno statuto in vigore")
    return s
