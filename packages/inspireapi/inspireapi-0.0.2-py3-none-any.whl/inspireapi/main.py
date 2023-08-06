#cfulcher
from inspireapi import dtypes 

def get_insight(ticker: str) -> dtypes.Insight:
    return dtypes.Insight(ticker).data


