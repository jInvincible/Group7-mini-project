main = 'BusinessTravel'
title = ''
for i in range(len(main)):
    if i != 0:
        if main[i].isupper():
            title += f' {main[i]}'
        else:
            title += main[i]
    else:
        title += main[i]

print(dir(list))