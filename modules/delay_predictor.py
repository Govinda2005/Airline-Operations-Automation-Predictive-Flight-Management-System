class DelayPredictor:
    def predict(self, flight, weather, crew_available):
        delay = 0
        reasons = []

        if weather["crosswind"] > 40:
            delay += 20
            reasons.append("High crosswind")

        if weather["visibility"] < 1500:
            delay += 15
            reasons.append("Low visibility")

        if weather["thunderstorm"]:
            delay += 25
            reasons.append("Thunderstorm")

        if flight["engine_thrust_deviation"] > 20:
            delay += 30
            reasons.append("Engine maintenance issue")

        if flight["cabin_pressure_delta"] < -3:
            delay += 20
            reasons.append("Cabin pressure drop")

        if weather["runway_queue_time"] > 25:
            delay += 15
            reasons.append("Runway congestion")

        if not crew_available:
            delay += 30
            reasons.append("Crew unavailable")

        return delay, reasons
