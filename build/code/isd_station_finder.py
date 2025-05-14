import pandas as pd
from geopy.distance import great_circle
import tqdm
from pathlib import Path

EMBIT_LOC = Path(r"D:\Columbia\EmissionsBitcoin\build\data")
ISD_HISTORY = pd.read_csv(EMBIT_LOC / "aermet/isd/isd-history.csv")
IGRA_HISTORY = pd.read_fwf(
    EMBIT_LOC / "aermet/igra/igra2-station-list.txt",
    names=[
        "station_id",
        "lat",
        "lon",
        "elev_m",
        "station_name",
        "begin_year",
        "end_year",
        "num_obs",
    ],
    colspecs=[
        (0, 11),
        (12, 20),
        (21, 30),
        (31, 38),
        (39, 71),
        (72, 76),
        (77, 81),
        (82, 88),
    ],
)
NH_LAT = 40.691957
NH_LON = -75.479887


def int_to_timestamp(yyyymmdd):
    yyyymmdd = int(yyyymmdd)
    yyyy = str(yyyymmdd // 10000)
    mmdd = yyyymmdd % 10000
    mm = str(mmdd // 100).zfill(2)
    dd = str(mmdd % 100).zfill(2)
    tstamp = pd.Timestamp(f"{yyyy}-{mm}-{dd}")

    return tstamp


def closest_isd_station(
    source_lat,
    source_lon,
    start_date="2021-09-01",
    end_date="2024-06-30",
    country="US",
    top_n=10,
):

    if pd.Timestamp(end_date) >= pd.Timestamp("2025-03-01"):
        end_date = "2025-03-01"

    if country is not None:
        isd = ISD_HISTORY.loc[ISD_HISTORY["CTRY"] == country, :].reset_index(drop=True)
    else:
        isd = ISD_HISTORY.copy()

    so_latlon = (source_lat, source_lon)
    source_to_destin_km = []
    for lat, lon in tqdm.tqdm(isd[["LAT", "LON"]].values.tolist()):
        latlon = (lat, lon)
        try:
            so_to_destn = great_circle(latlon, so_latlon).km
        except:
            so_to_destn = 9999999
        source_to_destin_km.append(so_to_destn)
    isd["source_to_station_km"] = source_to_destin_km
    isd.sort_values(["source_to_station_km"], ascending=True, inplace=True)
    isd.reset_index(drop=True, inplace=True)

    # removing cases where it doesn't contain the start and end dates
    isd["start_date_station"] = isd["BEGIN"].apply(int_to_timestamp)
    isd["end_date_station"] = isd["END"].apply(int_to_timestamp)
    isd = isd.loc[
        (isd["start_date_station"] <= pd.Timestamp(start_date))
        & (isd["end_date_station"] >= pd.Timestamp(end_date)),
        :,
    ].reset_index(drop=True)
    isd = isd.iloc[0:top_n, :].copy()
    closest = isd.iloc[0, :]

    return closest, isd


def closest_igra_station(
    source_lat,
    source_lon,
    start_date="2021-09-01",
    end_date="2024-06-30",
    top_n=10,
):

    if pd.Timestamp(end_date) >= pd.Timestamp("2025-03-01"):
        end_date = "2025-03-01"
    igra = IGRA_HISTORY.copy()
    igra = igra.loc[igra["lon"] >= -900, :].reset_index(drop=True)

    so_latlon = (source_lat, source_lon)
    source_to_destin_km = []
    for lat, lon in tqdm.tqdm(igra[["lat", "lon"]].values.tolist()):
        latlon = (lat, lon)
        try:
            so_to_destn = great_circle(latlon, so_latlon).km
        except:
            so_to_destn = 9999999
        source_to_destin_km.append(so_to_destn)
    igra["source_to_station_km"] = source_to_destin_km
    igra.sort_values(["source_to_station_km"], ascending=True, inplace=True)
    igra.reset_index(drop=True, inplace=True)

    # removing cases where it doesn't contain the start and end dates
    igra["start_date_station"] = (igra["begin_year"] * 10000 + 101).apply(
        int_to_timestamp
    )
    igra["end_date_station"] = (igra["end_year"] * 10000 + 1231).apply(int_to_timestamp)
    igra = igra.loc[
        (igra["start_date_station"] <= pd.Timestamp(start_date))
        & (igra["end_date_station"] >= pd.Timestamp(end_date)),
        :,
    ].reset_index(drop=True)
    igra = igra.iloc[0:top_n, :].copy()
    closest = igra.iloc[0, :]

    return closest, igra


closest_NH, top10_NH = closest_isd_station(NH_LAT, NH_LON)
closigra_NH, top10igra_NH = closest_igra_station(NH_LAT, NH_LON)

file_path = r"D:\Columbia\EmissionsBitcoin\build\data\aermet\igra\closest_to_northampton\USM00072501-data.txt"

dates = []

with open(file_path, "r") as f:
    for line in f:
        if line.startswith("#"):
            parts = line.strip().split()
            try:
                year = int(parts[1])
                month = int(parts[2])
                day = int(parts[3])
                dates.append(f"{str(year)}-{str(month).zfill(2)}-{str(day).zfill(2)}")
            except (ValueError, IndexError):
                continue

print(dates[-1])
