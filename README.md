# FuelPriceTracker

FuelPriceTracker is a Python script that automates the process of fetching fuel prices from an online source and updating them in a Google Sheet. This tool is ideal for tracking fuel price trends over time and is designed to be easily integrated into automated workflows.

## Features

- **Automated Data Retrieval**: Fetches the latest fuel prices for VLSFO, LSMGO, and HSFO from a specified online source.
- **Google Sheets Integration**: Updates a Google Sheet with the fetched data, including the date and time of the request.
- **Historical Tracking**: Appends new data to the sheet daily, allowing for trend analysis over time.
- **Automatic Header Setup**: Automatically adds headers to the Google Sheet if they do not exist, facilitating quick setup and deployment.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your machine.
- Access to the Google Cloud Platform with a service account and a downloaded JSON key file.
- Google Sheets API enabled for your Google Cloud project.
- A Google Sheet prepared or ready to be created by the script.

## Installation

**Clone the Repository**

   Clone this repository to your local machine using the following command:

   ```bash
   git clone https://github.com/loglux-dev/FuelPriceTracker.git
    ```
   
**Install the Required Packages**
```bash
cd FuelPriceTracker
pip install -r requirements.txt 
```

## Usage

### Edit Configuraton
Open the FuelPriceTracker.py script and update the following variables with your information:

```python
spreadsheet_id = 'your-google-sheet-id'  # Replace with your actual Google Sheet ID
sheet_name = 'your-sheet-name'           # Replace with your actual sheet name
creds_file = 'path/to/your/service_account.json'  # Replace with the path to your JSON key f
```
### Run the Script

Execute the script by running the following command:
    ```bash
    python fuel_price_tracker.py
    ```
## Automate Daily Execution
    - Use a task scheduler like `cron` to run the script daily at a specified time.
    - For example, to run the script every day at 8:00 AM, add the following line to your crontab:
    ```bash
    0 8 * * * /usr/bin/python3 /path/to/fuel_price_tracker.py
    ```
## License
This project is licensed under the MIT License - see the LICENSE file for details.


