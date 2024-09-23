import os
import shutil
import paths
import metadata
import utils
from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000


def generate_download_links(path):
	links = ""

	for file in os.listdir(path):
		path = path.replace(f"{paths.output}/", "")
		links += f'<a href="{path}/{file}" download>{os.path.splitext(file)[0]}</a><br>\n'

	links = links[:-1]
	
	return links


def create_file_structure():
	# Reset folder
	#utils.reset_dir("Website")

	for folder in os.listdir(paths.output):
		if folder != ".git":
			if os.path.isdir(f"{paths.output}/{folder}"):
				shutil.rmtree(f"{paths.output}/{folder}")
			else:
				os.remove(f"../Warehouse/{folder}")

	shutil.copytree(f"{paths.website_source}/Fonts", f"{paths.output}/Fonts")
	shutil.copytree(f"{paths.website_source}/Backgrounds", f"{paths.output}/Backgrounds")

	os.makedirs(f"{paths.output}/Thumbnails/Regions")
	os.makedirs(f"{paths.output}/Thumbnails/Vanilla+MSC Regions")
	os.makedirs(f"{paths.output}/Thumbnails/Region Expansions")
	os.makedirs(f"{paths.output}/Thumbnails/Region Packs")
	os.makedirs(f"{paths.output}/Thumbnails/Templates")
	os.makedirs(f"{paths.output}/Thumbnails/Tile Packs")
	os.makedirs(f"{paths.output}/Thumbnails/Prop Packs")
	os.makedirs(f"{paths.output}/Thumbnails/Index")
	#os.makedirs("Website/Thumbnails/Leditors")

	shutil.copytree(f"{paths.website_source}/Dist/Tools", f"{paths.output}/Dist/Tools")
	shutil.copytree(f"{paths.website_source}/Dist/Credits", f"{paths.output}/Dist/Credits")
	shutil.copytree(f"{paths.website_source}/Dist/Drip Goku", f"{paths.output}/Dist/Drip Goku")
	
	os.makedirs(f"{paths.output}/Dist/Packs/Tile Packs")
	os.makedirs(f"{paths.output}/Dist/Packs/Prop Packs")
	os.makedirs(f"{paths.output}/Dist/Regions")
	os.makedirs(f"{paths.output}/Dist/Region Packs")
	os.makedirs(f"{paths.output}/Dist/Region Expansions")
	os.makedirs(f"{paths.output}/Dist/Templates")
	os.makedirs(f"{paths.output}/Dist/Vanilla+MSC Regions")

	shutil.copyfile(f"{paths.website_source}/Thumbnails/Vanilla Pack.webp", f"{paths.output}/Thumbnails/Vanilla Pack.webp")
	shutil.copyfile(f"{paths.website_source}/Thumbnails/crash.png", f"{paths.output}/Thumbnails/crash.png")
	shutil.copyfile(f"{paths.website_source}/solar.png", f"{paths.output}/solar.png")

	shutil.copytree(f"{paths.website_source}/Thumbnails/Leditors", f"{paths.output}/Thumbnails/Leditors")
	shutil.copytree(f"{paths.website_source}/Thumbnails/Servers", f"{paths.output}/Thumbnails/Servers")
	shutil.copytree(f"{paths.website_source}/Thumbnails/Wikis", f"{paths.output}/Thumbnails/Wikis")
	shutil.copytree(f"{paths.website_source}/Thumbnails/Videos", f"{paths.output}/Thumbnails/Videos")
	shutil.copytree(f"{paths.website_source}/Thumbnails/Tools", f"{paths.output}/Thumbnails/Tools")

	#shutil.copytree(f"{paths.website_source}/.git", "Website/.git")


def replace_html(input_html, text, file_path):
	html_file = open(file_path)
	html = html_file.read()
	html_file.close()

	return input_html.replace(text, html)


img_width = 180
img_height = 320
def process_thumbnail_folder(folder):
	for input_img in os.listdir(f"{paths.website_source}/Thumbnails/{folder}"):
		img = Image.open(f"{paths.website_source}/Thumbnails/{folder}/{input_img}")

		# if folder == "Tile Packs":
		# 	palette_img = Image.open("input/palette.png")

		# 	width, height = img.size
		# 	for x in range(width):
		# 		for y in range(height):
		# 			r,g,b,a = img.getpixel((x,y))
					
		# 			match r:
		# 				case red if 91 <= red <= 120:
		# 					img.putpixel((x, y), palette_img.getpixel((red - 91, 2)))
						
		# 				case red if 121 <= red <= 150:
		# 					img.putpixel((x, y), palette_img.getpixel((red - 121, 3)))
						
		# 				case red if 151 <= red <= 180:
		# 					img.putpixel((x, y), palette_img.getpixel((red - 151, 4)))


		img_resize = img.resize((img_height, img_width))

		output_img = os.path.splitext(input_img)[0]

		img_resize.save(f"{paths.output}/Thumbnails/{folder}/{output_img + '.webp'}")
		print(f"[{folder}] {output_img} converted")


def process_thumbnails():
	img = Image.open(f"{paths.website_source}/Thumbnails/All Regions.png")
	img_resize = img.resize((img_height, img_width))
	img_resize.save(f"{paths.output}/Thumbnails/Regions/All Regions Small.webp")
	img_resize = img.resize((img_height * 2, img_width * 2))
	img_resize.save(f"{paths.output}/Thumbnails/Regions/All Regions Medium.webp")
	img_resize = img.resize((img_height * 3, img_width * 3))
	img_resize.save(f"{paths.output}/Thumbnails/Regions/All Regions Large.webp")

	process_thumbnail_folder("Regions")
	process_thumbnail_folder("Vanilla+MSC Regions")
	process_thumbnail_folder("Region Expansions")
	process_thumbnail_folder("Region Packs")
	process_thumbnail_folder("Templates")
	process_thumbnail_folder("Tile Packs")
	process_thumbnail_folder("Prop Packs")
	process_thumbnail_folder("Index")


featured_boxes = ""
def create_index_html(input_html):
	global featured_boxes

	output_html = input_html

	output_html = replace_html(output_html, "/* |navbar_css| */", f"{paths.website_source}/navbar_css.html")
	output_html = replace_html(output_html, "|navbar|", f"{paths.website_source}/navbar.html")
	output_html = replace_html(output_html, "// |navbar_script|", f"{paths.website_source}/navbar_js.html")

	output_html = replace_html(output_html, "/* |basic_css| */", f"{paths.website_source}/basic.css")

	output_html = replace_html(output_html, "/* |box_grid_css| */", f"{paths.website_source}/box_grid.css")

	output_html = output_html.replace("|featured_boxes|", featured_boxes)

	return output_html


def create_info_html(input_html):
	output_html = input_html

	output_html = replace_html(output_html, "/* |navbar_css| */", f"{paths.website_source}/navbar_css.html")
	output_html = replace_html(output_html, "|navbar|", f"{paths.website_source}/navbar.html")
	output_html = replace_html(output_html, "// |navbar_script|", f"{paths.website_source}/navbar_js.html")

	output_html = replace_html(output_html, "/* |basic_css| */", f"{paths.website_source}/basic.css")

	output_html = replace_html(output_html, "/* |box_grid_css| */", f"{paths.website_source}/box_grid.css")

	return output_html


def create_packs_html(input_html, pack_type):
	box_template_file = open(f"{paths.website_source}/pack_box_template.html")
	box_template = box_template_file.read()
	box_template_file.close()

	boxes = ""

	packs = os.listdir(f"{paths.output}/Dist/Packs/{pack_type}")
	packs.sort()

	for file in packs:
		pack = os.path.splitext(file)[0]

		box = box_template

		box = box.replace("|pack|", pack)
		box = box.replace("|pack_type|", pack_type)
		box = box.replace("|pack_link|", f"Dist/Packs/{pack_type}/{file}")

		# if not os.path.exists(f"Website/Thumbnails/{pack_type}/{pack}.webp"):
		# 	box = box.replace(f"Thumbnails/{pack_type}/{pack}.webp", "Thumbnails/crash.png")
		# 	print(f"[Tiles] {pack} is missing art!")
		
		boxes += box + "\n"

	output_html = input_html.replace("|boxes|", boxes)
	
	output_html = replace_html(output_html, "/* |navbar_css| */", f"{paths.website_source}/navbar_css.html")
	output_html = replace_html(output_html, "|navbar|", f"{paths.website_source}/navbar.html")
	output_html = replace_html(output_html, "// |navbar_script|", f"{paths.website_source}/navbar_js.html")

	output_html = replace_html(output_html, "/* |basic_css| */", f"{paths.website_source}/basic.css")

	output_html = replace_html(output_html, "/* |box_grid_css| */", f"{paths.website_source}/box_grid.css")

	return output_html


box_template_file = open(f"{paths.website_source}/box_template.html")
box_template = box_template_file.read()
box_template_file.close()
def make_boxes(path, zip_source):
	global featured_boxes
	
	boxes = ""
	items = os.listdir(path)
	items.sort()

	for item_zip in items:
		item = os.path.splitext(item_zip)[0]

		item_box = box_template

		if zip_source == "Regions" or zip_source == "Vanilla+MSC Regions":
			item_box = item_box.replace("|id|", f" [{metadata.regions[item]["id"]}]")
		else:
			item_box = item_box.replace("|id|", "")
		
		item_box = item_box.replace("|item|", item)
		item_box = item_box.replace("|type|", zip_source)
		item_box = item_box.replace("|link|", f"Dist/{zip_source}/{item_zip}")

		if not os.path.exists(f"{paths.output}/Thumbnails/{zip_source}/{item}.webp"):
			item_box = item_box.replace(f"Thumbnails/{zip_source}/{item}.webp", "Thumbnails/crash.png")
			print(f"[{zip_source}] {item} is missing art!")

		boxes += item_box

		if item in metadata.featured_regions:
			featured_boxes += item_box
	
	return boxes


def create_region_html(input_html, type):
	output_html = input_html

	output_html = output_html.replace("|vanilla_boxes|", make_boxes(f"{paths.output}/Dist/Vanilla+MSC Regions", "Vanilla+MSC Regions"))
	output_html = output_html.replace("|template_boxes|", make_boxes(f"{paths.output}/Dist/Templates", "Templates"))
	output_html = output_html.replace("|pack_boxes|", make_boxes(f"{paths.output}/Dist/Region Packs", "Region Packs"))
	output_html = output_html.replace("|expansion_boxes|", make_boxes(f"{paths.output}/Dist/Region Expansions", "Region Expansions"))
	output_html = output_html.replace("|boxes|", make_boxes(f"{paths.output}/Dist/Regions", "Regions"))
	
	output_html = replace_html(output_html, "/* |navbar_css| */", f"{paths.website_source}/navbar_css.html")
	output_html = replace_html(output_html, "|navbar|", f"{paths.website_source}/navbar.html")
	output_html = replace_html(output_html, "// |navbar_script|", f"{paths.website_source}/navbar_js.html")

	output_html = replace_html(output_html, "/* |basic_css| */", f"{paths.website_source}/basic.css")

	output_html = replace_html(output_html, "/* |box_grid_css| */", f"{paths.website_source}/box_grid.css")

	return output_html


def create_single_html(html, name):
	src_file = open(f"{paths.website_source}/{html}.html", "r")
	string = src_file.read()
	src_file.close()
	out_file = open(f"{paths.output}/{html}.html", "w")

	if name == "Main Page":
		out_file.write(create_index_html(string))
	if name == "Tile Packs" or name == "Prop Packs":
		out_file.write(create_packs_html(string, name))
	if name == "Regions" or name == "Region Expansions":
		out_file.write(create_region_html(string, name))
	if name == "Info":
		out_file.write(create_info_html(string))
	
	out_file.close()


def create_html():
	create_single_html("tiles", "Tile Packs")
	create_single_html("props", "Prop Packs")
	create_single_html("regions", "Regions")
	create_single_html("info", "Info")
	create_single_html("index", "Main Page")

