$Uri = 'https://azure.microsoft.com/api/v3/pricing/virtual-machines/calculator/?culture=en-us&currency=$currency'
$Response = Invoke-RestMethod -Uri  $Uri -Method Get

    # number of skus is around 25k - needs paralel processing here as well
    # pricingtypes are around 5-10
    # there are around 50 - 60 regions

$ParallelScript = {

    Foreach ($sku in (($using:Response.skus | Get-Member -MemberType NoteProperty).Name)) {
        $PricingTypes = (($using:Response).skus.$sku | get-member -MemberType NoteProperty).name
        # around 5 pricing types here. 
        Foreach ($PricingType in $PricingTypes) {
        $OfferInfo = ($using:Response).skus.$SKU.($PricingType) -split '--'
        $OfferSku = $OfferInfo[0]
        $OfferType= $OfferInfo[1]
        [PscustomOBject] @{
            Region = $_
            SKU = $SKU
            PricingType = $PricingType
            OfferSku = $OfferSku
            OfferType = $OfferType
            Price = ($using:Response).offers.$OfferSku.prices.$OfferType.($_).value 
        }       
    }
    }
}

<#
$Skus = ($Response.skus | Get-Member -MemberType NoteProperty).Name

$ParallelScript1 = {
    # number of skus is around 25k - needs paralel processing here as well
    Foreach ($Region in ($using:regions)) {
    
        $PricingTypes = (($using:Response).skus.$_ | get-member -MemberType NoteProperty).name
        # around 5 pricing types here. 
        Foreach ($PricingType in $PricingTypes) {
        $OfferInfo = ($using:Response).skus.$_.($PricingType) -split '--'
        $OfferSku = $OfferInfo[0]
        $OfferType= $OfferInfo[1]
        [PscustomOBject] @{
            Region = $region
            SKU = $_
            PricingType = $PricingType
            OfferSku = $OfferSku
            OfferType = $OfferType
            Price = ($using:Response).offers.$OfferSku.prices.$OfferType.$region.value 
        }       
    }
    
}
}
#>
#$Result = $skus | ForEach-Object -Parallel $ParallelScript1 -ThrottleLimit 30000
$regions = $response.regions.slug
$Result = $regions | ForEach-Object -Parallel $ParallelScript -ThrottleLimit 100

$result | ConvertTo-Json | Out-File -FilePath .\result.json


 