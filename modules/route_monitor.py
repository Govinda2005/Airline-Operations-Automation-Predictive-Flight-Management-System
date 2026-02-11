class RouteMonitor:
    def analyze(self, route, weather):
        if weather["thunderstorm"]:
            return True, route["alternate"], 45
        return False, None, 0
