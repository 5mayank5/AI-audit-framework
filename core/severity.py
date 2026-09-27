def classify_severity(risk):

    if risk >= 0.75:
        return "Critical"
    elif risk >= 0.50:
        return "High"
    elif risk >= 0.25:
        return "Medium"
    else:
        return "Low"