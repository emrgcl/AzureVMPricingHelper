# Variables
$subscriptionId = "<subscription-id>" # Your Azure Subscription ID
$offerId = "MS-AZR-0003p" # Offer ID for Pay-As-You-Go subscriptions, change as needed
$currency = "USD" # Currency
$locale = "en-US" # Locale
$region = "east-us" # Azure Region
$vmSize = "Standard_D2s_v3" # VM Size

# Authenticate with Azure
Connect-AzAccount

# Fetch Azure VM Prices
$response = Invoke-RestMethod -Uri "https://prices.azure.com/api/retail/prices?`$filter=serviceName eq 'Virtual Machines' and armRegionName eq '$region' and skuName eq '$vmSize' and priceType eq 'Consumption' and currencyCode eq '$currency' and locale eq '$locale' and offerId eq '$offerId'" -Method Get -Headers @{Authorization = "Bearer $(Get-AzAccessToken -ResourceUrl https://management.azure.com).Token"}

# Output the prices
$response.Prices
