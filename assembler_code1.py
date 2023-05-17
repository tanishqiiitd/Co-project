opcode = {
  "add": '00000',
  "sub": '00001',
  "mov": '00010',
  "mov": '00011',
  "ld": '00100',
  "st": '00101',
  'mul': '00110',
  'div': '00111',
  'rs': '01000',
  'ls': '01001',
  'xor': '01010',
  'or': '01011',
  'and': '01100',
  'not': '01101',
  'cmp': '01110',
  'jmp': '01111',
  'jlt': '11100',
  'jgt': '11101',
  'je': '11111',
  'hlt': '11010'
}

register = {
  "R0": '000',
  "R1": '001',
  "R2": '010',
  "R3": '011',
  "R4": '100',
  "R5": '101',
  "R6": '110',
  "FLAGS": '111'
}

f2 = open("output.txt", "w")

#holds label declaration line number
labeldec = {}
#holds label usage line number
labelcall = {}

memory = {}
memvariable = 1


def binaryconvert(number):  #for imm values
  bin = ""
  if number == 0:
    return "0000000"
  while number > 0:
    bin = str(number % 2) + bin
    number = number // 2
  while (len(bin) < 7):
    bin = "0" + bin
  return bin


wordsfinal = []
binarycode = []
errortest = 0

#reading text from input file
f = open("input.txt", "r")
words = f.read()
wordslist = words.split("\n")

for i in wordslist:
  temp = i.split(" ")
  wordsfinal.append(temp)

#error for variables
vartest = 0
insttest = 0

for i in wordsfinal:
  if i[0] in opcode:
    insttest = wordsfinal.index(i)
    break

for i in wordsfinal:
  if i[0] == "var":
    vartest = wordsfinal.index(i)

if vartest > insttest:
  print("error: Variables not declared in the beginning")
  f2.write("error: Variables not declared in the beginning" + "\n")
  errortest = 1

#assigning memory to variables
for i in wordsfinal:
  if errortest == 1:
    break
  if i[0] == "var":
    memory[i[1]] = binaryconvert(memvariable)
    memvariable += 1

wordsfinal = [i for i in wordsfinal if i[0] != 'var']

for i in wordsfinal:
  if len(i) == 2 and i[0] == 'var':
    wordsfinal.remove(i)

#removing blank spaces
for i in range(len(wordsfinal)):
  while "" in wordsfinal[i]:
    wordsfinal[i].remove("")

#labels
listE = ["jmp", 'jlt', 'jgt', 'je']
for i in wordsfinal:
  if i[0][-1] == ":":
    labeldec[i[0]] = wordsfinal.index(i)
    #print(labeldec)

  if i[0] in listE:
    labelcall[i[1]] = wordsfinal.index(i)
    #print(labelcall)

for i in wordsfinal:
  if i[0][-1] == ":":
    labelname = wordsfinal[wordsfinal.index(i)].pop(0)
    #print("removed label name: ", labelname)

#adding opcodes for instructions and the mov instruction
opcodevar = 0
for i in wordsfinal:

  if i[0] == "mov":
    if i[2][0] == "$":
      if i[1] not in register:
        print("error in line", opcodevar + 1 + len(memory),
              ": Register not found.")
        f2.write("error in line " + str(opcodevar + 1 + len(memory)) +
                 ": Register not found." + "\n")
        errortest = 1
        break
      binarycode.append("00010")

      binarycode[opcodevar] = binarycode[opcodevar] + "0"  #unused bits
      binarycode[opcodevar] = binarycode[opcodevar] + register[i[1]]
      immvalue = binaryconvert(int(i[2][1::]))
      if len(immvalue) > 7:
        print("error in line", opcodevar + 1 + len(memory),
              ": Illegal immediate value.")
        f2.write("error in line" + str(opcodevar + 1 + len(memory)) +
                 ": Illegal immediate value.")
        errortest = 1
        break
      binarycode[opcodevar] = binarycode[opcodevar] + immvalue
    else:
      binarycode.append("00011")
      binarycode[opcodevar] = binarycode[opcodevar] + "00000"  #unused bits
      binarycode[opcodevar] = binarycode[opcodevar] + register[i[1]]
      binarycode[opcodevar] = binarycode[opcodevar] + register[i[2]]
  elif i[0] not in opcode:
    if i[0][-1] == ":":
      continue
    print("error in line", opcodevar + 1 + len(memory), ": Incorrect opcode.")
    f2.write("error in line " + str(opcodevar + 1 + len(memory)),
             ": Incorrect opcode.")
    errortest = 1
    break

  else:
    binarycode.append(opcode[i[0]])
  opcodevar += 1

#type-A
listA = ['add', 'sub', 'mul', 'xor', 'or', 'and']
listB = ['rs', 'ls']
listC = ['div', 'not', 'cmp']
listD = ['ld', 'st']

opcodevar = 0
for i in wordsfinal:
  if i[0][-1] == ":":
    continue
  if errortest == 1:
    break
  #A
  if i[0] in listA:
    if i[1] not in register or i[2] not in register or i[3] not in register:
      print("error in line", opcodevar + 1 + len(memory),
            ": Register not found.")
      f2.write("error in line " + str(opcodevar + 1 + len(memory)) +
               ": Register not found.")
      errortest = 1
      break
    binarycode[opcodevar] = binarycode[opcodevar] + "00"  #unused bits
    binarycode[opcodevar] = binarycode[opcodevar] + register[i[1]]
    binarycode[opcodevar] = binarycode[opcodevar] + register[i[2]]
    binarycode[opcodevar] = binarycode[opcodevar] + register[i[3]]

  #B
  if i[0] in listB:
    if i[1] not in register:
      print("error in line", opcodevar + 1 + len(memory),
            ": Register not found.")
      f2.write("error in line " + str(opcodevar + 1 + len(memory)) +
               ": Register not found.")
      errortest = 1
      break
    binarycode[opcodevar] = binarycode[opcodevar] + "0"  #unused bits
    binarycode[opcodevar] = binarycode[opcodevar] + register[i[1]]
    immvalue = binaryconvert(int(i[2][1::]))
    if len(immvalue) > 7:
      print("error in line", opcodevar + 1 + len(memory),
            ": Illegal immediate value.")
      f2.write("error in line" + str(opcodevar + 1 + len(memory)) +
               ": Illegal immediate value.")
      errortest = 1
      break
    binarycode[opcodevar] = binarycode[opcodevar] + immvalue

  #C
  if i[0] in listC:
    if i[1] not in register or i[2] not in register:
      print("error in line", opcodevar + 1 + len(memory),
            ": Register not found.")
      f2.write("error in line " + str(opcodevar + 1 + len(memory)) +
               ": Register not found.")
      errortest = 1
      break
    binarycode[opcodevar] = binarycode[opcodevar] + "00000"  #unused bits
    binarycode[opcodevar] = binarycode[opcodevar] + register[i[1]]
    binarycode[opcodevar] = binarycode[opcodevar] + register[i[2]]

  #D
  if i[0] in listD:
    if i[1] not in register:
      print("error in line", opcodevar + 1 + len(memory),
            ": Register not found.")
      f2.write("error in line " + str(opcodevar + 1 + len(memory)) +
               ": Register not found.")
      errortest = 1
      break
    if i[2] not in memory:
      print("error: Memory not found in line " +
            str(opcodevar + 1 + len(memory)))
      f2.write("error: Memory not found in line " +
               str(opcodevar + 1 + len(memory)))
      errortest = 1
      break
    binarycode[opcodevar] = binarycode[opcodevar] + "0"  #unused bits
    binarycode[opcodevar] = binarycode[opcodevar] + register[i[1]]
    binarycode[opcodevar] = binarycode[opcodevar] + memory[i[2]]

  #E
  if i[0] in listE:
    if (i[1] + ":") not in labeldec:
      print("error in line", opcodevar + 1 + len(memory),
            ": Use of undefined label.")
      f2.write("error in line " + str(opcodevar + 1 + len(memory)) +
               ": Use of undefined label.")
      errortest = 1
      break
    binarycode[opcodevar] = binarycode[opcodevar] + "0000"  #unused bits
    binarycode[opcodevar] = binarycode[opcodevar] + binaryconvert(
      labeldec[i[1] + ":"])

  #F
  if i[0] == "hlt":
    binarycode[opcodevar] = binarycode[opcodevar] + "00000000000"  #unused bits

  opcodevar += 1
'''for i in wordsfinal:
  print(i)'''

#halt errors
hlttest = 0
for i in wordsfinal:
  for j in i:
    if j == "hlt":
      hlttest = 1
      break
if hlttest == 0:
  print("error: Missing halt instruction.")
  f2.write("error: Missing halt instruction.")
  errortest = 1
elif hlttest == 1:
  if wordsfinal[-1] != ['hlt']:
    print("error: Halt not used as the last instruction.")
    f2.write("error: Halt not used as the last instruction.")
    errortest = 1

if errortest == 0:
  for i in binarycode:
    f2.write(i + "\n")

f2.close()
f.close()

#Type-A: add, sub, mul, xor, or, and   (3 register type)

#type-B: x mov(00010), rs, ls            (register and immediate type)

#type-C: x mov(00011), div, not, cmp     (2 register type)

#type-D: ld, st                   (reg and mem addr type)

#type-E: jmp, jlt, jgt, je             (mem addr type)

#type-F: halt                          (halt)

#type-special  mov(00010), mov(00011)

