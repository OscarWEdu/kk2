from pydantic import BaseModel
from typing import List, Dict, Any

class CSVData(BaseModel):
    columns: List[str]
    rows: List[Dict[str, Any]]

class CSVMetadata(BaseModel):
    num_rows: int
    columns: List[str]
    dtypes: Dict[Any, str]