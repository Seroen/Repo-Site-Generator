import os
import shutil
import zipfile
from zipfile import ZipFile
from PIL import Image


def reset_dir(path):
	if os.path.exists(path):
			shutil.rmtree(path)


def fast_zip(zip_path, path):
	for root, dirs, files in os.walk(path):
		for file in files:
			os.system(f'zip -u {zip_path} "{os.path.join(root, file)}"')

def recursive_zip(zip_path, paths):
	zip = ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, strict_timestamps=False)

	for path in paths:
		for root, dirs, files in os.walk(path):
			for file in files:
				zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
	
	zip.close()


def lerp_color(source_color, dest_color, ammount):
	ammount = ammount / 255

	output_color = []

	for c in range(3):
		output_color.append(int(source_color[c] + ((dest_color[c] - source_color[c]) * ammount)))

	return tuple(output_color)
	#return a + ((b - a) * t)


palette_img = Image.open("palette.png")
def render_palette(path):
	img = Image.open(path)

	width, height = img.size
	for x in range(width):
		for y in range(height):
			r,g,b,a = img.getpixel((x,y))
			
			match r:
				case red if 1 <= red <= 30:
					img.putpixel((x, y), palette_img.getpixel((red - 1, 7)))
				
				case red if 31 <= red <= 60:
					img.putpixel((x, y), palette_img.getpixel((red - 31, 6)))
				
				case red if 61 <= red <= 90:
					img.putpixel((x, y), palette_img.getpixel((red - 61, 5)))
				
				case red if 91 <= red <= 120:
					img.putpixel((x, y), palette_img.getpixel((red - 91, 4)))
				
				case red if 121 <= red <= 150:
					img.putpixel((x, y), palette_img.getpixel((red - 121, 3)))
				
				case red if 151 <= red <= 180:
					img.putpixel((x, y), palette_img.getpixel((red - 151, 2)))
				
				case _:
					img.putpixel((x, y), palette_img.getpixel((0, 0)))

			match g:
				case 1:
					img.putpixel((x, y), lerp_color(img.getpixel((x,y)), (0, 255, 0), b))
				
				case 2:
					img.putpixel((x, y), lerp_color(img.getpixel((x,y)), (0, 0, 255), b))

				case 3:
					img.putpixel((x, y), lerp_color(img.getpixel((x,y)), (255, 255, 255), b))

				case _:
					pass
					
	
	img.save(path)

# render_palette("Website Source/Thumbnails/Tile Packs/Water Trains.png")


def tile_palettes():
	shutil.rmtree("Website Source/Thumbnails/Tile Packs")
	shutil.copytree("Website Source/Thumbnails/Tile Packs Source", "Website Source/Thumbnails/Tile Packs")

	for file in os.listdir("Website Source/Thumbnails/Tile Packs"):
		render_palette(f"Website Source/Thumbnails/Tile Packs/{file}")

def prop_palettes():
	shutil.rmtree("Website Source/Thumbnails/Prop Packs")
	shutil.copytree("Website Source/Thumbnails/Prop Packs Source", "Website Source/Thumbnails/Prop Packs")

	for file in os.listdir("Website Source/Thumbnails/Prop Packs"):
		render_palette(f"Website Source/Thumbnails/Prop Packs/{file}")
