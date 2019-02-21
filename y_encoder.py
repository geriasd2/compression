def y_encode(number):
    binary_form = "{0:b}".format(number + 1)
    y_encoded = ""
    for _ in binary_form[:-1]:
        y_encoded += "0"
    return y_encoded + binary_form


if __name__ == "__main__":
    values = []
    with open("sample1.data", "rb") as f:
        values = f.read()
        numOfVals = len(values)
        values = list(map(y_encode, values))
        values = [values[i:i+8] for i in range(0, len(values), 8)]
        values = list(map(lambda x: "".join(x), values))
        values = list(map(lambda x: int(x, 2), values))
        
    with open("test.data", "wb") as f:
        f.write(bytearray(values))
