import csv
from io import StringIO
from fastapi import UploadFile
from models.csv_model import CSVData

class CSVService:
    async def parse_csv(self, file: UploadFile) -> CSVData:
        content = await file.read()
        text = content.decode("utf-8")

        reader = csv.DictReader(StringIO(text))
        rows = list(reader)
        columns = list(reader.fieldnames or [])

        return CSVData(
            columns=columns,
            rows=rows
        )