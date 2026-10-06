param(
    [ValidateSet('26.2', '26.3', 'all')]
    [string]$Minecraft = 'all',
    [string]$JavaHome = $env:JAVA_HOME
)
$ErrorActionPreference = 'Stop'
if (-not $JavaHome) {
    $portable = Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot '.tools') -Directory -Filter 'jdk-*' -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($portable) { $JavaHome = $portable.FullName }
}
if (-not $JavaHome -or -not (Test-Path -LiteralPath (Join-Path $JavaHome 'bin/java.exe'))) {
    throw 'Specify a JDK 25 directory with -JavaHome or JAVA_HOME.'
}
$env:JAVA_HOME = $JavaHome
$env:GRADLE_USER_HOME = Join-Path $PSScriptRoot '.tools/gradle-user-home'
$targets = if ($Minecraft -eq 'all') { @('26.2', '26.3') } else { @($Minecraft) }
foreach ($game in $targets) {
    $project = Join-Path $PSScriptRoot "fabric-$game"
    & (Join-Path $project 'gradlew.bat') -p $project build --no-daemon --console=plain
    if ($LASTEXITCODE -ne 0) { throw "Build failed for Minecraft $game (exit $LASTEXITCODE)." }
    $output = Join-Path $PSScriptRoot "dist/$game/local-build"
    New-Item -ItemType Directory -Path $output -Force | Out-Null
    Get-ChildItem -LiteralPath (Join-Path $project 'build/libs') -Filter '*.jar' | Copy-Item -Destination $output
    Write-Output "Built Minecraft ${game}: $output"
}
