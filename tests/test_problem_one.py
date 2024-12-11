import pytest
from problem_one import generate_random_string, generate_fixed_width_file, parse_fixed_width_file
import os
import csv

# Constants for testing
COLUMN_NAMES = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10"]
OFFSETS = [5, 12, 3, 2, 13, 7, 10, 13, 20, 13]
TOTAL_WIDTH = sum(OFFSETS)
FIXED_WIDTH_ENCODING = "windows-1252"
DELIMITED_ENCODING = "utf-8"
INCLUDE_HEADER = True


# Test: generate_random_string
def test_generate_random_string():
    """Test that generate_random_string generates a string of correct length and type."""
    result = generate_random_string(10)
    assert len(result) == 10
    assert all(c.isalnum() for c in result)  # Ensure all characters are alphanumeric

    # Edge case: zero length
    result = generate_random_string(0)
    assert result == ""


# Test: generate_fixed_width_file
def test_generate_fixed_width_file_header(tmp_path):
    """Test that generate_fixed_width_file writes the correct header."""
    output_path = tmp_path / "test_fixed_width.txt"
    generate_fixed_width_file(output_path, num_rows=0)

    with open(output_path, "r", encoding=FIXED_WIDTH_ENCODING) as f:
        header = f.readline().strip()

    if INCLUDE_HEADER:
        expected_header = "".join(
            [name.ljust(offset)[:offset] for name, offset in zip(COLUMN_NAMES, OFFSETS)]
        ).rstrip()
        assert header == expected_header
    else:
        assert header == ""


def test_generate_fixed_width_file_rows(tmp_path):
    """Test that generate_fixed_width_file generates rows of correct format."""
    output_path = tmp_path / "test_fixed_width.txt"
    num_rows = 5
    generate_fixed_width_file(output_path, num_rows=num_rows)

    with open(output_path, "r", encoding=FIXED_WIDTH_ENCODING) as f:
        lines = f.readlines()

    if INCLUDE_HEADER:
        assert len(lines) == num_rows + 1  # Header + rows
    else:
        assert len(lines) == num_rows

    # Verify the length of each row
    for line in lines[1 if INCLUDE_HEADER else 0:]:
        assert len(line.strip()) == TOTAL_WIDTH


# Test: parse_fixed_width_file
def test_parse_fixed_width_file(tmp_path):
    """Test that parse_fixed_width_file correctly converts a fixed-width file to CSV."""
    fixed_width_path = tmp_path / "test_fixed_width.txt"
    csv_output_path = tmp_path / "test_output.csv"

    # Generate a fixed-width file and parse it
    num_rows = 5
    generate_fixed_width_file(fixed_width_path, num_rows=num_rows)
    parse_fixed_width_file(fixed_width_path, csv_output_path)

    # Verify the CSV file
    with open(csv_output_path, "r", encoding=DELIMITED_ENCODING) as f:
        reader = csv.reader(f)
        rows = list(reader)

    if INCLUDE_HEADER:
        assert rows[0] == COLUMN_NAMES  # Header
        rows = rows[1:]  # Exclude header for further testing

    # Verify number of rows and fields
    assert len(rows) == num_rows
    for row in rows:
        assert len(row) == len(COLUMN_NAMES)


# Edge Case: Empty Fixed-Width File
def test_empty_fixed_width_file(tmp_path):
    """Test parsing an empty fixed-width file."""
    fixed_width_path = tmp_path / "empty_fixed_width.txt"
    csv_output_path = tmp_path / "empty_output.csv"

    # Create an empty file
    fixed_width_path.touch()

    with pytest.raises(ValueError, match="The input file .* is empty"):
        parse_fixed_width_file(fixed_width_path, csv_output_path)


# Edge Case: Short Rows in Fixed-Width File
def test_short_rows_in_fixed_width_file(tmp_path):
    """Test parsing a fixed-width file with rows shorter than TOTAL_WIDTH."""
    fixed_width_path = tmp_path / "short_rows_fixed_width.txt"
    csv_output_path = tmp_path / "short_output.csv"

    # Create a file with short rows
    with open(fixed_width_path, "w", encoding=FIXED_WIDTH_ENCODING) as f:
        if INCLUDE_HEADER:
            header = "".join(
                [name.ljust(offset)[:offset] for name, offset in zip(COLUMN_NAMES, OFFSETS)]
            )
            f.write(header + "\n")
        f.write("Short\n")  # Shorter than TOTAL_WIDTH

    with pytest.raises(ValueError) as exc_info:
        parse_fixed_width_file(fixed_width_path, csv_output_path)
    assert "is shorter than expected width" in str(exc_info.value)


# Edge Case: Rows with Extra Characters
def test_extra_characters_in_fixed_width_file(tmp_path):
    """Test parsing a fixed-width file with rows longer than TOTAL_WIDTH."""
    fixed_width_path = tmp_path / "extra_chars_fixed_width.txt"
    csv_output_path = tmp_path / "extra_output.csv"

    # Create a file with extra characters in rows
    with open(fixed_width_path, "w", encoding=FIXED_WIDTH_ENCODING) as f:
        if INCLUDE_HEADER:
            header = "".join(
                [name.ljust(offset)[:offset] for name, offset in zip(COLUMN_NAMES, OFFSETS)]
            )
            f.write(header + "\n")
        f.write("A" * TOTAL_WIDTH + "ExtraData\n")  # Extra characters beyond TOTAL_WIDTH

    parse_fixed_width_file(fixed_width_path, csv_output_path)

    # Verify output
    with open(csv_output_path, "r", encoding=DELIMITED_ENCODING) as f:
        rows = list(csv.reader(f))
        if INCLUDE_HEADER:
            assert rows[0] == COLUMN_NAMES  # Header row
            rows = rows[1:]  # Exclude header for further testing
        assert len(rows) == 1  # Only one data row
        assert len(rows[0]) == len(COLUMN_NAMES)  # Correct number of columns


# Edge Case: Handling of Empty Lines
def test_empty_lines_in_fixed_width_file(tmp_path):
    """Test parsing a fixed-width file with empty lines."""
    fixed_width_path = tmp_path / "empty_lines_fixed_width.txt"
    csv_output_path = tmp_path / "empty_lines_output.csv"

    # Create a file with empty lines
    with open(fixed_width_path, "w", encoding=FIXED_WIDTH_ENCODING) as f:
        if INCLUDE_HEADER:
            header = "".join(
                [name.ljust(offset)[:offset] for name, offset in zip(COLUMN_NAMES, OFFSETS)]
            )
            f.write(header + "\n")
        f.write("A" * TOTAL_WIDTH + "\n")  # Valid row
        f.write("\n")  # Empty line
        f.write("B" * TOTAL_WIDTH + "\n")  # Another valid row

    parse_fixed_width_file(fixed_width_path, csv_output_path)

    # Verify output
    with open(csv_output_path, "r", encoding=DELIMITED_ENCODING) as f:
        rows = list(csv.reader(f))
        if INCLUDE_HEADER:
            assert rows[0] == COLUMN_NAMES  # Header row
            rows = rows[1:]  # Exclude header for further testing
        assert len(rows) == 2  # Only valid rows are included
