import pandas as pd

from getciks import get_company_data_with_sic

headers = {'User-Agent': "mbambal@purdue.edu"}

sic_mapping_file = '/Users/mayankbambal/Desktop/10K_API/data/mapping/company_tickers.csv'

company_data = get_company_data_with_sic(sic_mapping_file, headers)

# Get user input

sic_code = input("Enter SIC code: ")
user_start = int(input("Enter start period (YYYY): "))
user_end = int(input("Enter end period (YYYY): "))

#Download data

from datadownloader import fetch_sec_facts_by_sic
data_10k = fetch_sec_facts_by_sic(company_data, sic_code, headers, user_start, user_end, limit=5)


# Save data to csv
data_10k.to_csv(f'{sic_code}_{user_start}_{user_end}data_10k.csv', index=False)
