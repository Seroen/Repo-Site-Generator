import os
import shutil
import metadata
import utils
from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000


def generate_download_links(path):
	links = ""

	for file in os.listdir(path):
		path = path.replace("Website/", "")
		links += f'<a href="{path}/{file}" download>{os.path.splitext(file)[0]}</a><br>\n'

	links = links[:-1]
	
	return links


def create_file_structure():
	# Reset folder
	utils.reset_dir("Website")

	shutil.copytree("input/Website/Fonts", "Website/Fonts")
	shutil.copytree("input/Website/Backgrounds", "Website/Backgrounds")

	os.makedirs("Website/Thumbnails/Regions")
	os.makedirs("Website/Thumbnails/Vanilla+MSC Regions")
	os.makedirs("Website/Thumbnails/Region Expansions")
	os.makedirs("Website/Thumbnails/Region Packs")
	os.makedirs("Website/Thumbnails/Templates")
	os.makedirs("Website/Thumbnails/Tile Packs")
	os.makedirs("Website/Thumbnails/Prop Packs")
	os.makedirs("Website/Thumbnails/Index")
	#os.makedirs("Website/Thumbnails/Leditors")

	shutil.copytree("input/Website/Dist/Tools", "Website/Dist/Tools")
	shutil.copytree("input/Website/Dist/Credits", "Website/Dist/Credits")
	shutil.copytree("input/Website/Dist/Drip Goku", "Website/Dist/Drip Goku")
	
	os.makedirs("Website/Dist/Packs/Tile Packs")
	os.makedirs("Website/Dist/Packs/Prop Packs")
	os.makedirs("Website/Dist/Regions")
	os.makedirs("Website/Dist/Region Packs")
	os.makedirs("Website/Dist/Region Expansions")
	os.makedirs("Website/Dist/Templates")
	os.makedirs("Website/Dist/Vanilla+MSC Regions")

	shutil.copyfile("input/Website/Thumbnails/Vanilla Pack.webp", "Website/Thumbnails/Vanilla Pack.webp")
	shutil.copyfile("input/Website/Thumbnails/crash.png", "Website/Thumbnails/crash.png")
	shutil.copyfile("input/Website/solar.png", "Website/solar.png")

	shutil.copytree("input/Website/Thumbnails/Leditors", "Website/Thumbnails/Leditors")
	shutil.copytree("input/Website/Thumbnails/Servers", "Website/Thumbnails/Servers")
	shutil.copytree("input/Website/Thumbnails/Wikis", "Website/Thumbnails/Wikis")
	shutil.copytree("input/Website/Thumbnails/Videos", "Website/Thumbnails/Videos")
	shutil.copytree("input/Website/Thumbnails/Tools", "Website/Thumbnails/Tools")

	shutil.copytree("input/Website/.git", "Website/.git")


def replace_html(input_html, text, file_path):
	html_file = open(file_path)
	html = html_file.read()
	html_file.close()

	return input_html.replace(text, html)


img_width = 180
img_height = 320
def process_thumbnail_folder(folder):
	for input_img in os.listdir(f"input/Website/Thumbnails/{folder}"):
		img = Image.open(f"input/Website/Thumbnails/{folder}/{input_img}")

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

		img_resize.save(f"Website/Thumbnails/{folder}/{output_img + '.webp'}")
		print(f"[{folder}] {output_img} converted")


def process_thumbnails():
	img = Image.open(f"input/Website/Thumbnails/All Regions.png")
	img_resize = img.resize((img_height, img_width))
	img_resize.save(f"Website/Thumbnails/Regions/All Regions Small.webp")
	img_resize = img.resize((img_height * 2, img_width * 2))
	img_resize.save(f"Website/Thumbnails/Regions/All Regions Medium.webp")
	img_resize = img.resize((img_height * 3, img_width * 3))
	img_resize.save(f"Website/Thumbnails/Regions/All Regions Large.webp")

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

	output_html = replace_html(output_html, "/* |navbar_css| */", "input/Website/navbar_css.html")
	output_html = replace_html(output_html, "|navbar|", "input/Website/navbar.html")
	output_html = replace_html(output_html, "// |navbar_script|", "input/Website/navbar_js.html")

	output_html = replace_html(output_html, "/* |basic_css| */", "input/Website/basic.css")

	output_html = replace_html(output_html, "/* |box_grid_css| */", "input/Website/box_grid.css")

	output_html = output_html.replace("|featured_boxes|", featured_boxes)

	return output_html


def create_info_html(input_html):
	output_html = input_html

	output_html = replace_html(output_html, "/* |navbar_css| */", "input/Website/navbar_css.html")
	output_html = replace_html(output_html, "|navbar|", "input/Website/navbar.html")
	output_html = replace_html(output_html, "// |navbar_script|", "input/Website/navbar_js.html")

	output_html = replace_html(output_html, "/* |basic_css| */", "input/Website/basic.css")

	output_html = replace_html(output_html, "/* |box_grid_css| */", "input/Website/box_grid.css")

	return output_html


def create_packs_html(input_html, pack_type):
	box_template_file = open("input/Website/pack_box_template.html")
	box_template = box_template_file.read()
	box_template_file.close()

	boxes = ""

	packs = os.listdir(f"Website/Dist/Packs/{pack_type}")
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
	
	output_html = replace_html(output_html, "/* |navbar_css| */", "input/Website/navbar_css.html")
	output_html = replace_html(output_html, "|navbar|", "input/Website/navbar.html")
	output_html = replace_html(output_html, "// |navbar_script|", "input/Website/navbar_js.html")

	output_html = replace_html(output_html, "/* |basic_css| */", "input/Website/basic.css")

	output_html = replace_html(output_html, "/* |box_grid_css| */", "input/Website/box_grid.css")

	return output_html


box_template_file = open("input/Website/box_template.html")
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

		if not os.path.exists(f"Website/Thumbnails/{zip_source}/{item}.webp"):
			item_box = item_box.replace(f"Thumbnails/{zip_source}/{item}.webp", "Thumbnails/crash.png")
			print(f"[{zip_source}] {item} is missing art!")

		boxes += item_box

		if item in metadata.featured_regions:
			featured_boxes += item_box
	
	return boxes


def create_region_html(input_html, type):
	output_html = input_html

	output_html = output_html.replace("|vanilla_boxes|", make_boxes(f"Website/Dist/Vanilla+MSC Regions", "Vanilla+MSC Regions"))
	output_html = output_html.replace("|template_boxes|", make_boxes(f"Website/Dist/Templates", "Templates"))
	output_html = output_html.replace("|pack_boxes|", make_boxes(f"Website/Dist/Region Packs", "Region Packs"))
	output_html = output_html.replace("|expansion_boxes|", make_boxes(f"Website/Dist/Region Expansions", "Region Expansions"))
	output_html = output_html.replace("|boxes|", make_boxes(f"Website/Dist/Regions", "Regions"))
	
	output_html = replace_html(output_html, "/* |navbar_css| */", "input/Website/navbar_css.html")
	output_html = replace_html(output_html, "|navbar|", "input/Website/navbar.html")
	output_html = replace_html(output_html, "// |navbar_script|", "input/Website/navbar_js.html")

	output_html = replace_html(output_html, "/* |basic_css| */", "input/Website/basic.css")

	output_html = replace_html(output_html, "/* |box_grid_css| */", "input/Website/box_grid.css")

	return output_html


def create_single_html(html, name):
	src_file = open(f"input/Website/{html}.html", "r")
	string = src_file.read()
	src_file.close()
	out_file = open(f"Website/{html}.html", "w")

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

