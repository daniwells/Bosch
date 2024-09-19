from typing import Optional
from pydantic import BaseModel

class Futball(BaseModel):
    id: Optional[int] = None
    name_team: str
    date_foundation: str
    qtd_champions: int
    stage: str