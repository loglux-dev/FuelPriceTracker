from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
from datetime import datetime


class FuelPriceFetcher:
    def __init__(self, initial_url, api_url, spreadsheet_id, sheet_name, creds_file):
        self.initial_url = initial_url
        self.api_url = api_url
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        self.cookies = None
        self.creds = service_account.Credentials.from_service_account_file(
            creds_file,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.service = build('sheets', 'v4', credentials=self.creds)

    def get_cookies(self):
        try:
            response = self.session.get(self.initial_url, headers=self.headers)
            if response.status_code == 200:
                self.cookies = self.session.cookies
                print("Retrieved cookies:")
                for cookie in self.cookies:
                    print(f"{cookie.name}: {cookie.value}")
            else:
                print(f"Failed to retrieve cookies, status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while retrieving cookies: {e}")

    def fetch_prices(self):
        try:
            response = self.session.get(self.api_url, headers=self.headers, cookies=self.cookies)
            if response.status_code == 200:
                json_response = response.json()
                print("\nJSON Response:")
                print(json_response)

                if json_response.get('status') == 'OK':
                    return json_response['data']['prices']
                else:
                    print("Response status is not OK.")
                    return None
            else:
                print(f"Error with request to API: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred while fetching prices: {e}")
            return None

    def setup_sheet_headers(self):
        try:
            # Check if headers already exist
            sheet = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f'{self.sheet_name}!A1:D1'
            ).execute()

            if not sheet.get('values'):
                # If no headers, set them
                headers = [['Date', 'VLSFO', 'LSMGO', 'HSFO']]
                body = {
                    'values': headers
                }
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f'{self.sheet_name}!A1:D1',
                    valueInputOption='RAW',
                    body=body
                ).execute()
                print("Headers added to the Google Sheet.")
            else:
                print("Headers already exist in the Google Sheet.")

        except Exception as e:
            print(f"An error occurred while setting up headers: {e}")

    def update_google_sheet(self, data):
        if data:
            try:
                # Get the current date
                current_date = datetime.now().strftime("%Y-%m-%d")

                # Prepare the row to insert into Google Sheet
                row_data = [current_date]  # Start with the date

                # Create a mapping of fuel types to prices
                fuel_price_mapping = {price['fuelGroupName']: price['currentPrice'] for price in data}

                # Define the fuel types expected to maintain order
                fuel_types = ["VLSFO", "LSMGO", "HSFO"]

                # Append prices for each fuel type to the row data
                for fuel_type in fuel_types:
                    row_data.append(fuel_price_mapping.get(fuel_type, "N/A"))  # "N/A" if no data for that type

                # Append the new row at the end of the sheet
                body = {
                    'values': [row_data]
                }
                result = self.service.spreadsheets().values().append(
                    spreadsheetId=self.spreadsheet_id,
                    range=self.sheet_name,  # Specifying the sheet name for clarity
                    valueInputOption='RAW',
                    insertDataOption='INSERT_ROWS',
                    body=body
                ).execute()

                print(f"{result.get('updates').get('updatedCells')} cells updated in Google Sheet.")
            except Exception as e:
                print(f"An error occurred while updating Google Sheet: {e}")

    def run(self):
        self.get_cookies()
        self.setup_sheet_headers()  # Ensure headers are set before inserting data
        prices = self.fetch_prices()
        self.update_google_sheet(prices)


# Example usage
initial_url = 'https://integr8fuels.com/bunkering-ports/bunkering-singapore/'
api_url = 'https://integr8fuels.com/wp-admin/admin-ajax.php?action=getLatestPriceByPortFuels&portId=2615'
spreadsheet_id = 'your-google-sheet-id'  # Replace with your actual Google Sheet ID
sheet_name = 'your-sheet-name'           # Replace with your actual sheet name
creds_file = 'path/to/your/service_account.json'  # Replace with the path to your JSON key file

fetcher = FuelPriceFetcher(initial_url, api_url, spreadsheet_id, sheet_name, creds_file)
fetcher.run()
