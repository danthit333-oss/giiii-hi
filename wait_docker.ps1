$ready = $false
for ($i=0; $i -lt 30; $i++) {
    $v = docker info --format "{{.ServerVersion}}" 2>$null
    if ($LASTEXITCODE -eq 0 -and $v) {
        $ready = $true
        Write-Host "Docker ready version: $v"
        break
    }
    Start-Sleep -Seconds 2
}
if (-not $ready) {
    Write-Host "Docker not ready yet"
}
