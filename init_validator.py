init_path = "/home/seroen/Documents/rw-modding/Henrys/output-test/assets/renderer/Props/Init.txt"


init_file = open(init_path, "r")
init_lines = init_file.readlines()
init_file.close()

line_number = 0
for line in init_lines:
	line_number += 1
	if line[0] == "\n":
		continue

	if line[0] == "-":
		continue
	
	if line[-2] != "]" and line[-3] != "]":
		print(line)

	# i = 0
	# for char in line:
	# 	match i:
	# 		case 0:
	# 			if char != '[':
	# 				print(f"Missing Starting Bracket at {line_number}!")
	# 		case 1:
	# 			if char != '#':
	# 				print(f"Missing nm # at {line_number}!")
	# 		case 2:
	# 			if char != 'n':
	# 				print("Missing nm data header")
	# 		case 3:
	# 			if char != 'm':
	# 				print("Missing nm data header")

		# i += 1
	
	#print(line[:-1])