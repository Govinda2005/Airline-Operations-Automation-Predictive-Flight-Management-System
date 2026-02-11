from modules.log_processor import LogProcessor
from modules.delay_predictor import DelayPredictor
from modules.crew_optimizer import CrewOptimizer
from modules.load_predictor import LoadPredictor
from modules.health_monitor import HealthMonitor
from modules.route_monitor import RouteMonitor
from modules.dashboard import Dashboard
from modules.reporter import Reporter


# Initialize components
paths = {
    "aircraft": "data/aircraft_logs.json",
    "weather": "data/weather_logs.json",
    "crew": "data/crew_schedule.json",
    "passenger": "data/passenger_load.json",
    "routes": "data/routes.json"
}

log_processor = LogProcessor(paths)
delay_predictor = DelayPredictor()
crew_optimizer = CrewOptimizer(log_processor.crew_logs)
load_predictor = LoadPredictor()
health_monitor = HealthMonitor()
route_monitor = RouteMonitor()
dashboard = Dashboard()
reporter = Reporter()
# Dashboard metrics

dashboard_stats = []

total_flights = 0

total_delay_minutes = 0
critical_alerts = 0
crew_shortages = 0
load_factors = []
popular_routes = {}
weather_risk_summary = {"HIGH": 0, "LOW": 0}

report_lines = []


# Process each flight

for flight in log_processor.get_all_flights():
    total_flights += 1
    flight_id = flight["flight_id"]

    weather = log_processor.weather_logs[flight_id]
    passenger_data = log_processor.passenger_logs[flight_id]
    route = log_processor.routes[flight_id]

    # Crew assignment
    crew, crew_type = crew_optimizer.assign(flight_id)
    crew_available = crew is not None
    if not crew_available:
        crew_shortages += 1

    # Delay prediction
    delay, reasons = delay_predictor.predict(
        flight, weather, crew_available
    )
    total_delay_minutes += delay

    # Passenger load prediction
    avg_load, load_status = load_predictor.analyze(passenger_data)
    load_factors.append(avg_load)

    # Health monitoring
    health_monitor.check(flight)
    if flight["status_code"] in ["WARN", "CRITICAL"]:
        critical_alerts += 1

    # Route monitoring
    diversion_required, alternate, extra_time = route_monitor.analyze(
        route, weather
    )

    # Popular route tracking
    route_key = passenger_data["route"]
    popular_routes[route_key] = popular_routes.get(route_key, 0) + 1

    # Weather risk summary
    weather_risk_summary[weather["weather_risk_level"]] += 1

    # -------------------------------
    # Dashboard row per flight
    # -------------------------------
    dashboard_stats.extend([
        ["Flight", flight_id],
        ["Predicted Delay", f"{delay} mins"],
        ["Delay Reasons", ", ".join(reasons) if reasons else "None"],
        ["Crew Assigned", f"{crew['crew_id']} ({crew_type})" if crew else "Not Available"],
        ["Passenger Load", f"{round(avg_load * 100)}% ({load_status})"],
        ["Diversion Required", "Yes" if diversion_required else "No"],
        ["Alternate Airport", alternate if diversion_required else "N/A"],
        ["---", "---"]
    ])


    # Report content

    report_lines.append(
        f"""
Flight ID: {flight_id}
Route: {route['origin']} → {route['destination']}
Predicted Delay: {delay} mins
Delay Reasons: {', '.join(reasons) if reasons else 'None'}
Crew Assigned: {crew['crew_id']} ({crew_type}) if crew else 'Not Available'
Passenger Load: {round(avg_load * 100)}% ({load_status})
Weather Risk: {weather['weather_risk_level']}
Diversion Required: {diversion_required}
Alternate Airport: {alternate if diversion_required else 'N/A'}
----------------------------------------
"""
    )


# Aggregate dashboard metrics

average_load = round((sum(load_factors) / len(load_factors)) * 100, 2)
most_popular_route = max(popular_routes, key=popular_routes.get)

dashboard_stats.extend([
    ["Total Flights Monitored", total_flights],
    ["Total Predicted Delay", f"{total_delay_minutes} mins"],
    ["Critical Aircraft Alerts", critical_alerts],
    ["Crew Shortage Events", crew_shortages],
    ["Average Passenger Load", f"{average_load}%"],
    ["Most Popular Route", most_popular_route],
    ["High Weather Risk Flights", weather_risk_summary["HIGH"]],
    ["Low Weather Risk Flights", weather_risk_summary["LOW"]]
])
# Display dashboard & generate report
dashboard.display(dashboard_stats)
reporter.generate("\n".join(report_lines))
