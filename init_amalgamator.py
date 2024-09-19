import os
import shutil
import paths
from PIL import Image


output_folder = paths.input_thumbnails
palette_img = Image.open("input/palette.png")


txt_file = open(paths.input_tiles_init)
txt_lines = txt_file.readlines()
txt_file.close()

render_init_file = open("renderer/Data/Graphics/Init.txt", "w")
render_init_file.write('-["Machinery", color(255, 160, 255)]\n')

for line in txt_lines:
	if line[0] != "-":
		render_init_file.write(line)

render_init_file.close()

os.system(f'renderer/Drizzle.ConsoleApp render renderer/tile_previews.txt')

img = Image.open("renderer/Data/Levels/tile_previews_1.png")

width, height = img.size
for x in range(width):
	for y in range(height):
		r,g,b,a = img.getpixel((x,y))
		
		match r:
			case red if 1 <= red <= 30:
				img.putpixel((x, y), palette_img.getpixel((red - 1, 5)))
			
			case red if 31 <= red <= 60:
				img.putpixel((x, y), palette_img.getpixel((red - 31, 6)))
			
			case red if 61 <= red <= 90:
				img.putpixel((x, y), palette_img.getpixel((red - 61, 7)))
			
			case red if 91 <= red <= 120:
				img.putpixel((x, y), palette_img.getpixel((red - 91, 2)))
			
			case red if 121 <= red <= 150:
				img.putpixel((x, y), palette_img.getpixel((red - 121, 3)))
			
			case red if 151 <= red <= 180:
				img.putpixel((x, y), palette_img.getpixel((red - 151, 4)))
			
			case _:
				img.putpixel((x, y), palette_img.getpixel((0, 0)))

img.save("renderer/Data/Levels/tile_previews_1.png")

shutil.copyfile("renderer/Data/Levels/tile_previews_1.png", f"{output_folder}/Index/Resources.png")