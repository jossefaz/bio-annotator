from pydantic import BaseModel


class Variant:
    chromosome: str
    start: str
    end: str
    ref: str
    alt: str
    assembly: str
