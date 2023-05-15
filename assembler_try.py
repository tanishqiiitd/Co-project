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
  
