import paths

input_init_file = open(paths.input_classic_init)
input_init_lines = input_init_file.readlines()
input_init_file.close()

compare_init_file = open(paths.input_reorganized_init)
compare_init_lines = compare_init_file.readlines()
compare_init_file.close()


count = 0
for line in compare_init_lines:
	if line != "/n" and line[0] != "-":
		if line not in input_init_lines:
			print(line[:-1])
			count += 1

print(count)
