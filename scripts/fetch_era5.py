#!/usr/bin/env python
"""Fetch ERA5 hourly temperature data for Austin, TX and save as Zarr."""

import os
from datetime import datetime, timedelta

import xarray as xr


def create_era5_zarr_austin():
    """Fetch ERA5 data from GCP and save as local Zarr store for demo."""
    try:
        # Open the ERA5 Zarr store on GCP (public bucket, anonymous access)
        ds = xr.open_zarr(
            "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3",
            chunks={"time": 24},
            consolidated=False,
            storage_options={"token": "anon"},
        )

        # Austin coordinates
        lat, lon = 30.27, -97.74

        # Use recent valid data (April 8, 2026 per dataset metadata)
        latest_dt = datetime(2026, 4, 8, 23, 0, 0, tzinfo=__import__("datetime").timezone.utc)
        start_time = latest_dt - timedelta(hours=23)

        # Extract 2m temperature for Austin with nearest neighbor
        t2m = ds["2m_temperature"].sel(latitude=lat, longitude=lon, method="nearest")

        # Slice to past 24 hours
        t2m_24h = t2m.sel(time=slice(str(start_time)[:19], str(latest_dt)[:19]))

        # Convert K to C
        t2m_24h_c = t2m_24h - 273.15

        # Create proper dataset
        ds_out = xr.Dataset(
            data_vars={"temperature": t2m_24h_c},
            coords={"time": t2m_24h_c.time},
            attrs={
                "latitude": float(lat),
                "longitude": float(lon),
                "variable": "2m Temperature (°C)",
                "source": "ERA5 - GCP Zarr (gs://gcp-public-data-arco-era5/)",
            },
        )

        # Create output directory
        output_path = "public/data/era5-austin.zarr"
        os.makedirs("public/data", exist_ok=True)

        # Save as Zarr (v2 format for compatibility)
        ds_out.to_zarr(output_path, mode="w", zarr_format=2)

        # Also save as JSON for browser consumption
        hours = [f"{i:02d}:00 UTC" for i in range(len(t2m_24h_c))]
        json_data = {
            "hours": hours,
            "temperatures": [float(v) for v in t2m_24h_c.values],
            "latitude": float(lat),
            "longitude": float(lon),
            "timestamp": "ERA5 - GCP Zarr (gs://gcp-public-data-arco-era5/)",
        }

        import json

        json_path = output_path.replace(".zarr", ".json")
        with open(json_path, "w") as f:
            json.dump(json_data, f, indent=2)

        print(f"✓ Saved ERA5 Zarr to {output_path}")
        print(f"✓ Saved ERA5 JSON to {json_path}")
        print(f"  Shape: {t2m_24h_c.shape}")
        print(f"  Time range: {str(start_time)[:19]} to {str(latest_dt)[:19]}")
        print(
            f"  Temperature range: {float(t2m_24h_c.min()):.1f}°C to {float(t2m_24h_c.max()):.1f}°C"
        )

    except Exception as e:
        raise RuntimeError(f"Failed to create ERA5 Zarr: {e}") from e


if __name__ == "__main__":
    try:
        create_era5_zarr_austin()
    except Exception as e:
        print(f"Error: {e}", file=__import__("sys").stderr)
        exit(1)
