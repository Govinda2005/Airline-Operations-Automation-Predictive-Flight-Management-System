import json

class LogProcessor:
    def __init__(self, paths):
        self.aircraft_logs = self._load(paths["aircraft"])
        self.weather_logs = self._load(paths["weather"])
        self.crew_logs = self._load(paths["crew"])
        self.passenger_logs = self._load(paths["passenger"])
        self.routes = self._load(paths["routes"])

    def _load(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def get_all_flights(self):
        return self.aircraft_logs
