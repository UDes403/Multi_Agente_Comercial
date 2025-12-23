from typing import List, Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

class InterestSchema(BaseModel):
    interest: List[str] = Field(description="Intereses principales del usuario")

class Router(TypedDict):
    next: Literal[
        "agente_recepcionista",
        "agente_promotor",
        "agente_asesor",
        "agente_vendedor",
        "agente_encuestador",
        "FINISH",
    ]