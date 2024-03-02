import urllib.request as request
import json

def get_virtual_machine_sku_prices(region):
    skus = list(jsondata['skus'].keys())
    
    found_price_count=0
    for sku in skus:
        sku_info = sku.split('-')
            offer_info = jsondata['skus'][sku][pricing_type][0].split('--')
            offer_sku = offer_info[0]
            offer_type = offer_info[1]
            try :
                price = jsondata['offers'][offer_sku]['prices'][offer_type][region]['value']
                found_price_count += 1
                print(f"sku: {sku}, pricing_type: {pricing_type}, offer_type: {offer_sku}, offer_type: {offer_type}, price: {price}")
            except KeyError:
                print(f"Price information not available for sku: {sku}, pricing_type: {pricing_type}, in region: {region}")
    print(f"Number of skus: {len(skus)}")
    print(f"Number of prices found for region {region}: {found_price_count}")

virtual_machine_calculator_api = 'https://azure.microsoft.com/api/v3/pricing/virtual-machines/calculator/?culture=en-us&currency=$currency'
response=request.urlopen(virtual_machine_calculator_api)
data = response.read()
jsondata = json.loads(data)
regions  = jsondata['regions']


get_virtual_machine_sku_prices('us-east')
