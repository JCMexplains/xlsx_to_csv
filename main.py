import argparse
import sys
import logging
from datetime import date
from pathlib import Path
from xlsx_to_csv import transform_xlsx_to_csv
import ipdb

# ipdb.set_trace()  # Add this where you want to start debugging


def setup_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Excel files to CSV with data cleaning and transformation."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input Excel file path. If not provided, will look for data*.xlsx in the data directory.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output CSV file path. If not provided, will save as [current date] data.csv in the data directory.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging output"
    )
    return parser


def main():
    parser = setup_argparser()
    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Get the directory containing the script
    current_dir = Path(__file__).parent
    data_dir = current_dir / "data"
    logging.debug(f"Current directory: {current_dir}")
    logging.debug(f"Data directory: {data_dir}")

    # Ensure data directory exists
    if not data_dir.exists():
        logging.info(f"Creating data directory: {data_dir}")
        data_dir.mkdir(exist_ok=True)

    # Determine input file
    if args.input:
        input_file = Path(args.input)
        if not input_file.exists():
            logging.error(f"Error: Input file not found: {input_file}")
            sys.exit(1)
    else:
        # Find all xlsx files that start with "data"
        xlsx_files = list(data_dir.glob("data*.xlsx"))
        if not xlsx_files:
            logging.error("No data*.xlsx files found!")
            logging.info(
                "Please place your Excel file (named 'data.xlsx' or similar) in the following directory:"
            )
            logging.info(f"  {data_dir}")
            logging.info("Or specify an input file using the -i/--input argument.")
            sys.exit(1)
        input_file = xlsx_files[0]

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        today = date.today().strftime("%Y-%m-%d")
        output_file = data_dir / f"{today} data.csv"

    logging.info(f"Input file:  {input_file}")
    logging.info(f"Output file: {output_file}")

    try:
        import ipdb; ipdb.set_trace()  # Debugger will start here
        transform_xlsx_to_csv(input_file, output_file)
        logging.info("Conversion completed successfully!")
    except Exception as e:
        logging.error(f"Error during conversion: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 