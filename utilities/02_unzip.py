import tarfile
import os
import shutil


start_folder = "fire_data\\fire_data_total"

os.chdir(f"{start_folder}")

for i in range(2015, 2021):
    os.chdir('E:\\fire_data\\fire_data_total')
    working_folder = str(i)
    os.chdir(f"{working_folder}")

    with tarfile.open(f"{i}.tar.gz", 'r') as zip_ref:
        zip_ref.extractall()

    os.remove(f"{i}.tar.gz")

    list_of_files = os.listdir(os.getcwd())
    for current_file in list_of_files:
        if current_file.startswith("167") or current_file.startswith("166"):
            shutil.move(current_file, f"E:\\fire_data\\greek_fire_data\\{i}")

