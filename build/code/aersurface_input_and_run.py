import os
from pathlib import Path

os.makedirs("./aersurface_scripts", exist_ok=True)
os.makedirs("../data/aersurface_outputfiles", exist_ok=True)


def aersurface_input_generate(
    plant_name,
    latitude,
    longitude,
    year,
    path_to_land_cover_tif="../data/landcover_mrlc/Annual_NLCD_LndCov_2016_CU_C1V0.tif",
    output_name=None,
):
    YY = str(year)
    if output_name is None:
        output_name = f"surface_charac_{plant_name}_{YY}.txt"

    output_path = os.path.abspath(
        f"../data/aersurface_outputfiles/{output_name}"
    ).replace("\\", "/")
    tif_path = os.path.abspath(path_to_land_cover_tif).replace("\\", "/")

    # Generate control file content
    control_text = f"""\
CO STARTING
TITLEONE AERSURFACE input for {plant_name} {YY}
OPTIONS PRIMARY ZORAD
DEBUGOPT GRID TIFF
CENTERLL {latitude} {longitude} NAD83
DATAFILE NLCD2016 "{tif_path}"
CLIMATE AVERAGE NOSNOW NONARID
FREQ_SECT SEASONAL 12 NONAP
RUNORNOT RUN
CO FINISHED

OU STARTING
SFCCHAR "{output_path}"
OU FINISHED
"""
    # Save control file
    input_filename = f"./aersurface_scripts/{plant_name}_{YY}.inp"
    os.makedirs(os.path.dirname(input_filename), exist_ok=True)

    with open(input_filename, "w", encoding="utf-8") as f:
        f.write(control_text)

    return input_filename


aersurface_input_generate("northampton", 40.691957, -75.479887, 2021)
