import requests
import pandas as pd
import json
import time
import random

def fetch_sec_facts_by_sic(company_data, sic_code, headers, user_start, user_end, limit=None):
    """
    Fetch SEC XBRL company facts for companies with a specific SIC code.

    Args:
        company_data (pd.DataFrame): DataFrame with company info including 'SIC' and 'cik_str' columns.
        sic_code (int): The SIC code to filter companies by.
        headers (dict): Headers to use for the SEC API request (must include User-Agent).
        user_start (int): Starting fiscal year to filter data.
        user_end (int): Ending fiscal year to filter data.
        limit (int, optional): Limit the number of CIKs to fetch. Default is None (fetch all).

    Returns:
        pd.DataFrame: Filtered DataFrame containing SEC facts.
    """
    filtered_cik_list = company_data[company_data['SIC_code'] == sic_code]['cik_str'].tolist()
    ciks = filtered_cik_list if limit is None else filtered_cik_list[:limit]

    all_data = []

    for cik in ciks:
        try:
            response = requests.get(
                f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',
                headers=headers
            )
            response.raise_for_status()
            data_dict = response.json()
            cik_val = data_dict.get('cik')
            entityName = data_dict.get('entityName')

            for taxonomy, fact_group in data_dict.get('facts', {}).items():
                for fact_name, fact_data in fact_group.items():
                    label = fact_data.get('label')
                    description = fact_data.get('description')
                    units_dict = fact_data.get('units', {})
                    for unit, records in units_dict.items():
                        for record in records:
                            row = {
                                'cik': cik_val,
                                'entityName': entityName,
                                'taxonomy': taxonomy,
                                'fact_name': fact_name,
                                'label': label,
                                'description': description,
                                'unit': unit
                            }
                            row.update(record)
                            all_data.append(row)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for CIK {cik}: {e}")
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error processing data for CIK {cik}: {e}")

        time.sleep(random.uniform(1, 2))  # Polite delay

    df = pd.DataFrame(all_data)

    # Convert 'start' and 'end' columns to datetime
    for col in ['start', 'end']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Apply filtering conditions
    if not df.empty:
        df = df[
            (df['fy'] >= user_start) &
            (df['fy'] <= user_end) &
            ((df['end'] - df['start']).dt.days > 350) &
            (df['end'].dt.year == df['fy'])
        ]

    return df