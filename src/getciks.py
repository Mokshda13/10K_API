import requests
import pandas as pd

def get_company_data_with_sic(sic_csv_path, headers=None):
    """
    Fetch SEC company ticker data and merge it with SIC codes from a local CSV.

    Args:
        sic_csv_path (str): Path to the CSV file that contains 'cik_str' and 'SIC_code'.
        headers (dict, optional): Headers for SEC API requests. Defaults to standard User-Agent.

    Returns:
        pd.DataFrame: Merged DataFrame with SEC ticker data and SIC codes.
    """
    if headers is None:
        headers = {'User-Agent': 'your.email@example.com'}

    try:
        # Fetch company tickers from SEC
        response = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers=headers
        )
        response.raise_for_status()

        # Load into DataFrame
        company_data = pd.DataFrame.from_dict(response.json(), orient='index')
        company_data['cik_str'] = company_data['cik_str'].astype(str).str.zfill(10)

        # Load and clean your local SIC mapping
        sic_mapping = pd.read_csv(sic_csv_path)
        sic_mapping['cik_str'] = sic_mapping['cik_str'].astype(str).str.zfill(10)
        sic_mapping['SIC_code'] = (
            sic_mapping['SIC_code']
            .fillna(0)
            .astype(float)
            .astype(int)
            .astype(str)
        )

        # Merge on cik_str
        merged_data = pd.merge(company_data, sic_mapping, on='cik_str', how='left')
        return merged_data

    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"Error retrieving or processing company data: {e}")
        return pd.DataFrame()
