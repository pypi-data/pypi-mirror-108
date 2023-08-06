import numpy
import string


# Convert ASCII to Decimal (1 letter).
def ASCII_DECIMAL(ASCII_Character):
    return ord(ASCII_Character)


# Convert ASCII to Decimal (array).
def ASCII_DECIMAL_ARRAY(ASCII_Array):
    temp = []
    for i in ASCII_Array:
        temp.append(ord(i))
    return temp


# Convert ASCII to HEX (1 letter).
def ASCII_HEX(ASCII_Character):
    return format(ord(ASCII_Character), "x").zfill(2).upper()


# Convert ASCII to HEX (array).
def ASCII_HEX_ARRAY(ASCII_Array):
    temp = []
    for i in ASCII_Array:
        temp.append(format(ord(i), "x").zfill(2).upper())
    return temp


# Convert ASCII to Binary (1 letter).
def ASCII_BINARY(ASCII_Character):
    return format(ord(ASCII_Character), "b").zfill(8)


# Convert ASCII to HEX (array).
def ASCII_BINARY_ARRAY(ASCII_Array):
    temp = []
    for i in ASCII_Array:
        temp.append(format(ord(i), "b").zfill(8))
    return temp


# Convert ASCII to HEX (1 Byte).
def HEX_ASCII(HEX_Number):
    if HEX_Number[:2] == "0x":
        bytes_object = bytes.fromhex(HEX_Number[2:])
        return bytes_object.decode("ASCII")
    else:
        bytes_object = bytes.fromhex(HEX_Number)
        return bytes_object.decode("ASCII")


# Convert ASCII to HEX (Array).
def HEX_ASCII_ARRAY(HEX_Array):
    temp = []
    for i in HEX_Array:
        if i[:2] == "0x":
            bytes_object = bytes.fromhex(i[2:])
            temp.append(bytes_object.decode("ASCII"))

        else:
            bytes_object = bytes.fromhex(i)
            temp.append(bytes_object.decode("ASCII"))
    return temp


# Convert ASCII to Decimal (1 Byte).
def HEX_DECIMAL(HEX_Number):
    if HEX_Number[:2] == "0x":
        return int(HEX_Number[2:], 16)
    else:
        return int(HEX_Number, 16)


# Convert ASCII to Decimal (Array).
def HEX_DECIMAL_ARRAY(HEX_Array):
    temp = []
    for i in HEX_Array:
        if i[:2] == "0x":
            temp.append(int(i[2:], 16))
        else:
            temp.append(int(i, 16))
    return temp


# Convert ASCII to Binary (1 Byte).
def HEX_BINARY(HEX_Number):
    if HEX_Number[:2] == "0x":
        return bin(int(HEX_Number[2:], 16))[2:].zfill(8)
    else:
        return bin(int(HEX_Number, 16))[2:].zfill(8)


# Convert ASCII to Binary (Array).
def HEX_BINARY_ARRAY(HEX_Array):
    temp = []
    for i in HEX_Array:
        if i[:2] == "0x":
            temp.append(bin(int(i[2:], 16))[2:].zfill(8))
        else:
            temp.append(bin(int(i, 16))[2:].zfill(8))
    return temp

