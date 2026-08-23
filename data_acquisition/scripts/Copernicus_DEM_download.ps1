# ================== CDSE DEM bulk downloader (AOI + token auto-refresh) ==================

# --- 0) CONFIG ---

# Copernicus Data Space credentials are read from local environment variables.
$CdseUser = $env:CDSE_USER
$CdsePassword = $env:CDSE_PASSWORD

# Local folder where downloaded DEM ZIP files will be saved.
$OutDir = "C:\path\to\Copernicus_DEM"

# Northern Thrace study-area polygon in WKT, EPSG:4326.
# Replace the placeholder below with the exact study-area WKT exported from ArcGIS Pro.
$WKT = "PASTE_STUDY_AREA_WKT_HERE"

# Copernicus DEM dataset used in the thesis.
$Dataset = "COP-DEM_EEA-10-DGED/2024_1"

$Top = 200
$MaxRedir = 8
$MaxRetriesPerFile = 3


# --- 1) CHECK SETTINGS ---

if (-not $CdseUser -or -not $CdsePassword) {
    throw "Set the CDSE_USER and CDSE_PASSWORD environment variables before running the script."
}

if ($WKT -eq "PASTE_STUDY_AREA_WKT_HERE") {
    throw "Replace the WKT placeholder with the Northern Thrace study-area polygon before running the script."
}


# --- 2) FUNCTIONS ---

function New-CDSEToken {
    param(
        [string]$User,
        [string]$Pass
    )

    $TokenUrl = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    $Body = @{
        client_id  = "cdse-public"
        grant_type = "password"
        username   = $User
        password   = $Pass
    }

    $Response = Invoke-RestMethod -Method Post -Uri $TokenUrl -Body $Body
    return "Bearer " + $Response.access_token
}


function Get-CDSEProducts {
    param(
        [string]$Bearer,
        [string]$Dataset,
        [string]$WKT,
        [int]$Top
    )

    $Filter = @"
Attributes/OData.CSC.StringAttribute/any(att: att/Name eq 'dataset' and att/OData.CSC.StringAttribute/Value eq '$Dataset')
and OData.CSC.Intersects(area=geography'SRID=4326;$WKT')
"@

    $EncodedFilter = [uri]::EscapeDataString($Filter)
    $Url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?`$filter=$EncodedFilter&`$top=$Top&`$expand=Attributes&`$orderby=ContentLength asc"

    Invoke-RestMethod -Headers @{ Authorization = $Bearer } -Uri $Url -Method Get
}


function Download-CDSEProduct {
    param(
        [ref]$Bearer,
        [pscustomobject]$Product,
        [string]$OutPath,
        [int]$MaxRetries = 3
    )

    $Attempt = 0

    while ($Attempt -lt $MaxRetries) {
        $Attempt++

        try {
            $DownloadUrl = "https://download.dataspace.copernicus.eu/odata/v1/Products($($Product.Id))/`$value"

            Invoke-WebRequest `
                -Headers @{ Authorization = $Bearer.Value } `
                -Uri $DownloadUrl `
                -OutFile $OutPath `
                -MaximumRedirection $MaxRedir `
                -TimeoutSec 0

            return $true
        }
        catch {
            $Message = $_.Exception.Message

            if (
                $Message -match "Token is expired" -or
                $Message -match "\b401\b" -or
                $Message -match "\b403\b"
            ) {
                Write-Host "Token expired or unauthorized. Refreshing and retrying ($Attempt/$MaxRetries)..."
                $Bearer.Value = New-CDSEToken -User $CdseUser -Pass $CdsePassword
                Start-Sleep -Seconds 2
            }
            else {
                Write-Host "Download error (attempt $Attempt/$MaxRetries): $Message"
                Start-Sleep -Seconds 2
            }
        }
    }

    return $false
}


# --- 3) RUN ---

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$Bearer = New-CDSEToken -User $CdseUser -Pass $CdsePassword
Write-Host "Token obtained."

$Catalogue = Get-CDSEProducts `
    -Bearer $Bearer `
    -Dataset $Dataset `
    -WKT $WKT `
    -Top $Top

if (-not $Catalogue.value) {
    throw "No products were returned for the selected AOI and dataset."
}

$Catalogue.value |
    Select-Object Id, Name, @{n = "MB"; e = {[math]::Round($_.ContentLength / 1MB, 1)}} |
    Format-Table -AutoSize

Write-Host "`nFound $($Catalogue.value.Count) tiles. Starting downloads to: $OutDir`n"

foreach ($Product in $Catalogue.value) {
    $Destination = Join-Path $OutDir ($Product.Name + ".zip")

    if (Test-Path $Destination) {
        Write-Host "Already exists, skipping: $($Product.Name)"
        continue
    }

    $SizeMb = [math]::Round($Product.ContentLength / 1MB, 1)
    Write-Host "Downloading $($Product.Name) ($SizeMb MB)"

    $Success = Download-CDSEProduct `
        -Bearer ([ref]$Bearer) `
        -Product $Product `
        -OutPath $Destination `
        -MaxRetries $MaxRetriesPerFile

    if ($Success) {
        Write-Host "Saved: $Destination"
    }
    else {
        Write-Host "Failed after retries: $($Product.Name)"
    }
}

Write-Host "`nDone."
