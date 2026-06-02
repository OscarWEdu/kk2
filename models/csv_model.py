from pydantic import BaseModel
from typing import List, Dict

class CSVData(BaseModel):
    columns: List[str]
    rows: List[Dict[str, str]] #TODO: Convert to any before storing as model
