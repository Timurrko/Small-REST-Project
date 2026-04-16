import numpy as np

def calculate_stats(values):
    if not values:
        return {
            "min": None,
            "max": None,
            "count": 0,
            "sum": 0,
            "median": None
        }

    return {
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "count": int(len(values)),
        "sum": float(np.sum(values)),
        "median": float(np.median(values))
    }

def analyze(measurements):
    x_vals = [m.x for m in measurements]
    y_vals = [m.y for m in measurements]
    z_vals = [m.z for m in measurements]

    return {
        "x": calculate_stats(x_vals),
        "y": calculate_stats(y_vals),
        "z": calculate_stats(z_vals),
    }