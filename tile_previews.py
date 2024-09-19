import os
import shutil
import utils
import paths


output_folder = paths.input_tiles_thumbnails


for pack_folder_name in os.listdir('processed repo/Tile Packs'):
	for file_name in os.listdir(f'processed repo/Tile Packs/{pack_folder_name}'):
		if ".txt" in file_name:
			pack_init_file = open(f'processed repo/Tile Packs/{pack_folder_name}/{file_name}')
			pack_init_lines = pack_init_file.readlines()
			pack_init_file.close()

			render_init_file = open("renderer/Data/Graphics/Init.txt", "w")
			render_init_file.write('-["Machinery", color(255, 160, 255)]\n')

			for line in pack_init_lines:
				if line[0] != "-":
					render_init_file.write(line)
			
			render_init_file.close()

			os.system(f'renderer/Drizzle.ConsoleApp render renderer/tile_previews.txt')

			utils.render_palette("renderer/Data/Levels/tile_previews_1.png")

			shutil.copyfile("renderer/Data/Levels/tile_previews_1.png", f"{output_folder}/{pack_folder_name}.png")
		