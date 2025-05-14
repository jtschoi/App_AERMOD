import rasterio
import subprocess
import os


def check_and_convert_nlcd_tif(tif_path, output_path=None):
    with rasterio.open(tif_path) as src:
        compression = src.profile.get("compress", "NONE")
        print(f"Compression type: {compression}")

        if compression != "NONE":
            if output_path is None:
                output_path = os.path.splitext(tif_path)[0] + "_uncompressed.tif"

            cmd = ["gdal_translate", "-co", "COMPRESS=NONE", tif_path, output_path]
            print("Running:", " ".join(cmd))
            subprocess.run(cmd, check=True)
            print(f"Uncompressed file saved to: {output_path}")
        else:
            print("The file is already uncompressed. No action needed.")
