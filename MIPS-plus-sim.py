import linecache

regs = (
'$0', '$8', '$9', '$10', '$11', '$12', '$13', '$14', '$15', '$16', '$17', '$18', '$19', '$20', '$21', '$22', '$23',
'lo', 'hi', 'pc')

regArray = [0]
for x in range(0, 20):
    regArray.append(0)

memArray = [0]
for x in range(0, 4096):
    memArray.append(0)


# 8192 is starter

def hexToDec(hexint):
    trueAddress = int(str(hexint), 16)
    return trueAddress


def hexToDecA(hexint):
    trueAddress = int(hexint, 16) - 8192
    return trueAddress


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def twos_complement(hexstr):
    try:
        value = int(hexstr, 16)
        if value & (1 << (8 - 1)):
            value -= 1 << 8
        return value
    except TypeError:
        return hexstr


def toShex(val, nbits):
    return hex((val + (1 << nbits)) % (1 << nbits))


def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0
    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')
    for line in asm:
        line = line.replace(" ", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(lineCount)  # append the label's index
            asm[lineCount] = line[line.index(":") + 1:]
        lineCount += 1


def main():
    PC = 0
    count = 0
    labelIndex = []
    labelName = []
    f = open("mc.txt", "w+")
    h = open("Hash-MIPS-default.asm", "r")
    asm = h.readlines()

    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')
    length = len(asm)
    saveJumpLabel(asm, labelIndex, labelName)  # Save all jump's destinations
    n = 0
    while n < length:
        lineParse = asm[n]
        print(lineParse)
        f.write("\n" + lineParse + "\n")


        lineParse = lineParse.replace("\n", "")  # Removes extra chars
        # lineParse = lineParse.replace("$", "")
        lineParse = lineParse.replace(" ", "")
        lineParse = lineParse.replace("(", ",")
        lineParse = lineParse.replace(")", ",")
        lineParse = lineParse.replace("zero", "0")  # assembly can also use both $zero and $0

        if (lineParse[0:4] == "addi"):  # ADD

            lineParse = lineParse.replace("addi", "")
            lineParse = lineParse.split(",")
            r1 = regArray[regs.index(lineParse[0])]
            r2 = regArray[regs.index(lineParse[1])]
            r3 = lineParse[2]
            if is_number(r3) is True:
                f.write("number \n")
                value = (hexToDec(str(r2)) + int(r3))

                f.write(hex(value) + "\n")

                regArray[regs.index(lineParse[0])] = toShex(value, 32)

            else:
                f.write("hex \n")
                value = twos_complement(r2) + hexToDec(r3)
                regArray[regs.index(lineParse[0])] = toShex(value, 32)

                f.write(hex(value) + "\n")
            print('Added ' + str(r2) + " in " + lineParse[1] + ' and ' + str(r3) + " which gives: " + hex(
                value) + " in " + lineParse[0] + "\n")
            f.write('Added ' + str(r2) + " in " + lineParse[1] + ' and ' + str(r3) + " which gives: " + hex(
                value) + " in " + lineParse[0] + "\n")

        elif (lineParse[0:3] == "add"):  # ADD
            lineParse = lineParse.replace("add", "")
            lineParse = lineParse.split(",")
            r1 = regArray[regs.index(lineParse[0])]
            r2 = regArray[regs.index(lineParse[1])]
            r3 = regArray[regs.index(lineParse[2])]

            value = hexToDec(r2) + hexToDec(r3)
            regArray[regs.index(lineParse[0])] = toShex(value, 32)
            print('Added ' + str(r2) + " in " + lineParse[1] + ' and ' + str(r3) + " in " + lineParse[
                2] + " which gives: " + hex(value) + " in " + lineParse[0] + "\n")
            f.write('Added ' + str(r2) + " in " + lineParse[1] + ' and ' + str(r3) + " in " + lineParse[
                2] + " which gives: " + hex(value) + " in " + lineParse[0] + "\n")

        elif (lineParse[0:5] == "multu"):  # mult
            lineParse = lineParse.replace("multu", "")
            lineParse = lineParse.split(",")
            regArray[17] = '0'
            regArray[18] = '0'
            r1 = regArray[regs.index(lineParse[0])]
            r2 = regArray[regs.index(lineParse[1])]
            value = hexToDec(str(r1)) * hexToDec(str(r2))

            r3 = hex(value)

            if len(r3) > 10:
                r4 = str("0x" + str(r3[-8:]))
                regArray[17] = r4
                regArray[18] = str(r3[:-8])
            else:
                regArray[17] = r3
            f.write(
                'Multiplied ' + str(r1) + " in " + lineParse[0] + ' with ' + str(r2) + " in " + lineParse[
                    1] + " which gives: " + str(value) + "\n")

        elif (lineParse[0:4] == "hash"):  # mult
            lineParse = lineParse.replace("hash", "")
            lineParse = lineParse.split(",")

            r1 = regArray[regs.index(lineParse[1])]
            r2 = regArray[regs.index(lineParse[2])]
            value = hexToDec(str(r1)) * hexToDec(str(r2))

            r3 = hex(value)

            if len(r3) > 10:
                r4 = str("0x" + str(r3[-8:]))
                r5 = r4
                r6 = str(r3[:-8])
            else:
                r5 = r3
                r6 = str(0)
            r7 = bin(hexToDec(r5))
            r8 = bin(hexToDec(r6))

            r1 = int(r7, 2) ^ int(r8, 2)
            r0 = hex(r1)

            regArray[regs.index(lineParse[0])] = r0

            f.write(
                'Multiplied ' + str(r1) + " in " + lineParse[0] + ' with ' + str(r2) + " in " + lineParse[
                    1] + " which gives: " + str(value) + "\n")


        elif (lineParse[0:4] == "mult"):  # mult
            lineParse = lineParse.replace("mult", "")
            lineParse = lineParse.split(",")
            regArray[17] = '0'
            regArray[18] = '0'
            r1 = regArray[regs.index(lineParse[0])]
            r2 = regArray[regs.index(lineParse[1])]
            value = twos_complement(r1) * twos_complement(r2)
            r3 = toShex(value, 32)

            if len(r3) > 10:
                r4 = r3[:2] + r3[-8:]
                regArray[17] = r4
                regArray[18] = ("0x" + r3[2:-8])
            else:
                regArray[17] = r3
            print('Multiplied ' + str(r1) + " in " + lineParse[0] + ' with ' + str(r2) + " in " + lineParse[
                1] + " which gives: " + str(value) + "\n")
            f.write('Multiplied ' + str(r1) + " in " + lineParse[0] + ' with ' + str(r2) + " in " + lineParse[1] + " which gives: " + str(value) + "\n")

        elif (lineParse[0:2] == "sb"):  # mult
            lineParse = lineParse.replace("sb", "")
            lineParse = lineParse.split(",")
            r1 = regArray[regs.index(lineParse[0])]
            print(r1)
            k=0
            while k < 2:
                if (r1[k] == 'x'):
                    r1 = r1[k+1:]
                k = k + 1
            r1 = r1[-2:]
            r1 = (str('0x') + r1)
            r2 = int(lineParse[1])
            r3 = regArray[regs.index(lineParse[2])]
            address = hexToDecA(r3) + r2
            memArray[address] = r1
            f.write('Stored ' + str(r1) + " with an offset of " + str(r2) + " into " + hex(address + 8192) + "\n")

        elif (lineParse[0:4] == "andi"):  # mult
            lineParse = lineParse.replace("andi", "")
            lineParse = lineParse.split(",")
            r2 = str((regArray[regs.index(lineParse[1])]))
            r3 = str(lineParse[2])
            r2 = bin(hexToDec(r2))
            r3 = bin(hexToDec(r3))
            print("r2: " + r2)
            print("r3: " + r3)
            r4 = str('')
            if len(r2) < len(r3):
                andLength = len(r2)
            else:
                andLength = len(r3)
            b = 1
            print("length: " + str(andLength))
            while b < andLength + 1:
                if r2[-b] == r3[-b]:
                    r4 = str(str(r3[-b]) + r4)
                elif r2[-b] != r3[-b]:
                    r4 = str(0) + r4
                b = b + 1
            r4 = int(r4,2 )
            r4 = hex(r4)
            r4 = r4.replace("0x", "")
            if (len(r4) % 2 == 1):
                r4 = str('0' + r4)
            r4 = ('0x' + r4)
            regArray[regs.index(lineParse[0])] = r4

            print("ANDI: " + r4)

            print('Compared ' + str(regArray[regs.index(lineParse[1])]) + " with " + lineParse[2] + " and returning " + str(r4) + "\n")
            f.write('Compared ' + str(regArray[regs.index(lineParse[1])]) + " with " + lineParse[
                2] + " and returning " + str(r4) + "\n")
        elif (lineParse[0:2] == "lb"):  # mult
            lineParse = lineParse.replace("lb", "")
            lineParse = lineParse.split(",")
            r2 = int(lineParse[1])
            r3 = regArray[regs.index(lineParse[2])]
            address = hexToDecA(r3) + r2
            r1 = str(memArray[address])
            regArray[regs.index(lineParse[0])] = r1

            f.write('Loaded ' + str(r1) + " from " + hex(address + 8192) + " with an offset of " + str(r2) + " into " +
                    lineParse[0] + "\n")

        elif (lineParse[0:4] == "mflo"):  # mult
            lineParse = lineParse.replace("mflo", "")
            lineParse = lineParse.split(",")
            regArray[regs.index(lineParse[0])] = regArray[17]
            print('Loaded ' + str(regArray[17]) + " from LO into " + str(lineParse[0]) + "\n")
            f.write('Loaded ' + str(regArray[17]) + " from LO into " + str(lineParse[0]) + "\n")

        elif (lineParse[0:4] == "mfhi"):  # mult
            lineParse = lineParse.replace("mfhi", "")
            lineParse = lineParse.split(",")
            regArray[regs.index(lineParse[0])] = regArray[18]
            print('Loaded ' + str(regArray[18]) + " from HI into " + str(lineParse[0]) + "\n")
            f.write('Loaded ' + str(regArray[18]) + " from HI into " + str(lineParse[0]) + "\n")

        elif (lineParse[0:2] == "sw"):  # mult
            lineParse = lineParse.replace("sw", "")
            lineParse = lineParse.split(",")
            r1 = regArray[regs.index(lineParse[0])]
            r2 = int(lineParse[1])
            r3 = regArray[regs.index(lineParse[2])]
            address = hexToDecA(r3) + r2
            memArray[address] = r1
            print('Stored ' + str(r1) + " with an offset of " + str(r2) + " into " + hex(address + 8192) + "\n")
            f.write('Stored ' + str(r1) + " with an offset of " + str(r2) + " into " + hex(address + 8192) + "\n")

        elif (lineParse[0:2] == "sw"):  # mult
            lineParse = lineParse.replace("sw", "")
            lineParse = lineParse.split(",")
            r1 = regArray[regs.index(lineParse[0])]
            r2 = int(lineParse[1])
            r3 = regArray[regs.index(lineParse[2])]
            address = hexToDecA(r3) + r2
            memArray[address] = r1

            f.write('Stored ' + str(r1) + " with an offset of " + str(r2) + " into " + hex(address + 8192) + "\n")
        elif (lineParse[0:2] == "lw"):  # mult
            lineParse = lineParse.replace("lw", "")
            lineParse = lineParse.split(",")
            r2 = int(lineParse[1])
            r3 = regArray[regs.index(lineParse[2])]
            address = hexToDecA(r3) + r2
            regArray[regs.index(lineParse[0])] = memArray[address]
            f.write('Loaded ' + str(r1) + " from " + hex(address + 8192) + " with an offset of " + str(r2) + " into " +
                    lineParse[0] + "\n")
            print('Loaded ' + str(r1) + " from " + hex(address + 8192) + " with an offset of " + str(r2) + " into " +
                    lineParse[0] + "\n")

        elif (lineParse[0:4] == "slti "):  # mult
            lineParse = lineParse.replace("slti", "")
            lineParse = lineParse.split(",")
            r2 = regArray[regs.index(lineParse[1])]
            r2 = twos_complement(r2)
            r3 = lineParse[2]
            if r2 < r3:
                regArray[regs.index(lineParse[0])] = hex(1)
                f.write(
                    'Comparing ' + str(r2) + " with " + str(r3) + ": 1 has been written into " + lineParse[0] + "\n")
            else:
                regArray[regs.index(lineParse[0])] = hex(0)
                f.write(
                    'Comparing ' + str(r2) + " with " + str(r3) + ": 0 has been written into " + lineParse[0] + "\n")

        elif (lineParse[0:4] == "sltu"):  # mult
            lineParse = lineParse.replace("sltu", "")
            lineParse = lineParse.split(",")
            r2 = regArray[regs.index(lineParse[1])]
            r3 = regArray[regs.index(lineParse[2])]
            r2 = hexToDec(r2)
            r3 = hexToDec(r3)
            if r2 < r3:
                regArray[regs.index(lineParse[0])] = hex(1)
                f.write(
                    'Comparing ' + str(r2) + " with " + str(r3) + ": 1 has been written into " + lineParse[0] + "\n")
            else:
                regArray[regs.index(lineParse[0])] = hex(0)
                f.write(
                    'Comparing ' + str(r2) + " with " + str(r3) + ": 0 has been written into " + lineParse[0] + "\n")


        elif (lineParse[0:3] == "slt"):  # mult
            lineParse = lineParse.replace("slt", "")
            lineParse = lineParse.split(",")
            r2 = regArray[regs.index(lineParse[1])]
            r3 = regArray[regs.index(lineParse[2])]
            r2 = twos_complement(r2)
            r3 = twos_complement(r3)
            if r2 < r3:
                regArray[regs.index(lineParse[0])] = 1
                f.write(
                    'Comparing ' + str(r2) + " with " + str(r3) + ": 1 has been written into " + lineParse[0] + "\n")
            else:
                regArray[regs.index(lineParse[0])] = 0
                f.write(
                    'Comparing ' + str(r2) + " with " + str(r3) + ": 0 has been written into " + lineParse[0] + "\n")

        elif (lineParse[0:3] == "srl"):  # ADD
            lineParse = lineParse.replace("srl", "")
            lineParse = lineParse.split(",")
            r5 = str(regArray[regs.index(lineParse[1])])
            r2 = bin(hexToDec(r5))[2:]
            r3 = int(lineParse[2])
            r1 = str(('0' * r3) + r2[:-r3])
            r1 = hex(int(r1, 2))
            f.write("shift logic right result: " +r1)
            regArray[regs.index(lineParse[0])] = r1
            print("Shifting " + r5 + " by " +str(r3) +". Resulting in " + r1 )

        elif (lineParse[0:3] == "sll"):  # ADD
            lineParse = lineParse.replace("sll", "")
            lineParse = lineParse.split(",")
            r2 = str(regArray[regs.index(lineParse[1])])
            r2 = bin(hexToDec(r2))[2:]
            print(r2)
            r3 = int(lineParse[2])
            r1 = str(r2 + ('0' * r3))
            print(r1)
            r1 = hex(int(r1, 2))
            f.write("shift logic left result: " +r1)
            regArray[regs.index(lineParse[0])] = r1

        elif (lineParse[0:3] == "ori"):  # ADD
            lineParse = lineParse.replace("ori", "")
            lineParse = lineParse.split(",")
            r2 = regArray[regs.index(lineParse[1])]
            r3 = lineParse[2]
            r3 = r3[-4:]
            r4 = r2[:6]
            r1 = str(r4 + r3)
            regArray[regs.index(lineParse[0])] = r1

        elif (lineParse[0:3] == "lui"):  # ADD
            lineParse = lineParse.replace("lui", "")
            lineParse = lineParse.split(",")
            r2 = lineParse[1]
            regArray[regs.index(lineParse[0])] = r2

        elif (lineParse[0:3] == "xor"):  # ADD
            lineParse = lineParse.replace("xor", "")
            lineParse = lineParse.split(",")
            r5 = regArray[regs.index(lineParse[1])]
            r6 = regArray[regs.index(lineParse[2])]
            print(r5)
            print(r6)
            r2 = bin(hexToDec(r5))
            r3 = bin(hexToDec(r6))

            r1 = int(r2, 2) ^ int(r3, 2)
            r1 = hex(r1)

            regArray[regs.index(lineParse[0])] = r1
            print("XOR'ing " + r5 +" and " +r6)
            print('Inputting ' + r1 + " into " +str(lineParse[0]))

        elif (lineParse[0:3] == "bne"):  # JUMP
            lineParse = lineParse.replace("bne", "")
            lineParse = lineParse.split(",")
            r1 = regArray[regs.index(lineParse[0])]
            r2 = regArray[regs.index(lineParse[1])]
            print("r1: " + str(r1))
            print("r2: " + str(r2))
            r1 = hexToDec(r1)
            r2 = hexToDec(r2)

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location
            f.write('Comparing ' + str(r1) + ' and ' + str(r2) + "\n")
            if (r1 != r2):
                print("comparing\n")
                if (is_number(lineParse[2]) == True):  # First,test to see if it's a label or a integer
                    n = n + int(lineParse[2])
                    f.write('Jumping to ' + lineParse[2] + "\n")
                else:  # Jumping to label

                    for i in range(len(labelName)):
                        if (labelName[i] == lineParse[2]):
                            n = int(labelIndex[i])
                            f.write('Jumping to ' + lineParse[2] + "\n")

        elif (lineParse[0:3] == "beq"):  # JUMP
            lineParse = lineParse.replace("beq", "")
            lineParse = lineParse.split(",")
            r1 = twos_complement(regArray[regs.index(lineParse[0])])
            r2 = twos_complement(regArray[regs.index(lineParse[1])])
            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location
            f.write('Comparing ' + str(r1) + ' and ' + str(r2) + "\n")
            if (r1 == r2):
                print("comparing\n")
                if (is_number(lineParse[2]) == True):  # First,test to see if it's a label or a integer
                    n = n + int(lineParse[2])
                    f.write('Jumping to ' + lineParse[2] + "\n")

                else:  # Jumping to label

                    for i in range(len(labelName)):
                        if (labelName[i] == lineParse[2]):
                            n = int(labelIndex[i])
                            f.write('Jumping to ' + lineParse[2] + "\n")

        elif (lineParse[0:1] == "j"):  # JUMP
            lineParse = lineParse.replace("j", "")
            lineParse = lineParse.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            print("comparing\n")
            if (is_number(lineParse[0]) == True):  # First,test to see if it's a label or a integer
                n = n + int(lineParse[0])

            else:  # Jumping to label

                for i in range(len(labelName)):
                    if (labelName[i] == lineParse[0]):
                        n = int(labelIndex[i] + 1)
            f.write('Jumping to ' + lineParse[0] + "\n")
        n += 1
        PC = PC + 1
    regArray[19] = (PC * 4)
    f.write("\nUtilized Registers:" + "\n")
    for x in range(0, 20):
        if regArray[x] != 0:
            f.write(str(regs[x]) + ": " + str(regArray[x]) + "\n")

    f.write("\nUtilized Memory Addresses:" + "\n")
    for x in range(0, 4096):
        if memArray[x] != 0:
            f.write(hex(x + 8192) + ": " + str(memArray[x]) + "\n")
    f.close()
    regArray[20] = PC

    print("\nUtilized Registers:")
    for x in range(0, 20):
        if regArray[x] != 0:
            print(str(regs[x]) + ": " + str(regArray[x]))

    print("\nUtilized Memory Addresses:")
    for x in range(0, 4096):
        if memArray[x] != 0:
            print(hex(x + 8192) + ": " + str(memArray[x]))
    print("Instruction Count: " +str(PC))


if __name__ == "__main__":
    main()