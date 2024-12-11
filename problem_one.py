import json
import csv
import random
import string
import os
from logger import logger
from typing import Union

# Load spec at the top of the script
with open(os.path.join(os.getcwd(), "spec.json"), "r") as f:
    SPEC = json.load(f)

# Extract configuration values from the loaded JSON spec
COLUMN_NAMES: list[str] = SPEC["ColumnNames"]
OFFSETS: list[int] = list(map(int, SPEC["Offsets"]))
FIXED_WIDTH_ENCODING: str = SPEC["FixedWidthEncoding"]
DELIMITED_ENCODING: str = SPEC["DelimitedEncoding"]
INCLUDE_HEADER: bool = SPEC["IncludeHeader"] == "True"
TOTAL_WIDTH: int = sum(OFFSETS)

def generate_random_string(length: int) -> str:
    """
    Generate a random alphanumeric string of the specified length.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_fixed_width_file(output_path: Union[str, os.PathLike], num_rows: int = 10) -> None:
    """
    Generate a fixed-width file based on the spec and write it to the specified path.
    """
    # Open the specified file path for writing with the defined encoding
    with open(output_path, 'w', encoding=FIXED_WIDTH_ENCODING) as fwf:
        # If INCLUDE_HEADER is True, generate and write the header row
        if INCLUDE_HEADER:
            # Create the header row by formatting each column name to match the corresponding offset
            header = "".join([name.ljust(offset)[:offset] for name, offset in zip(COLUMN_NAMES, OFFSETS)])
            fwf.write(header + "\n")
            logger.info("Header written to fixed-width file.")

        # Loop to generate the specified number of data rows
        for i in range(num_rows):
            # Generate each row by creating random strings of the required length for each field
            row = "".join([
                generate_random_string(offset).ljust(offset)[:offset] for offset in OFFSETS
            ])
            # Write the generated row to the file
            fwf.write(row + "\n")
            logger.info(f"Row {i + 1} written to fixed-width file.")


def parse_fixed_width_file(input_path: Union[str, os.PathLike], output_path: Union[str, os.PathLike]) -> None:
    """
    Parse a fixed-width file and write its content to a CSV file.
    """
    # Open the input fixed-width file for reading and the output CSV file for writing
    with open(input_path, 'r', encoding=FIXED_WIDTH_ENCODING) as fwf, open(output_path, 'w', encoding=DELIMITED_ENCODING, newline='') as csvfile:
        lines = fwf.readlines()

        # If the file is empty, raise a ValueError to notify the user
        if not lines:
            raise ValueError(f"The input file {input_path} is empty.")

        # Initialize a CSV writer object to write parsed data into the output CSV file
        writer = csv.writer(csvfile)

        # If the header is to be included, write the column names to the CSV file
        if INCLUDE_HEADER:
            writer.writerow(COLUMN_NAMES)
            logger.info("Header written to CSV file.")

        # Iterate through each line of the fixed-width file
        for line_num, line in enumerate(lines):
            # Skip the first line if it contains a header (already written to CSV)
            if line_num == 0 and INCLUDE_HEADER:
                continue

            # Skip lines that are entirely empty and log a warning
            if not line.strip():
                logger.warning(f"Skipping empty line at line {line_num + 1}")
                continue

            # Raise a ValueError if a line is shorter than the total expected width
            if len(line.strip()) < TOTAL_WIDTH:
                raise ValueError(f"Line {line_num + 1} is shorter than expected width of {TOTAL_WIDTH} characters")

            # Truncate the line to the expected fixed width to handle any extra characters
            parsed_line = line[:TOTAL_WIDTH]

            # Initialize variables to parse the fixed-width fields
            start = 0
            row = []

            # Extract each field using the offsets specified in the configuration
            for offset in OFFSETS:
                # Slice the line to get the field and strip any whitespace
                row.append(parsed_line[start:start + offset].strip())
                # Update the starting index for the next field
                start += offset

            # Write the parsed row to the CSV file
            writer.writerow(row)

        # Log a message indicating that the parsing process has completed
        logger.info(f"Parsed fixed-width file and wrote to CSV: {output_path}")