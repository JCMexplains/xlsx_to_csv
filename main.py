import argparse
import sys
from pathlib import Path
from xlsx_to_csv import transform_xlsx_to_csv


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
        help="Output CSV file path. If not provided, will save as data.csv in the data directory.",
    )
    return parser


def main():
    parser = setup_argparser()
    args = parser.parse_args()

    # Get the directory containing the script
    current_dir = Path(__file__).parent
    data_dir = current_dir / "data"

    # Ensure data directory exists
    if not data_dir.exists():
        print(f"Creating data directory: {data_dir}")
        data_dir.mkdir(exist_ok=True)

    # Determine input file
    if args.input:
        input_file = Path(args.input)
        if not input_file.exists():
            print(f"Error: Input file not found: {input_file}")
            sys.exit(1)
    else:
        # Find all xlsx files that start with "data"
        xlsx_files = list(data_dir.glob("data*.xlsx"))
        if not xlsx_files:
            print("No data*.xlsx files found!")
            print(
                "Please place your Excel file (named 'data.xlsx' or similar) in the following directory:"
            )
            print(f"  {data_dir}")
            print("Or specify an input file using the -i/--input argument.")
            sys.exit(1)
        input_file = xlsx_files[0]

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = data_dir / "data.csv"

    print(f"Input file:  {input_file}")
    print(f"Output file: {output_file}")

    try:
        transform_xlsx_to_csv(input_file, output_file)
        print("Conversion completed successfully!")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 