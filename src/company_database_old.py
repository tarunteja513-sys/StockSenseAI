
import os
import json
from config import DATA_DIR


class CompanyDatabase:

    def __init__(self):

        self.file_path = os.path.join(
            DATA_DIR,
            "company_database.json"
        )

        os.makedirs(DATA_DIR, exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file)

    def load_companies(self):

        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_companies(self, companies):

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(companies, file, indent=4)

    def add_company(self, company):

        required_fields = [
            "company",
            "symbol",
            "exchange",
            "sector"
        ]

        for field in required_fields:
            if not isinstance(company.get(field), str) or not company[field].strip():
                print("Invalid or missing field:", field)
                return False

        companies = self.load_companies()

        # Prevent duplicate exchange and symbol records
        for existing in companies:
            if (
                existing["exchange"].upper() == company["exchange"].upper()
                and existing["symbol"].upper() == company["symbol"].upper()
            ):
                print("Company already exists")
                return False

        companies.append(company)
        self.save_companies(companies)

        print(company["company"], "added successfully")
        return True

    def search_company(self, keyword):

        companies = self.load_companies()

        keyword = keyword.strip().lower()

        if not keyword:
            return []

        results = []

        for company in companies:
            if (
                keyword in company["company"].lower()
                or keyword in company["symbol"].lower()
            ):
                results.append(company)

        return results

    def update_company(self, symbol, updated_data, exchange="NSE"):

        companies = self.load_companies()

        for company in companies:

            if (
                company["symbol"].upper() == symbol.upper()
                and company["exchange"].upper() == exchange.upper()
            ):

                company.update(updated_data)

                self.save_companies(companies)

                print("Company updated successfully")
                return True

        print("Company not found")
        return False

    def display_all(self):

        companies = self.load_companies()

        print("\nTOTAL COMPANIES:", len(companies))

        for company in companies:
            print(
                company["company"],
                "|",
                company["symbol"],
                "|",
                company["exchange"]
            )
