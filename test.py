a = "123456789"

a = list(a)

while len(a) != 8:
    del a[-8]
    print(len(a))
print("".join(a))