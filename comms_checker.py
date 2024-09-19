import paths


category = ""
max_len = 43 #29
current_len = 0


init_file = open(paths.input_classic_init)
init_lines = init_file.readlines()
init_file.close()


for line in init_lines:
	if line != "\n":
		if line[0] == "-":
			if current_len > max_len:
				print(category)

			category = line
			current_len = 0
		
		else:
			current_len += 1
			if current_len == max_len:
				print(line[:-1])
