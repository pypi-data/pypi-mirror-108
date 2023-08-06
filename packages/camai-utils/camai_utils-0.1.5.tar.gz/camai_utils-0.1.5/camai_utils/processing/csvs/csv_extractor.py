from typing import Iterable, Dict, Any
import pandas as pd


class CSVExtractor:
    def __init__(self, csv_bytes):
        self.df = pd.read_csv(csv_bytes)
        self.field_map = {'Member ID': 'patient_id',
                          'Test Result': 'positivity'}
        self.df.columns = [self.field_map.get(c, c) for c in self.df.columns]

    def search(self, s):
        return [k for k in self.df.columns if s.upper() in k.upper()]

    def extract(self, fields=Iterable[str]) -> Dict[str, Any]:
        return self.df[fields].to_dict(orient='records')
