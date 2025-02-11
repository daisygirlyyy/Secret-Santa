import csv
import random
from typing import List, Dict
from pathlib import Path
from .utils import validate_csv, handle_errors


class SecretSanta:
    def __init__(self, employees_file: str, previous_assignments_file: str = None):
        self.employees_file = employees_file
        self.previous_assignments_file = previous_assignments_file
        self.employees = self._load_employees()
        self.previous_assignments = self._load_previous_assignments()

    @handle_errors
    def _load_employees(self) -> List[Dict[str, str]]:
        """Load employee data from the CSV file."""
        validate_csv(self.employees_file, ["Employee_Name", "Employee_EmailID"])
        with open(self.employees_file, mode="r") as file:
            return list(csv.DictReader(file))

    @handle_errors
    def _load_previous_assignments(self) -> Dict[str, str]:
        """Load previous assignments from the CSV file."""
        if not self.previous_assignments_file:
            return {}
        validate_csv(self.previous_assignments_file, ["Employee_EmailID", "Secret_Child_EmailID"])
        with open(self.previous_assignments_file, mode="r") as file:
            return {row["Employee_EmailID"]: row["Secret_Child_EmailID"] for row in csv.DictReader(file)}

    def _generate_assignments(self) -> List[Dict[str, str]]:
        """Generate Secret Santa assignments."""
        employees = self.employees.copy()
        random.shuffle(employees)

        assignments = []
        for i, employee in enumerate(employees):
            secret_child = employees[(i + 1) % len(employees)]
            # Ensure no employee is assigned to themselves or their previous secret child
            while (secret_child["Employee_EmailID"] == employee["Employee_EmailID"] or
                   self.previous_assignments.get(employee["Employee_EmailID"]) == secret_child["Employee_EmailID"]):
                random.shuffle(employees)
                secret_child = employees[(i + 1) % len(employees)]

            assignments.append({
                "Employee_Name": employee["Employee_Name"],
                "Employee_EmailID": employee["Employee_EmailID"],
                "Secret_Child_Name": secret_child["Employee_Name"],
                "Secret_Child_EmailID": secret_child["Employee_EmailID"]
            })

        return assignments

    @handle_errors
    def save_assignments(self, output_file: str) -> None:
        """Save the generated assignments to a CSV file."""
        assignments = self._generate_assignments()
        with open(output_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"])
            writer.writeheader()
            writer.writerows(assignments)