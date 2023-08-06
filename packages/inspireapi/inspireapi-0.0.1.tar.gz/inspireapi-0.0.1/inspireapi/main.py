#cfulcher
from inspireapi import dtypes 

class Inspire: 
    def get_insight(self, ticker: str) -> dtypes.Insight:
        return dtypes.Insight(ticker).data


