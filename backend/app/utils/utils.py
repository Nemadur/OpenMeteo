from datetime import date, timedelta
import numpy as np

def get_default_dates():
    yesterday = date.today() - timedelta(days=1)
    return yesterday.isoformat(), yesterday.isoformat()

# def average(values: list[float]) -> float:
#     return sum(values) / len(values)

def average(x):
    return float(np.mean(x))