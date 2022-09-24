g_hcheck = ['Guillermo Stábile', "G 12', 13'", "12'", "'", "13'", "'", 'Mario Evaristo', "G 51'", "51'", "'"]
for item in g_hcheck:
    if item == "'":
        list.remove(g_hcheck, item)
    if len(item) == 3:
        list.remove(g_hcheck, item)