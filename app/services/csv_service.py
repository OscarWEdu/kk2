import csv
from io import StringIO
from fastapi import UploadFile
from typing import Any
from models.csv_model import CSVData

class CSVService:
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

    async def parse_csv(self, file: UploadFile) -> CSVData:
        content = await file.read()
        text = content.decode("utf-8")

        reader = csv.DictReader(StringIO(text))
        rows = []
        for row in reader:
            converted = {i: self._typecheck(data) for i, data in row.items()}
            rows.append(converted)
            
        columns = list(reader.fieldnames or [])

        return CSVData(
            columns=columns,
            rows=rows
        )