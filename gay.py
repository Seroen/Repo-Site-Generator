import colorsys
import paths


init_file = open(paths.input_props_init)
init_lines = init_file.readlines()
init_file.close()

output_init = open(paths.input_tiles_init, "w")

categories = 0
for line in init_lines:
	if line[0] == "-":
		categories += 1

hue_dif = (1.0 / categories)

categories = 0
for line in init_lines:
	if line[0] == "-":
		categories += 1

		print(line[line.find(", ") + 2 : -2])
		print(colorsys.hsv_to_rgb(hue_dif * categories, 1.0, 1.0))
		print(hue_dif * categories)
		print(hue_dif)

		float_color = colorsys.hsv_to_rgb(hue_dif * categories, 1.0, 1.0)
		color = list(float_color)
		for i in range(3):
			color[i] = int(color[i] * 255)
		color = tuple(color)

		line = line.replace(line[line.find(", ") + 2 :], f"color{color}]\n")
		print(line)
	
	output_init.write(line)

output_init.close()