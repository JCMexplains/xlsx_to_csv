import argparse
import logging
import sys
from datetime import date
from pathlib import Path

from xlsx_to_csv import transform_xlsx_to_csv
from config import EXCEL_PATTERN

def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity"""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_input_file(input_path: str | None, data_dir: Path) -> Path:
    """Determine input file path"""
    if input_path:
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        return input_file
    
    xlsx_files = list(data_dir.glob(EXCEL_PATTERN))
    if not xlsx_files:
        raise FileNotFoundError(
            f"No {EXCEL_PATTERN} files found in {data_dir}. "
            "Please provide an input file with -i/--input"
        )
    return xlsx_files[0]

def get_output_file(output_path: str | None, data_dir: Path) -> Path:
    """Determine output file path"""
    if output_path:
        return Path(output_path)
    return data_dir / f"{date.today().strftime('%Y-%m-%d')} data.csv"

def main():
    parser = argparse.ArgumentParser(
        description="Convert Excel files to CSV with data cleaning"
    )
    parser.add_argument("-i", "--input", help="Input Excel file path")
    parser.add_argument("-o", "--output", help="Output CSV file path")
    parser.add_argument("-v", "--verbose", action="store_true", 
                       help="Enable verbose logging")
    args = parser.parse_args()

    setup_logging(args.verbose)
    
    try:
        current_dir = Path(__file__).parent
        data_dir = current_dir / "data"
        data_dir.mkdir(exist_ok=True)
        
        input_file = get_input_file(args.input, data_dir)
        output_file = get_output_file(args.output, data_dir)
        
        logging.info(f"Input file:  {input_file}")
        logging.info(f"Output file: {output_file}")
        
        transform_xlsx_to_csv(input_file, output_file)
        logging.info("Conversion completed successfully!")
        
    except Exception as e:
        logging.error(f"Error during conversion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 