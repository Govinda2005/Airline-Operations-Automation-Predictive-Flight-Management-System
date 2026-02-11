from statistics import mean

class LoadPredictor:
    def analyze(self, data):
        avg = mean(data["historical_load_factors"])

        if avg > 0.9:
            status = "Overbooking risk"
        elif avg < 0.5:
            status = "Under-utilized"
        else:
            status = "Normal demand"

        return avg, status
