from json import dump

# Edge input
with open("rawEdge.csv", "r") as inFile:
    line = inFile.readline()
    l = line.replace('|', '').replace('\"', '\'').split('}, {')
with open("rawEdge.json", "w") as outFile:
    for st in l:
        stt = '{' + st + '}'
        stt = stt.replace('{', '{\'').replace(':', '\':').replace(', ', ', \'')
        data = eval(stt)
        # parsing type
        slope = data["slope"]
        data["slope"] = int(slope) if slope else 0
        fr = data["from"]
        data["from"] = int(fr) if fr else None
        to = data["to"]
        data["to"] = int(to) if to else None
        width = data["width"]
        data["width"] = float(width) if width else None
        length = data["length"]
        data["length"] = float(length) if length else None
        duplex = data["duplex"]
        data["duplex"] = True if (duplex == "T") else False
        sat = data["sat"]
        data["sat"] = True if (sat == "T") else False
        # save
        dump(data, outFile)
        outFile.write('\n')

# Vertex input
# position
text_file = open("rawPos.csv", "r")
line = text_file.readline()
listPos = line.split('}, {')
ansPos = []
for st in listPos:
    stt = "[" + st + "]"
    temp = eval(stt)
    ansPos.append(temp)
# other data
with open("rawVertex.csv", "r") as inFile:
    line = inFile.readline()
    l = line.replace('|', '').replace('\"', '\'').split('}, {')
with open("rawVertex.json", "w") as outFile:
    i = 0
    for st in l:
        stt = '{' + st + '}'
        stt = stt.replace('{', '{\'').replace(':', '\':').replace(', ', ', \'')
        data = eval(stt)
        # parsing type
        type = data["type"]
        data["type"] = type if type else "normal"
        b = data["b"]
        data["b"] = int(b) if b else 0
        r = data["r"]
        data["r"] = int(r) if r else 0
        num = data["num"]
        data["num"] = int(num) if num else None
        phi = data["phi"]
        data["phi"] = float(phi) if phi else 0
        color = data["color"]
        data["color"] = color if color else "#000000"
        pos = ansPos[i]
        data["pos"] = pos if pos else [0, 0]
        i += 1
        # save
        dump(data, outFile)
        outFile.write('\n')
