import sys

def getRepresentation(f):
    cutIndexes, bitStream, byteLength = "", "", 0 
    bitRepresentation = None
    while True:
        byte = f.read(1)
        if not byte:
            print(len(bitStream))
            return cutIndexes, bitStream, byteLength
        
        bitRepresentation = "{0:b}".format(ord(byte))
        cutIndexes += ("{0:03b}".format(len(bitRepresentation) - 1))
        bitStream += bitRepresentation
        byteLength += 1

def writeAsBitStream(bitStreamedFile, extension, cutIndexes, bitStream, byteLength):
    #write how many values are coded
    bitStreamedFile.write(str(byteLength).encode())
    bitStreamedFile.write(b"\n")

    #Original extension
    bitStreamedFile.write(extension.encode())
    bitStreamedFile.write(b"\n")

    #write length of values encoded as bits
    bitStreamedFile.write(bytearray(cutIndexes))
    bitStreamedFile.write(b"\n")
    #write bitstream as bytes
    bitStreamedFile.write(bytearray(bitStream))
    
def transformRepresentation(cutIndex, bitStream):

    #Trafo cutindexes into bytes
    cutIndexesList = [cutIndex[i:i+8] for i in range(0, len(cutIndex), 8)]
    cutIndexesList = list(map(lambda x: int(x, 2), cutIndexesList))

    #Trafo bitstream into bytes
    print(len(bitStream))
    bitStreamList = [bitStream[i:i+8] for i in range(0, len(bitStream), 8)]
    """
    while(len(bitStreamList[-1]) != 8):
        bitStreamList[-1] = "0" + bitStreamList[-1] 
    """
    print(bitStreamList[-1])
    print(bitStreamList[-2])
    bitStreamList = list(map(lambda x: int(x, 2), bitStreamList))

    return cutIndexesList, bitStreamList
    

def checkCorrectness(cutIndex, bitStream):
    cutIndex2 = "".join(["{0:08b}".format(element) for element in cutIndex])
    if len(cutIndex2) / 3 != 1000000:
        print("error 1")
    
    cutIndex2 = [cutIndex2[i:i+3] for i in range(0, len(cutIndex2), 3)]
    if len(cutIndex2) != 1000000:
        print("error 2")
    bitStream = "".join(["{0:08b}".format(element) for element in bitStream])
    print(len(bitStream))
    return

    i = 0
    with open("sample5.data", "rb") as f:
        idx = 0
        for cut in cutIndex2:
            cut = int(cut, 2)
            val = int(bitStream[i:cut], 2)
            i += cut
            if val > 255:
                print("error 3")
            byte = chr(val)
            byte2 = f.read(1)
            if byte != byte2:
                print("error 4")
                print(byte)
                print(byte2)
                print(idx)
                print("--------------")
            idx += 1


if __name__ == "__main__":

    filename, extension = sys.argv[1].split(".")
    #filename, extension = "sample5", "data"
  
    cutIndex, bitStream, byteLength = "", "", 0
    with open("{}.{}".format(filename, extension), "rb") as f:
        cutIndex, bitStream, byteLength = getRepresentation(f)

    cutIndex, bitStream = transformRepresentation(cutIndex, bitStream)

    with open("{}.{}".format(filename, "geri"), "wb") as f:
        writeAsBitStream(f, extension, cutIndex, bitStream, byteLength)