from json import dump

# Edge input
with open("rawEdge.csv", "r") as inFile:
    line = inFile.readline()
    l = line.replace('|', '').replace('\"', '\'').split('}, {')
with open("rawEdge.json", "w") as outFile:
    for st in l:
        stt = '{' + st + '}'
        stt = stt.replace('{', '{\'').replace(':', '\':').replace(', ', ', \'')
        temp = eval(stt)
        dump(temp, outFile)
        outFile.write('\n')

# Vertex input
with open("rawVertex.csv", "r") as inFile:
    line = inFile.readline()
    l = line.replace('|', '').replace('\"', '\'').split('}, {')
with open("rawVertex.json", "w") as outFile:
    for st in l:
        stt = '{' + st + '}'
        stt = stt.replace('{', '{\'').replace(':', '\':').replace(', ', ', \'')
        temp = eval(stt)
        dump(temp, outFile)
        outFile.write('\n')
