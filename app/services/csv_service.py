import csv
from io import StringIO
from fastapi import UploadFile, HTTPException
from typing import Any
from models.csv_model import CSVData, CSVMetadata, CSVStats
import pandas as pd

class CSVService:
    def __init__(self):
        self.data: CSVData | None = None
        self.df: pd.DataFrame | None = None
        self.stats: dict | None = None

    def _typecheck(self, value: str) -> Any: #Do some typechecking on csv fields
        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        return value

    def get_metadata(self) -> CSVMetadata:
        if self.df is None:
            raise HTTPException(status_code=404, detail="No CSV has been uploaded.")

        return CSVMetadata(
            num_rows = len(self.df),
            columns = self.df.columns.tolist(),
            dtypes = self.df.dtypes.apply(str).to_dict()
        )

    async def parse_csv(self, file: UploadFile) -> CSVData:
        content = await file.read()
        text = content.decode("utf-8")

        reader = csv.DictReader(StringIO(text))
        rows = []
        for row in reader:
            converted = {i: self._typecheck(data) for i, data in row.items()}
            rows.append(converted)
            
        columns = list(reader.fieldnames or [])

        parsed_csv = CSVData(columns=columns, rows=rows)
        self.data = parsed_csv
        self.df = pd.DataFrame(rows)
        self.stats = None

        return parsed_csv
    
    def get_stats(self) -> CSVStats:
        if self.df is None:
            raise HTTPException(status_code=404, detail="No CSV has been uploaded.")

        csv_stats = self.df.describe(include="all")
        stats_dict = csv_stats.to_dict()

        stats_dict = {str(column): i for column, i in stats_dict.items()}

        return CSVStats(stats=stats_dict)
