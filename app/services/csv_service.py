import csv
from io import StringIO
from fastapi import UploadFile, HTTPException
from typing import Any
from app.models.csv_model import CSVData, CSVMetadata, CSVStats
import pandas as pd

class CSVService:
    def __init__(self):
        self.data: CSVData | None = None
        self.df: pd.DataFrame | None = None
        self.stats: dict | None = None

    # Does typechecks on the given csv value and returns it correctly typed
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

    # Returns some given metadata about the csv data
    def get_metadata(self) -> CSVMetadata:
        if self.df is None:
            raise HTTPException(status_code=404, detail="No CSV has been uploaded.")

        if self.df.empty or len(self.df.columns) == 0:
            raise HTTPException(status_code=400, detail="Invalid file")
                            
        return CSVMetadata(
            num_rows = len(self.df),
            columns = self.df.columns.tolist(),
            dtypes = self.df.dtypes.apply(str).to_dict()
        )

    # Parses a csv file using the built in csv library, and stores it
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
    
    # Runs describe() on the relevant data, and stores it
    def get_stats(self) -> CSVStats:
        if self.df is None or self.df.empty:
            raise HTTPException(status_code=404, detail="No CSV has been uploaded.")

        csv_stats = self.df.describe(include="all")
        stats_dict = csv_stats.to_dict()
        stats_dict = {str(column): i for column, i in stats_dict.items()}

        # Compute Pearson correlation
        numeric_df = self.df.select_dtypes(include=["int64", "float64"])
        if not numeric_df.empty and numeric_df.shape[1] > 1:
            correlation = numeric_df.corr(method="pearson")
            stats_dict["pearson_r"] = correlation.to_dict()

        return CSVStats(stats=stats_dict)
    
    # Returns the stats from describe() in a string format for the llm
    def get_formatted_stats(self) -> str:
        stats = self.get_stats().stats
        lines = []

        for column, column_stats in stats.items():
            lines.append(f"Column: {column}")
            for stat_name, value in column_stats.items():
                lines.append(f"  {stat_name}: {value}")
            lines.append("") #Empty Line

        return "\n".join(lines)
