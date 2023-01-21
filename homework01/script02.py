import names


# generate 5 full names with character lengths of 8 (excluding spaces)
i = 0
while (i < 5):
    name = names.get_full_name()
    if len(name) == 9:
        print(name)
        i = i+1
