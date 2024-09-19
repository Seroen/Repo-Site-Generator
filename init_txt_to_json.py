import json
import pprint
import paths


init_dict = {
	"Tile Categories": {"-root" : []},
	"Tiles": {},
	"Prop Categories" : {"-root" : []},
	"Props": {},
}


tiles_file = open(paths.input_tiles_init)
tiles_lines = tiles_file.readlines()
tiles_file.close()

current_category = ""
for line in tiles_lines:
	current_tile = ""
	current_key = "None"

	in_string = False
	string = ""

	char_i = 0
	while char_i < len(line):
		char = line[char_i]

		if line[0] != "-":
			match current_key:
				case "None":
					if char == "#":
						if line[char_i : char_i + 4] == "#nm:":
							current_key = "#nm:"
							char_i += 3

							in_string = False
							string = ""
						
						if line[char_i : char_i + 9] == '#sz:point':
							current_key = '#sz:point'
							char_i += 8

							in_point = False
							point = [-1, -1]
							point_index = 0
							num_string = ""
						
						if line[char_i : char_i + 8] == '#specs:[':
							current_key = '#specs:'
							char_i += 6

							in_array = False
							specs_array = []
							num_string = ""

							init_dict["Tiles"][current_tile]["Collision"] = []
						
						if line[char_i : char_i + 8] == '#specs2:':
							current_key = '#specs2:'
							char_i += 7

							in_array = False
							specs_array = []
							num_string = ""

						if line[char_i : char_i + 4] == "#tp:":
							current_key = "#tp:"
							char_i += 3

							in_string = False
							string = ""
						
						if line[char_i : char_i + 9] == "#bfTiles:":
							current_key = "#bfTiles:"
							char_i += 8

							num_string = ""
						
						if line[char_i : char_i + 5] == "#rnd:":
							current_key = "#rnd:"
							char_i += 4

							num_string = ""
						
						if line[char_i : char_i + 9] == "#repeatL:":
							current_key = "#repeatL:"
							char_i += 8

							in_array = False
							layer_array = []
							num_string = ""
						
						if line[char_i : char_i + 6] == "#tags:":
							current_key = "#tags:"
							char_i += 5

							in_array = False
							tags_array = []
							string = ""


				case "#nm:":
					if char == '"':
						in_string = not in_string

						if in_string == False:
							if string not in init_dict["Tiles"]:
								init_dict["Tiles"][string] = {}

							#if "Categories" not in init_dict["Tiles"][string]:
							#	init_dict["Tiles"][string]["Categories"] = []
							
							#init_dict["Tiles"][string]["Categories"].append(current_category)

							init_dict["Tile Categories"][current_category].append(string)

							current_tile = string

							init_dict["Tiles"][current_tile]["Display Name"] = string

							current_key = "None"

					else:
						if in_string:
							string += char
				
				case '#sz:point':
					match char:
						case "(":
							in_point = True
					
						case ',':
							point[point_index] = int(num_string)

							point_index += 1
							num_string = ""

						case ")":
							point[point_index] = int(num_string)

							in_point = False
							
							init_dict["Tiles"][current_tile]["Size"] = point

							current_key = "None"

						case _:
							num_string += char
				
				case '#specs:':
					match char:
						case "[":
							in_array = True
					
						case ',':
							specs_array.append(int(num_string))

							num_string = ""

						case "]":
							specs_array.append(int(num_string))

							in_array = False
							
							init_dict["Tiles"][current_tile]["Collision"].append(specs_array)

							current_key = "None"

						case _:
							num_string += char
				
				case '#specs2:':
					if line[char_i : char_i + 4] == "void":
						current_key = "None"
					
					match char:
						case "0":
							if in_array == False:
								current_key = "None"

						case "[":
							in_array = True
					
						case ',':
							if num_string != '':
								specs_array.append(int(num_string))

							num_string = ""

						case "]":
							if num_string != '':
								specs_array.append(int(num_string))

							in_array = False
							
							init_dict["Tiles"][current_tile]["Collision"].append(specs_array)

							current_key = "None"

						case _:
							if char != " ":
								num_string += char
				
				case '#tp:':
					if char == '"':
						in_string = not in_string

						if in_string == False:
							match string:
								case "voxelStruct":
									string = "Standard"
								case "voxelStructRockType":
									string = "Rock"
								case "voxelStructSandType":
									string = "Sand"
								case "voxelStructRandomDisplaceHorizontal":
									string = "Displace X"
								case "voxelStructRandomDisplaceVertical":
									string = "Displace Y"
								case "box":
									string = "Box"

							init_dict["Tiles"][current_tile]["Type"] = string

							current_key = "None"

					else:
						if in_string:
							string += char
				
				case "#repeatL:":
					match char:
						case "[":
							in_array = True
					
						case ',':
							layer_array.append(int(num_string))

							num_string = ""

						case "]":
							layer_array.append(int(num_string))

							in_array = False
							
							init_dict["Tiles"][current_tile]["Repeat Layers"] = layer_array

							current_key = "None"

						case _:
							num_string += char

				case "#bfTiles:":
					if char == ",":
						init_dict["Tiles"][current_tile]["Buffer Cells"] = int(num_string)

						current_key = "None"

					else:
						num_string += char
				
				case "#rnd:":
					if char == ",":
						init_dict["Tiles"][current_tile]["Variations"] = int(num_string)

						current_key = "None"

					else:
						num_string += char
				
				case "#tags:":
					match char:
						case "[":
							in_array = True
					
						case ',':
							tags_array.append(string)

							string = ""

						case "]":
							if string != '':
								tags_array.append(string)

							in_array = False
							
							init_dict["Tiles"][current_tile]["Tags"] = tags_array

							current_key = "None"

						case _:
							if char != '"':
								string += char
		else:
			match char:
				case '"':
					in_string = not in_string

					if in_string == False:
						current_category = "-" + string

						init_dict["Tile Categories"][current_category] = []

						init_dict["Tile Categories"]["-root"].append(current_category)
				
				case _:
					if in_string:
						string += char

		char_i += 1
	
	if current_tile != "":
		init_dict["Tiles"][current_tile]["Notes"] = []
		init_dict["Tiles"][current_tile]["Authors"] = ""


props_file = open(paths.input_props_init)
props_lines = props_file.readlines()
props_file.close()

current_category = ""
for line in props_lines:
	current_tile = ""
	current_key = "None"

	in_string = False
	string = ""


with open("Init.json", "w") as outfile:
	outfile.write(pprint.pformat(init_dict, indent=0, compact=True).replace("'",'"'))
