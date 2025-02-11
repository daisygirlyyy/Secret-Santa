import csv  # Add this import
import os
from functools import wraps
from typing import List


def validate_csv(file_path: str, required_columns: List[str]) -> None:
    """Validate that the CSV file contains the required columns."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        if not all(column in reader.fieldnames for column in required_columns):
            raise ValueError(f"CSV file must contain the following columns: {required_columns}")


def handle_errors(func):
    """Decorator to handle errors in methods."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return wrapper


def ensure_directory_exists(file_path: str) -> None:
    """Ensure the directory for the output file exists."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)