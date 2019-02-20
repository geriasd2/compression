import math
import sys

def readNextHeader(f):
    header = ""
    while True:
        byte = f.read(1)
        if byte == b"\x0a":
            return header
        header += byte.decode()


def readGeriFile(f):
    numOfValues = int(readNextHeader(f))
    extension = readNextHeader(f)
    numOfCutIndexes = math.ceil(numOfValues * 3 / 8)

    cutIndexes = list(f.read(int(numOfCutIndexes)))
    print(f.read(1))
    binaryData = list(f.read())
    return numOfValues, extension, cutIndexes, binaryData

def transFormRepresentation(cutIndexes, binaryData):
    cutIndexes = "".join(["{0:08b}".format(byte) for byte in cutIndexes])
    cutIndexes = [int(cutIndexes[i:i+3], 2) + 1 for i in range(0, len(cutIndexes), 3)]

    print(len(cutIndexes))
    binaryData = "".join(["{0:08b}".format(byte) for byte in binaryData])
    
    decodedValues = []
    i = 0
    for cutLength in cutIndexes[:-1]:
        decodedValues.append(int(binaryData[i : i + cutLength], 2))
        i += cutLength
    lastVal = list(binaryData[i:])
    print(len(lastVal))
    while len(lastVal) > 8:
        del lastVal[-8]
    lastVal = "".join(lastVal)
    decodedValues.append(int(lastVal, 2))

    return decodedValues


if __name__ == "__main__":
    
    filename, _ = sys.argv[1].split(".")
    #filename = "test"
    numOfValues, extension, cutIndexes, binaryData = 0, "", [], []
    with open("{}.{}".format(filename, "geri"), "rb") as f:
        numOfValues, extension, cutIndexes, binaryData = readGeriFile(f)

    decodedValues = transFormRepresentation(cutIndexes, binaryData)
    with open("{}.{}".format(filename, extension), "wb") as f:
        f.write(bytearray(decodedValues))
