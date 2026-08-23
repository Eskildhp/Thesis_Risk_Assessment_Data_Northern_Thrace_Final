# Copernicus DEM Download Script

This folder contains the PowerShell script used to query and download Copernicus DEM tiles from the Copernicus Data Space Ecosystem (CDSE).

The script is configured for the DEM dataset used in the workflow:

`COP-DEM\_EEA-10-DGED/2024\_1`

Before running the script, the user must provide their own CDSE account credentials, choose a local output directory and insert the area of interest (AOI) as a WKT polygon.

### File

`Copernicus\_DEM\_download.ps1`

### Requirements

The script requires:

* Windows PowerShell or PowerShell
* Copernicus Data Space Ecosystem account
* Online connected to the Internet
* Study-area polygon in WKT format using EPSG:4326 coordinates

### 1\. Add CDSE account credentials

The script does not contain a username or password.

It reads the following environment variables:

`CDSE\_USER`

`CDSE\_PASSWORD`

Set these variables locally before running the script.

For the current PowerShell session:

```powershell
$env:CDSE\_USER = "your-email@example.com"
$env:CDSE\_PASSWORD = "your-password"
```

These values are only available during the PowerShell session.

To store them as Windows user environment variables:

```powershell
\[Environment]::SetEnvironmentVariable("CDSE\_USER", "your-email@example.com", "User")
\[Environment]::SetEnvironmentVariable("CDSE\_PASSWORD", "your-password", "User")
```

After setting environment variables, open a new PowerShell window before running the script.

Do not add personal credentials to the script before saving it in a public repository.

### 2\. Set the download directory

The script contains the placeholder:

```powershell
$OutDir = "C:\\path\\to\\Copernicus\_DEM"
```

Replace this with the local folder where the downloaded DEM ZIP files should be saved.

For example:

```powershell
$OutDir = "D:\\GIS\_Data\\Copernicus\_DEM"
```

The downloaded DEM files should be stored outside the GitHub repository because of their size.

### 3\. Add the study-area polygon

The script contains the placeholder:

```powershell
$WKT = "PASTE\_STUDY\_AREA\_WKT\_HERE"
```

Replace this with the AOI polygon used for the download.

The polygon must:

* Be written in WKT format
* Use EPSG:4326 coordinates
* Form a closed polygon, where the first and last coordinate pair are identical

Example structure:

```text
POLYGON((
longitude latitude,
longitude latitude,
longitude latitude,
longitude latitude,
longitude latitude
))
```

The example shows the required format, it is not the Northern Thrace area polygon.

To reproduce the thesis workflow, the Northern Thrace area polygon should be inserted here before running the script.

### 4\. Check the dataset

The script is currently configured with:

```powershell
$Dataset = "COP-DEM\_EEA-10-DGED/2024\_1"
```

This is the dataset identifier used for the thesis DEM download.

Only change this value if a different Copernicus DEM product is being downloaded.

### 5\. Run the script

Open PowerShell and go to the folder containing the script.

For example:

```powershell
cd "C:\\path\\to\\data\_acquisition\\scripts"
```

Run:

```powershell
.\\Copernicus\_DEM\_download.ps1
```

The script will:

1. Check that the CDSE credentials and AOI have been provided
2. Request an access token
3. Query the CDSE catalogue for DEM products intersecting the AOI
4. List the matching DEM tiles
5. Download the tiles to the selected output directory
6. Skip files that already exist
7. Refresh the access token and retry when required

### Repository structure

A suggested repository structure is:

```text
data\_acquisition/
├── README.md
└── scripts/
    └── Copernicus\_DEM\_download.ps1
```

The downloaded DEM tiles are not included in the repository.

