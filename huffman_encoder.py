class node:
    def __init__(self, left, right, weight, value=None, bitCode=None):
        self.left = left
        self.right = right
        self.weight = weight
        self.value = value
        self.bitCode = bitCode

    def __repr__(self):
        return "{} -> {}".format(self.value, self.weight)


class generalizedHuffman:
    def __init__(self, symbol, codeLength):
        self.symbol = symbol
        self.codeLength = codeLength

    @classmethod
    def generate(cls, mapping):
        symbol = list(mapping)[0]
        codeLength = len(list(mapping.values())[0])
        return generalizedHuffman(symbol, codeLength)

    def __repr__(self):
        return "{} -> {}".format(self.symbol, self.codeLength)


def transform(content):
    instances = {}
    for byte in content:
        if byte not in instances:
            instances[byte] = 0
        instances[byte] += 1
    instances = [{key: val} for key, val in instances.items()]
    return [node(None, None, list(item.values())[0], list(item)[0]) for item in instances]


def buildHuffmanTree(content):
    while len(content) != 1:
        left = min(content, key=lambda x: x.weight)
        content.remove(left)
        right = min(content, key=lambda x: x.weight)
        content.remove(right)
        combined = node(left, right, left.weight + right.weight, None)
        content.append(combined)
    return content[0]


def assignCode(treeNode, bitCode):
    treeNode.bitCode = bitCode
    if treeNode.left:
        assignCode(treeNode.left, "0")
    if treeNode.right:
        assignCode(treeNode.right, "1")


def code(treeNode, currentCode):
    if not treeNode.left and not treeNode.right:
        # it's leaf then
        treeNode.bitCode = currentCode + treeNode.bitCode
        return
    if treeNode.left:
        code(treeNode.left, currentCode + treeNode.bitCode)
    if treeNode.right:
        code(treeNode.right, currentCode + treeNode.bitCode)


def transformHuffmanTree(treeNode, codeBook):
    if not treeNode.left and not treeNode.right:
        codeBook[treeNode.value] = treeNode.bitCode
        return
    if treeNode.left:
        transformHuffmanTree(treeNode.left, codeBook)
    if treeNode.right:
        transformHuffmanTree(treeNode.right, codeBook)


def huffmanEncode(transformedContent, content):
    rootNode = buildHuffmanTree(transformedContent)
    assignCode(rootNode, "")
    code(rootNode, "")
    codeBook = {}
    transformHuffmanTree(rootNode, codeBook)
    generalizeCodeBook(codeBook)
    print("oi")


def generalizeCodeBook(codeBook):
    codeBook = [{key: value} for key, value in codeBook.items()]
    codeBook = [generalizedHuffman.generate(item) for item in codeBook]
    
    print("e")


if __name__ == "__main__":
    content = None
    with open("sample2.data", "rb") as f:
        #content = f.read()
        content = ["a" for _ in range(10)]
        content += ["b" for _ in range(11)]
        content += ["c" for _ in range(1)]
        content += ["d" for _ in range(4)]
        content += ["e" for _ in range(7)]

    transformedContent = transform(content)
    huffmanEncode(transformedContent, content)


# hw huffman coding implementation
# compare with universal
