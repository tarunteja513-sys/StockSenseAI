
import requests
import csv
import io
import os
from config import DATA_DIR


class NSEImporter:

    def __init__(self):
        self.url = (
            "https://nsearchives.nseindia.com/"
            "content/equities/EQUITY_L.csv"
        )

        self.output_file = os.path.join(
            DATA_DIR,
            "nse_companies.csv"
        )

    def download_company_list(self):

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/csv,*/*"
        }

        try:
            response = requests.get(
                self.url,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            if not response.content:
                raise ValueError("Empty response")

            text = response.content.decode(
                "utf-8-sig"
            )

            reader = csv.DictReader(io.StringIO(text))

            if not reader.fieldnames:
                raise ValueError("Invalid CSV format")

            required = {"SYMBOL", "NAME OF COMPANY"}

            if not required.issubset(set(reader.fieldnames)):
                raise ValueError(
                    "Unexpected NSE CSV columns"
                )

            companies = list(reader)

            if not companies:
                raise ValueError("No company records found")

            with open(
                self.output_file,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=reader.fieldnames
                )

                writer.writeheader()
                writer.writerows(companies)

            print("NSE company list downloaded!")
            print("Total records:", len(companies))
            print("Saved at:", self.output_file)

            return companies

        except (requests.RequestException, ValueError) as error:

            print("NSE download failed:", error)
            return []


if __name__ == "__main__":

    importer = NSEImporter()
    importer.download_company_list()
