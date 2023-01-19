import names


i = 0
while (i < 5):
    name = names.get_full_name()
    if len(name) == 9:
        print(name)
        i = i+1
