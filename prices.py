import urllib.request as request
import json

def save_to_file(itemlist,filename):
    with open(filename, 'w') as f:
        for item in itemlist:
            f.write("%s\n" % item)
        

def get_virtual_machine_sku_prices(region, jsondata):
    skus = list(jsondata['skus'].keys()) 
    found_price_count=0
    sku_os=[]
    for sku in skus:
        print(f"found windows sku: {sku}")
        pricing_types = jsondata['skus'][sku].keys()
        for pricing_type in pricing_types:
            for offer_info_data in jsondata['skus'][sku][pricing_type]:
                print(f"pricing_type: {pricing_type}")
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
                    return offer

                    print(f"sku: {sku}, pricing_type: {pricing_type}, offer_sku: {offer_sku}, offer_type: {offer_type}, price: {price}")
                except KeyError:
                    print(f"Price information not available for sku: {sku}, pricing_type: {pricing_type}, in region: {region}")
                except:
                    print(f"Error occurred while processing sku: {sku}, pricing_type: {pricing_type}, in region: {region}")

    print(f"Number of skus: {len(skus)}")
    print(f"Number of prices found for region {region}: {found_price_count}")
    print(f'List of OS: {", ".join(map(str, set(sku_os)))},')

def export_offers_to_json(offers, filename):
    with open(filename, 'w') as f:
        json.dump(offers, f, indent=4)

def main():
    virtual_machine_calculator_api = 'https://azure.microsoft.com/api/v3/pricing/virtual-machines/calculator/?culture=en-us&currency=$currency'
    response=request.urlopen(virtual_machine_calculator_api)
    data = response.read()
    jsondata = json.loads(data)
    regions  = jsondata['regions']

    offers= get_virtual_machine_sku_prices('us-east', jsondata)

    # Export the offers to a json file,
    export_offers_to_json(offers, 'offers.json')

if __name__ == '__main__':
    main()
