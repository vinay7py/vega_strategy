# vega_strategy


This project implements a Vega Strategy for options trading using Python.

## Project Structure

- `data/`: Contains data files like instruments.csv and vega_vomma_data.csv.
- `scripts/`: Contains Python modules for data retrieval, Greek calculations, strategy implementation, and report generation.
- `main.py`: Main script to run the strategy.
- `README.md`: Project documentation.
- `requirements.txt`: Python dependencies.

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Add your Zerodha credentials in `main.py`.
4. Run the main script: `python main.py`.

## Modules

### data_retrieval.py
Handles data fetching from the Zerodha Kite API.

### greeks_calculations.py
Contains functions for calculating Greek values like Vega and Vomma.

### vega_strategy.py
Implements the main Vega Strategy.

### report_generation.py
Generates a summary report of the Vega and Vomma changes.

## Usage

Run the strategy by executing `main.py`. The script will continuously monitor the market and log Vega and Vomma changes to a CSV file. A summary report is generated upon termination.
