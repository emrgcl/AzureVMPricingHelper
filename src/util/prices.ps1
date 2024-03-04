$ResversationCsvPath = 'C:\temp\reservations\reservations.csv'
$ConsumptionCsvPath = 'C:\temp\reservations\consumption.csv'
$Region= 'westeurope'
$service = 'Virtual Machines'
$ScriptStart = Get-date
$Uri = "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview"
$Items = @()
do {

$Response= Invoke-RestMethod -Uri  $Uri -Method Get
$Items += $Response.Items
$Uri = $Response.NextPageLink

} 
until ([string]::IsNullOrEmpty($Uri))

$VMItems = $Items | Where-Object {$_.serviceName -eq 'Virtual Machines'}

$Reservations = $Items | Where-Object {$_.type -eq 'Reservation' -and $_.'ArmregionName' -eq $Region -and $_.serviceName -eq $SErvice}
$Reservations | export-csv -Path $ResversationCsvPath

$Consumptions = $Items | Where-Object {$_.type -eq 'Consumption' -and $_.'ArmregionName' -eq $Region -and $_.serviceName -eq $SErvice}
$Consumptions | Export-Csv -Path $ConsumptionCsvPath
$DurationSeconds = [Math]::Round(((Get-Date) - $ScriptStart).TotalSeconds)
Write-verbose "Script ended in $DurationSeconds seconds. Number of items $($Items.Count)" -Verbose