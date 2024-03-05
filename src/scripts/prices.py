import urllib.request as request
import json
from concurrent.futures import ThreadPoolExecutor,as_completed
import sqlite3
import os
import time
from datetime import datetime

def fetch_current_time():
    return datetime.now().strftime('%x %H:%M:%S')

def save_to_file(itemlist,filename):
    with open(filename, 'w') as f:
        for item in itemlist:
            f.write("%s\n" % item)

def get_virtual_machine_sku_prices(region, jsondata):
    skus = list(jsondata['skus'].keys()) 
    found_price_count=0
    not_found_price_count=0
    sku_os=[]
    offers = []
    for sku in skus:
        pricing_types = jsondata['skus'][sku].keys()
        for pricing_type in pricing_types:
            for offer_info_data in jsondata['skus'][sku][pricing_type]:
                
                offer_info = offer_info_data.split('--')
                offer_sku = offer_info[0]
                offer_sku_info = sku.split('-')
                os_name = offer_sku_info[0]
                if os_name not in sku_os:
                    sku_os.append(os_name)
                offer_type = offer_info[1]
                try :
                    price = jsondata['offers'][offer_sku]['prices'][offer_type][region]['value']
                    
                    found_price_count += 1
                    # create and return offer object
                    offer = {
                        'sku': sku,
                        'pricing_type': pricing_type,
                        'offer_sku': offer_sku,
                        'offer_type': offer_type,
                        'region': region,
                        'price': price
                    }
                    offers.append(offer)
                    #print(f"sku: {sku}, pricing_type: {pricing_type}, offer_sku: {offer_sku}, offer_type: {offer_type}, price: {price}")
                except KeyError:
                    not_found_price_count += 1
                    #print(f"Price information not available for sku: {sku}, pricing_type: {pricing_type}, in region: {region}")
                except:
                    print(f"Error occurred while processing sku: {sku}, pricing_type: {pricing_type}, in region: {region}")

    #print(f"Number of skus: {len(skus)}")
    #print(f"Number of prices found for region {region}: {found_price_count}")
    #print(f"Number of skus without a price for region {region}: {not_found_price_count}")
    #print(f'List of OS: {", ".join(map(str, set(sku_os)))},')
    return offers

def export_offers_to_json(offers, filename):
    with open(filename, 'w') as f:
        json.dump(offers, f, indent=4)

def generate_insert_statement(table_name, dict_list):
    if not dict_list:
        return None  # Return None if the list is empty

    # Assuming all dictionaries in the list have the same structure
    keys = dict_list[0].keys()
    columns = ', '.join(keys)
    placeholders = ', '.join(['?'] * len(keys))  # Create placeholders based on the number of keys

    return f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

def reset_database(db_file):
    # Check if the database file exists and remove it
    if os.path.exists(db_file):
        os.remove(db_file)

def create_table_if_not_exists(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    # Adjust the column definitions according to your data structure
    c.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT,
            pricing_type TEXT,
            offer_sku TEXT,
            offer_type TEXT,
            region TEXT,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_offers_into_db(offers, db_file='virtual_machine_prices.db'):
    insert_statement = generate_insert_statement('offers', offers)
    print(f'Insert statement: {insert_statement}')
    if not insert_statement:
        print('statment is empty, no data to insert into the database. Exiting...')
        return
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    if offers and isinstance(offers[0], dict):
        keys = offers[0].keys()
        offers = [tuple(offer[key] for key in keys) for offer in offers]
    c.executemany(insert_statement, offers)
    
    conn.commit()
    conn.close()

def count_table_rows(db_file, table_name):
    """
    Count the number of rows in a given table within a SQLite database.

    Parameters:
    db_path (str): The file path to the SQLite database.
    table_name (str): The name of the table to count rows in.

    Returns:
    int: The number of rows in the specified table.
    """
    # Establish a connection to the SQLite database
    conn = sqlite3.connect(db_file)

    # Create a cursor object
    cur = conn.cursor()

    # SQL query to count the number of rows in the table
    query = f'SELECT COUNT(*) FROM {table_name}'

    # Execute the query
    cur.execute(query)

    # Fetch the result
    number_of_rows = cur.fetchone()[0]

    # Close the connection
    conn.close()

    # Return the number of rows
    return number_of_rows

def main():
    # Record the start time
    start_time = time.time()
    print(f'[{fetch_current_time()}] Script started')
    virtual_machine_calculator_api = 'https://azure.microsoft.com/api/v3/pricing/virtual-machines/calculator/?culture=en-us&currency=$currency'
    db_file='virtual_machine_prices.db'
    response=request.urlopen(virtual_machine_calculator_api)
    data = response.read()
    jsondata = json.loads(data)
    regions  = list(map(lambda region: region['slug'], jsondata['regions']))
    offers = []

    print(f'[{fetch_current_time()}] Number of regions to work on: {len(regions)}')


    with ThreadPoolExecutor(max_workers=len(regions)) as executor:
        # Submit tasks to the executor
        future_to_region = {executor.submit(get_virtual_machine_sku_prices, region, jsondata): region for region in regions}

        # Process as they complete
        for future in as_completed(future_to_region):
            region = future_to_region[future]
            try:
                region_offers = future.result()
                offers.extend(region_offers)
            except Exception as exc:
                print(f'{region} generated an exception: {exc}')
    print(f'[{fetch_current_time()}] Generated {len(offers)} offers in total. writing to database...')
    # reset the database in each run
    reset_database(db_file)

    # Create the table if it does not exist    
    create_table_if_not_exists(db_file)

    print(f'[{fetch_current_time()}] Created the table "offers" in the database "{db_file}".')
    # Insert the offers into a sqlite database    
    insert_offers_into_db(offers,db_file)

    # Count the number of rows in the table
    count_of_offers_inserted = count_table_rows(db_file, 'offers')
    # Print the result
    print(f'[{fetch_current_time()}] Number of rows in the "offers" table: {count_of_offers_inserted}')
    # Record the end time
    end_time = time.time()

    # Calculate the duration
    duration = end_time - start_time

    # Print the duration
    print(f'[{fetch_current_time()}] Duration: {duration:.2f} seconds')
if __name__ == '__main__':
    main()
