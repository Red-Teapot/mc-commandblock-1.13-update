import os

from process import process_region

world_folder = os.path.abspath('/home/redteapot/.local/share/multimc/instances/1.13/.minecraft/saves/World Update Test')
regions_folder = os.path.join(world_folder, 'region')

region_files = [f for f in os.listdir(regions_folder) if os.path.isfile(os.path.join(regions_folder, f))]

for file in region_files:
    file_abs = os.path.join(regions_folder, file)

    process_region(file_abs)