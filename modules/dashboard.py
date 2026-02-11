class Dashboard:
    def display(self, stats):
        """
        Displays dashboard output in simple:
        Metric - Value format (no tables).
        """

        print("n AIRLINE OPERATIONS DASHBOARD")

        section = "FLIGHT-WISE OPERATIONAL STATUS"
        print(f"{section}\n")

        separator_count = 0

        for key, value in stats:
            if key == "---":
                separator_count += 1

                # After flight-level data, switch to summary section
                if separator_count == 2:
                    print("\n OVERALL OPERATIONAL SUMMARY")
                continue

            print(f"{key} - {value}")
