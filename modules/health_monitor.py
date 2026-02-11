import logging

health_logger = logging.getLogger("health")
critical_logger = logging.getLogger("critical")

health_logger.setLevel(logging.WARNING)
critical_logger.setLevel(logging.ERROR)

health_logger.addHandler(logging.FileHandler("logs/aircraft_health_alerts.log"))
critical_logger.addHandler(logging.FileHandler("logs/critical_flight_alerts.log"))

class HealthMonitor:
    def check(self, flight):
        if flight["engine_vibration"] > 8:
            critical_logger.error(f"{flight['flight_id']} - Engine vibration")

        if flight["fuel_burn_rate"] > 6:
            health_logger.warning(f"{flight['flight_id']} - High fuel burn")

        if flight["cabin_temperature"] > 26:
            health_logger.warning(f"{flight['flight_id']} - High cabin temperature")
