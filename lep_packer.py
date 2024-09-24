import os
import utils
import paths
import zipfile
from zipfile import ZipFile
from threading import Thread
import metadata


#folder_with_regions = [f"{paths.input_projects}/Vanilla Regions and Downpour Regions", f"{paths.input_projects}/Modded Regions", f"{paths.input_projects}/Sunlit Trail", f"{paths.input_projects}/Old New Horizons"]
folders_with_regions = [f"{paths.input_projects}/Regions", f"{paths.input_projects}/Region Expansions", f"{paths.input_projects}/Vanilla+MSC Regions"]
invalid_regions = ["Arenas", "Gates", "Tests"]
template_folders = [f"{paths.input_projects}/Templates/Size Templates", f"{paths.input_projects}/Templates/Gate Templates", f"{paths.input_projects}/Templates/Shelter Templates"]


# gate_files = []
# for file in os.listdir("input/Modded-Regions-Starter-Pack-main/LevelEditorProjects/Modded Gates"):
# 	if file == "Hollowed Grotto Gates":
# 		for grotto_file in os.listdir("input/Modded-Regions-Starter-Pack-main/LevelEditorProjects/Modded Gates/Hollowed Grotto Gates"):
# 			gate_files.append(grotto_file)
# 	else:
# 		gate_files.append(file)


def get_region_id(region, file):
	if region not in metadata.regions and ".png" in file:
		id = ""
		for char in file:
			if char == "_":
				break
			id += char
		
		if id != "GATE" and id != "G":
			metadata.regions[region] = {}
			metadata.regions[region]["id"] = id

	# for sub_path in os.listdir(path):
	# 	if os.path.isdir(f"{path}/{sub_path}"):
	# 		output_path += sub_path
	# 		recursive_zip(zip, f"{path}/{sub_path}", output_path)
	# 	else:
	# 		zip.write(f"{path}/{sub_path}", f"{output_path}/{os.path.split(sub_path)[1]}")


def pack_templates():
	for template_folder in template_folders:
		template_zip_path = f"{paths.dist_path}/Templates/{os.path.split(template_folder)[1]}.zip"

		utils.recursive_zip(template_zip_path, [f"{template_folder}"])

		print(f"[Template] {os.path.split(template_folder)[1]} complete")


pack_threads = []
def pack_pack(pack_folder, dummy):
	pack_zip_path = f"{paths.dist_path}/Region Packs/{os.path.split(pack_folder)[1]}.zip"

	utils.recursive_zip(pack_zip_path, [f"{pack_folder}"])

	print(f"[Region Pack] {os.path.split(pack_folder)[1]} complete")


def pack_packs():
	for pack_folder in os.listdir(paths.input_region_packs):
		pack_folder = f"{paths.input_region_packs}/{pack_folder}"

		pack_thread = Thread(target=pack_pack, args=(pack_folder, False))
		pack_thread.start()

		pack_threads.append(pack_thread)
	
	for thread in pack_threads:
		thread.join()
		


def pack_region(folder, region):
	if region not in invalid_regions:
		region_zip_path = f"{paths.dist_path}/{os.path.split(folder)[1]}/{region}.zip"
		region_zip = ZipFile(region_zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9)
		
		for file in os.listdir(f"{folder}/{region}"):
			if ".txt" not in file and ".png" not in file:
				for sub_file in os.listdir(f"{folder}/{region}/{file}"):
					region_zip.write(f"{folder}/{region}/{file}/{sub_file}", f"{file}/{sub_file}")

					if "Connection" not in folder:
						get_region_id(region, sub_file)
			else:
				region_zip.write(f"{folder}/{region}/{file}", f"{file}")
				get_region_id(region, file)
		
		region_zip.close()
		print(f"[Region] {region} complete")


region_threads = []
def pack_regions():
	for folder in folders_with_regions:
		for region in os.listdir(folder):
			region_thread = Thread(target=pack_region, args=(folder, region))
			region_thread.start()

			region_threads.append(region_thread)
	
	for thread in region_threads:
		thread.join()