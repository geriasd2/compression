import sys

def getRepresentation(f):
    cutIndexes, bitStream, byteLength = "", "", 0 
    while True:
        byte = f.read(1)
        if not byte:
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
    for i in cutIndexes:
        #print(i)
        bitStreamedFile.write(i)
    bitStreamedFile.write(b"\n")
    #write bitstream as bytes
    for i in bitStream:
        bitStreamedFile.write(i)

def convertToByte(binary):
    return bytes([int(binary, 2)])

def transformRepresentation(cutIndex, bitStream):

    #Trafo cutindexes into bytes
    cutIndexesList = [cutIndex[i:i+8] for i in range(0, len(cutIndex), 8)]
    print(len(cutIndex))
    print(cutIndexesList[-1])
    cutIndexesList = list(map(convertToByte, cutIndexesList))

    #Trafo bitstream into bytes
    bitStreamList = [bitStream[i:i+8] for i in range(0, len(bitStream), 8)]
    bitStreamList = list(map(convertToByte, bitStreamList))

    return cutIndexesList, bitStreamList
    

if __name__ == "__main__":

    filename, extension = sys.argv[1].split(".")
    #filename, extension = "sample2", "data"
  
    cutIndex, bitStream, byteLength = "", "", 0
    with open("{}.{}".format(filename, extension), "rb") as f:
        cutIndex, bitStream, byteLength = getRepresentation(f)

    cutIndex, bitStream = transformRepresentation(cutIndex, bitStream)
    
    with open("{}.{}".format(filename, "geri"), "wb") as f:
        writeAsBitStream(f, extension, cutIndex, bitStream, byteLength)