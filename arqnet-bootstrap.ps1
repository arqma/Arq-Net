[CmdletBinding()]
param ()
$web = New-Object System.Net.WebClient
if( -not ( Test-Path $env:APPDATA\.arqnet -PathType Container ) )
{
  arqnet.exe -g
}


$web.DownloadFile("https://seed.arqma.com/arqnet.signed", "$env:APPDATA\.arqnet\bootstrap.signed")
