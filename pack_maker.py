import os
import shutil
import zipfile
from zipfile import ZipFile
import utils
import paths


packs_to_make = ["Tile Packs", "Prop Packs"]
output_folder = "processed repo"
forbidden_folders = ["Machinery", "Machinery2", "Metal", "MiscDonalds", "Stone"]


# Extracts name from init line
def extract_name(line):
	name = ""
	last_char = ""
	case_changed = False

	in_string = False
	for char in line:
		if char == '"':
			if not in_string:
				in_string = True
			else:
				in_string=False
				break
		else:
			if in_string:
				name += char
		
		last_char = char

	return name


# Locates png regardless of capitalization
def locate_case(input):
	for file in os.listdir(pack_source):
		file = os.path.splitext(file)[0]

		if file.lower() == input.lower():
			return file
	
	print(f"[{pack}] {input}.png missing!")
	return ""


def zip_pack():
	for folder in os.listdir(f"{output_folder}/{pack}"):
		if folder not in forbidden_folders:
			zip_path = f"{paths.dist_packs_path}/{pack}/{folder}.zip"
			zip = ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9)

			for file in os.listdir(f"{output_folder}/{pack}/{folder}"):
				zip.write(f"{output_folder}/{pack}/{folder}/{file}", f"{file}")
		
			zip.close()
			print(f"[{pack}] {folder} complete")


for pack in packs_to_make:
	# Remove old packs
	utils.reset_dir(f"{output_folder}/{pack}")
	
	# Get pack source folder
	match pack:
		case "Tile Packs":
			pack_source = f"{paths.input_repo}/Graphics"
		case "Prop Packs":
			pack_source = f"{paths.input_repo}/Props"
		
	# Load Init
	init = open(f"{pack_source}/Init.txt", "r")
	init_lines = init.readlines()
	init.close()

	# Process init
	for line in init_lines:
		if line != "\n":
			match line[0]:
				case "-":
					if "catagory_init" in vars():
						catagory_init.close()

					catagory = extract_name(line)

					os.makedirs(f"{output_folder}/{pack}/{catagory}")

					catagory_init = open(f"{output_folder}/{pack}/{catagory}/Copy_To_Init.txt", "w")
					catagory_init.write(line)
				
				case "[":
					item = extract_name(line)
					
					item_init_name = item
					item_png_name = item

					catagory_init.write(line)

					if not os.path.exists(f"{pack_source}/{item_png_name}.png"):
						item_png_name = locate_case(item_png_name)

					# Check if file found
					if item_png_name != "":
						shutil.copyfile(f"{pack_source}/{item_png_name}.png", f"{output_folder}/{pack}/{catagory}/{item_png_name}.png")
	
	zip_pack()
