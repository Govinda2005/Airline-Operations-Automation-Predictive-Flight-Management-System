class CrewOptimizer:
    def __init__(self, crew):
        self.crew = crew
        self.assigned = set()

    def assign(self, flight_id):
        """
        Primary assignment:
        - Available
        - Rest-hour compliant
        - Not already assigned
        """
        for member in self.crew:
            if (
                member["available"]
                and not member.get("standby", False)
                and member["rest_hours"] >= 8
                and member["crew_id"] not in self.assigned
            ):
                self.assigned.add(member["crew_id"])
                return member, "PRIMARY"

        """
        Standby auto-assignment:
        - Standby crew
        - Minimum rest threshold (>= 6 hrs)
        """
        for member in self.crew:
            if (
                member.get("standby", False)
                and member["rest_hours"] >= 6
                and member["crew_id"] not in self.assigned
            ):
                self.assigned.add(member["crew_id"])
                return member, "STANDBY"

        # No crew available
        return None, "NONE"
