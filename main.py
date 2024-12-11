from problem_one import generate_fixed_width_file, parse_fixed_width_file
from logger import logger

def main():
    try:
        logger.info("Starting fixed-width file generation.")
        generate_fixed_width_file("fixed_width.txt", num_rows=20)

        logger.info("Starting fixed-width file parsing.")
        parse_fixed_width_file("fixed_width.txt", "output.csv")

        logger.info("Processing completed successfully.")
    except ValueError as ve:
        logger.error(f"ValueError encountered: {ve}")
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
