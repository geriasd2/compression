class node:

    def __init__(self, idx, chars):
        self.idx = idx
        self.chars = chars
    
    def __eq__(self, chars):
        return self.chars == chars
    
    def __repr__(self):
        return "{} {}".format(self.idx, self.chars)


def lz78Encode(data):
    codeBook = []
    codeBook.append(node(0, ""))
    chars = ""
    matchIdx = 0
    for char in data:
        chars += char
        if chars not in codeBook:
            codeBook.append(node(matchIdx, chars))
            chars = ""
            matchIdx = 0
            continue
        matchIdx = codeBook.index(chars)
    codeBook = [node(element.idx, element.chars[-1]) for element in codeBook[1:]]
    return codeBook
        
        
        

if __name__ == "__main__":
    test = lz78Encode("test text for lz78")
