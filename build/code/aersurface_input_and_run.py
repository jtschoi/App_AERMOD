import os
from pathlib import Path

os.makedirs("./aersurface_scripts", exist_ok=True)
os.makedirs("../data/aersurface_outputfiles", exist_ok=True)

def aersurface_input_generate(
    plant_name,
    latitude,
    longitude,
    year,
    path_to_land_cover_tif=(
        "../data/landcover_mrlc/Annual_NLCD_LndCov_2016_CU_C1V0.tif"
    ),
    output_name=None,
):
    
    YY = str(year)
    if output_name is None:
        output_name = "surface_charac_{}_{}.txt".format(plant_name, YY)
    
    output_name = f"../data/aersurface_outputfiles/{output_name}"
    output_name = os.path.abspath(output_name).replace("\\", "/")
    tifpath = os.path.abspath(path_to_land_cover_tif).replace("\\", "/")
    
    entire_txt = (
        f"AERSURFACE\n LOCATION LATITUDE {str(latitude)} "
        + f"LONGITUDE {str(longitude)}\n "
        + f"LANDUSEFILE {tifpath}\n "
    )
    
    entire_txt += (
        "REGION 1\n SEASONWINTER AVERAGE\n SEASONSPRING AVERAGE\n "
        "SEASONSUMMER AVERAGE\n SEASONFALL   AVERAGE\n "
        "MOISTUREWINTER AVERAGE\n MOISTURESPRING AVERAGE\n "
        "MOISTURESUMMER AVERAGE\n MOISTUREFALL   AVERAGE\n "
        + f"YEAR {YY}\n "
        + f"OUTPUTFILE {output_name}\nEND"
    )
    
    aersurface_input_code_name = f"./aersurface_scripts/{plant_name}_{YY}.inp"
    with open(aersurface_input_code_name, "w", encoding="utf-8") as fileinp:
        fileinp.write(entire_txt)
    
    return None

aersurface_input_generate("northampton", 40.691957, -75.479887, 2021)