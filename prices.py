import urllib.request as request
import json
import time
def get_virtual_machine_sku_prices(region):
    skus = list(json['skus'].keys())
    for sku in skus:
        pricing_types = json['skus'][sku].keys()
        for pricing_type in pricing_types:
            offer_info = json['skus'][sku][pricing_type][0].split('--')
            offer_sku = offer_info[0]
            offer_type = offer_info[1]
            price = json['offers'][offer_sku]['prices'][offer_type][region]['value']
            print(f"sku: {sku}, pricing_type: {pricing_type}, offer_type: {offer_sku}, offer_type: {offer_type}, price: {price}")

virtual_machine_calculator_api = 'https://azure.microsoft.com/api/v3/pricing/virtual-machines/calculator/?culture=en-us&currency=$currency'
response=request.urlopen(virtual_machine_calculator_api)
data = response.read()
json = json.loads(data)
regions  = json['regions']
for region in regions:
    print(region['slug'])

