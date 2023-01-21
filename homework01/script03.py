import names


def len_name(name):
    return len(name) - 1

# generate list of five names
name_list = []
for i in range(5):
    name_list.append(names.get_full_name())

# print list of names and thier corresponding lengths(omitting the space character)
for name in name_list:
    print(name, len_name(name), '\n')
