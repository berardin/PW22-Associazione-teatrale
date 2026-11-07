from datetime import date

from pydantic import BaseModel, ConfigDict


class StatutoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    versione: str
    testo: str
    in_vigore_dal: date
