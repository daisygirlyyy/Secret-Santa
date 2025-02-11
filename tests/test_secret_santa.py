import unittest
import csv
from src.secret_santa import SecretSanta


class TestSecretSanta(unittest.TestCase):
    def setUp(self):
        self.employees_file = "data/employees.csv"
        self.previous_assignments_file = "data/previous_assignments.csv"
        self.output_file = "output/test_assignments.csv"

    def test_assignments(self):
        secret_santa = SecretSanta(self.employees_file, self.previous_assignments_file)
        secret_santa.save_assignments(self.output_file)

        with open(self.output_file, mode="r") as file:
            reader = csv.DictReader(file)
            assignments = list(reader)

        self.assertEqual(len(assignments), len(secret_santa.employees))
        for assignment in assignments:
            self.assertNotEqual(assignment["Employee_EmailID"], assignment["Secret_Child_EmailID"])


if __name__ == "__main__":
    unittest.main()