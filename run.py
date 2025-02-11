from src.secret_santa import SecretSanta


def main():
    employees_file = "data/employees.csv"
    previous_assignments_file = "data/previous_assignments.csv"
    output_file = "output/assignments.csv"

    secret_santa = SecretSanta(employees_file, previous_assignments_file)
    secret_santa.save_assignments(output_file)
    print(f"Secret Santa assignments saved to {output_file}")


if __name__ == "__main__":
    main()