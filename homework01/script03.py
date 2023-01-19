import names


def len_name(name):
    return len(name) - 1


name_list = []
for i in range(5):
    name_list.append(names.get_full_name())

for name in name_list:
    print(name, len_name(name), '\n')
