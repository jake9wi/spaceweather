param (
    [switch]$daily = $false,
    [switch]$fast = $false,
    [switch]$seven = $false,
    [switch]$three = $false
)

if (($sevem -eq $false) -and ($three -eq $false)) {
    throw 'Three or seven must be set'
} elseif (($sevem -eq $true) -and ($three -eq $true)) {
    throw 'Three or seven must be set'
}

if (($daily -eq $false) -and ($fast -eq $false)) {
    throw 'At least one of daily or fast must be set'
}

Push-Location -path $PSScriptRoot

$dirstruct = @(
    '..\spaceweather\web\html\',
    '..\spaceweather\web\img\',
    '..\spaceweather\src\'
)

if (($dirstruct | Test-Path) -contains $false) {
    throw 'Bad dir structure'
}

if (Get-Command -Name 'python.exe') {
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

$xray = '.\src\goesxray.py'
$swpcaaa = '.\src\swpcaaa.py'
$usgsmag = '.\src\usgsgeomag.py'
${flux107} = '.\src\flux107.py'
$planetk = '.\src\planetk.py'
$rtsw = '.\src\rtsw.py'

if ($daily -eq $true) {
    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList  @('-OO', ${flux107}) `
      -NoNewWindow `
      -Wait

    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList  @('-OO', $swpcaaa) `
      -NoNewWindow `
      -Wait
}

if ($fast -eq $true) {
    if ($three -eq $true) {
        Start-Process `
          -FilePath 'python.exe' `
          -ArgumentList  @('-OO', $xray, '--three')`
          -NoNewWindow `
          -Wait
    } else {
        Start-Process `
          -FilePath 'python.exe' `
          -ArgumentList  @('-OO', $xray, '--seven')`
          -NoNewWindow `
          -Wait
    }

    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList  @('-OO', $usgsmag) `
      -NoNewWindow `
      -Wait

    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList  @('-OO', $planetk) `
      -NoNewWindow `
      -Wait

    Start-Process `
      -FilePath 'python.exe' `
      -ArgumentList @('-OO', $rtsw) `
      -NoNewWindow  `
      -Wait
}

Pop-Location
