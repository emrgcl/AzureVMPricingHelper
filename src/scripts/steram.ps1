Function say-sth {
    param(
        [string]$sth
    )
    write-verbose "said sth" -Verbose # verbose stream
    Write-output "saying $sth" # output stream

}
$result = say-sth -sth "hello world"
$result