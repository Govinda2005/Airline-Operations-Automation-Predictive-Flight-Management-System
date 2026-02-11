from datetime import date

class Reporter:
    def generate(self, content):
        path = f"output/reports/aviation_report_{date.today()}.txt"
        with open(path, "w") as f:
            f.write(content)
