from json import dump
text_file = open("raw.csv", "r")
line = text_file.readline()
list = line.replace('|', '').replace('\"', '\'').split('}, {')
ans = []
with open("raw.json", "w") as file:
    for st in list:
        stt = '{' + st + '}'
        stt = stt.replace('{', '{\'').replace(':', '\':').replace(', ', ', \'')
        temp = eval(stt)
        ans.append(temp)
        dump(temp, file)
        file.write('\n')
