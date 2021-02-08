param (
    [switch]$daily = $false,
    [switch]$fast = $false
)

if (($daily -eq $false) -and ($fast -eq $false)) {
    throw 'at least one of daily or fast must be set'
}

Push-Location -path $PSScriptRoot

$dirstruct = @(
    '..\..\spaceweather\web\html\',
    '..\..\spaceweather\web\img\',
    '..\..\spaceweather\src\'
)

if (($dirstruct | Test-Path) -contains $false) {
    throw 'Bad dir structure'
}

if (Get-Command -Name 'python.exe' -ErrorAction SilentlyContinue) {
    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList '--version' `
      -NoNewWindow `
      -Wait `
      -RedirectStandardOutput 'vercheck'

    if (!(Select-String -path 'vercheck' -pattern '^Python 3.*')) {
	Remove-Item -Path 'vercheck'
	throw 'File python.exe exists but it emitted an unknown version string.'
    } else {
	Remove-Item -Path 'vercheck'
    }
    
} else {
    Remove-Item -Path 'vercheck'
    throw 'CAN NOT FIND "python.exe".'
}

$usgsmag = '.\usgsgeomag.py'
${flux107} = '.\flux107.py'
$planetk = '.\planetk.py'
$rtswmag = '.\rtswmag.py'
$rtswplasma = '.\rtswplasma.py'

if ($daily -eq $true) {
    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList  ${flux107} `
      -NoNewWindow `
      -Wait
}

if ($fast -eq $true) {
    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList  $usgsmag `
      -NoNewWindow `
      -Wait

    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList  $planetk `
      -NoNewWindow `
      -Wait

    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList $rtswmag `
      -NoNewWindow  `
      -Wait

    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList $rtswplasma `
      -NoNewWindow `
      -Wait
}

Pop-Location
