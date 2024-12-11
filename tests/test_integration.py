import pytest
from problem_one import generate_fixed_width_file, parse_fixed_width_file

def test_full_integration(tmp_path):
    fixed_width_path = tmp_path / "test_fixed_width.txt"
    csv_output_path = tmp_path / "test_output.csv"

    # Generate and parse fixed-width file
    generate_fixed_width_file(fixed_width_path, num_rows=10)
    parse_fixed_width_file(fixed_width_path, csv_output_path)

    # Verify output
    with open(csv_output_path, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 11  # 1 header + 10 rows
