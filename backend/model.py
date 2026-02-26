def predict_crop(temp, humidity):
    if temp > 25 and humidity > 60:
        return "Rice ðŸŒ¾"
    elif temp < 20:
        return "Wheat ðŸŒ±"
    else:
        return "Maize ðŸŒ½"
