$base = "http://localhost:8000"

Write-Host "`n--- POST /chat ---"
$body = @{ customer_id = "alice"; text = "track order 12345" } | ConvertTo-Json
Invoke-RestMethod -Uri "$base/chat" -Method Post -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 10

Write-Host "`n--- GET /health ---"
Invoke-RestMethod -Uri "$base/health" | ConvertTo-Json

Write-Host "`n--- GET /session/alice ---"
Invoke-RestMethod -Uri "$base/session/alice" | ConvertTo-Json
