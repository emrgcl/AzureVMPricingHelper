import urllib.request as request
import datetime
import json
import os
import sqlite3


def fetch_current_time():
    return datetime.now().strftime('%x %H:%M:%S')

def save_to_file(itemlist,filename):
    with open(filename, 'w') as f:
        for item in itemlist:
            f.write("%s\n" % item)
def fetch_virtual_machine_sku_prices(virtual_machine_calculator_api='https://azure.microsoft.com/api/v3/pricing/virtual-machines/calculator/?culture=en-us&currency=$currency'):
        try:
            response=request.urlopen(virtual_machine_calculator_api)
            data = response.read()
            jsondata = json.loads(data)
            return jsondata
        except Exception as e:
            print(f"Error occurred while fetching virtual machine prices: {e}")
        
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

vm_series = {
    "all": "All",
    "av2": "Av2 Standard",
    "basv2": "Basv2-series",
    "bs": "Bs-series",
    "bsv2": "Bsv2-series",
    "constrained": "Constrained vCPUs capable",
    "dadsv5": "Dadsv5-series",
    "dadsv6": "Dadsv6-series",
    "daldsv6": "Daldsv6-series",
    "dalsv6": "Dalsv6-series",
    "dasv4": "Dasv4-series",
    "dasv5": "Dasv5-series",
    "dasv6": "Dasv6-series",
    "dav4": "Dav4-series",
    "dcadsv5": "DCadsv5-series",
    "dcasv5": "DCasv5-series",
    "dcdsv3": "DCdsv3-series",
    "dcsv2": "DCsv2-series",
    "dcsv3": "DCsv3-series",
    "ddsv4": "Ddsv4-series",
    "ddsv5": "Ddsv5-series",
    "ddv4": "Ddv4-series",
    "ddv5": "Ddv5-series",
    "dldsv5": "Dldsv5-series",
    "dlsv5": "Dlsv5-series",
    "dsv2": "Dsv2-series",
    "dsv3": "Dsv3-series",
    "dsv4": "Dsv4-series",
    "dsv5": "Dsv5-series",
    "dv2": "Dv2-series",
    "dv3": "Dv3-series",
    "dv4": "Dv4-series",
    "dv5": "Dv5-series",
    "eadsv5": "Eadsv5-series",
    "eadsv6": "Eadsv6-series",
    "easv4": "Easv4-series",
    "easv5": "Easv5-series",
    "easv6": "Easv6-series",
    "eav4": "Eav4-series",
    "ebdsv5": "Ebdsv5-series",
    "ebsv5": "Ebsv5-series",
    "ecadsv5": "ECadsv5-series",
    "ecasv5": "ECasv5-series",
    "edsv4": "Edsv4-series",
    "edsv5": "Edsv5-series",
    "edv4": "Edv4-series",
    "edv5": "Edv5-series",
    "esv3": "Esv3-series",
    "esv4": "Esv4-series",
    "esv5": "Esv5-series",
    "ev3": "Ev3-series",
    "ev4": "Ev4-series",
    "ev5": "Ev5-series",
    "f": "F-series",
    "falsv6": "Falsv6-series",
    "famsv6": "Famsv6-series",
    "fasv6": "Fasv6-series",
    "fs": "Fs-series",
    "fsv2": "Fsv2-series",
    "fx": "FX-series",
    "g": "G-series",
    "gs": "Gs-series",
    "h": "H-series",
    "hb": "HB-series",
    "hbv2": "HBv2-series",
    "hbv3": "HBv3-series",
    "hbv4": "HBv4-series",
    "hc": "HC-series",
    "hx": "HX-series",
    "lasv3": "Lasv3-series",
    "ls": "Ls-series",
    "lsv2": "Lsv2-series",
    "lsv3": "Lsv3-series",
    "m": "M-series",
    "mdsv2": "Mdsv2-series",
    "mdsv3": "Mdsv3-series",
    "msv2": "Msv2-series",
    "msv3": "Msv3-series",
    "mv2": "Mv2-series",
    "nc": "NC-series",
    "nca100v4": "NCA100v4-series",
    "nca10v4": "NCadsA10v4-series",
    "ncast4v3": "NCas_T4_v3-series",
    "ncsv2": "NCsv2-series",
    "ncsv3": "NCsv3-series",
    "ndasrv4": "NDA100v4-series",
    "ndamsrv4": "NDmA100v4-series",
    "nds": "NDs-series",
    "ndv2": "NDv2-series",
    "ngadsv620": "NGadsV620-series",
    "nv": "NV-series",
    "nvv5": "NVadsA10v5-series",
    "nvv3": "NVv3-series",
    "nvv4": "NVv4-series",
}