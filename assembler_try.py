opcode={"add":'00000', "sub":'00001', "mov":'00010', "mov":'00011',
         "ld": '00100', "st":'00101', 'mul':'00110', 'div':'00111',
            'rs':'01000', 'ls':'01001', 'xor':'01010', 'or':'01011',
             'and':'01100', 'not':'01101', 'cmp':'01110', 'jmp':'01111',
              'jlt':'11100', 'jgt':'11101', 'je':'11111', 'hlt':'11010' }

register={"R0":'000', "R1":'001', "R2":'010', "R3":'011',
           "R4":'100', "R5":'101', "R6":'110', "FLAGS":'111'}

memory={}
memvariable=1

def binaryconvert(number):         #for imm values
   bin=""
   if number==0:
      return "0000000"
   while number>0:
      bin=str(number%2)+bin
      number=number//2
   while (len(bin)!=7):
      bin="0"+bin
   return bin
      



wordsfinal=[]
binarycode=[]

#reading text from input file
f=open("input.txt","r")
words=f.read()
wordslist=words.split("\n")

for i in wordslist:
    temp=i.split(" ")
    wordsfinal.append(temp)



#assigning memory to variables
for i in wordsfinal:
   if i[0]=="var":
      memory[i[1]]=binaryconvert(memvariable)
      memvariable+=1
   
wordsfinal=[i for i in wordsfinal if i[0]!='var']

for i in wordsfinal:
   if len(i)==2 and i[0]=='var':
      wordsfinal.remove(i)      




for i in wordsfinal:
    print(i)







#adding opcodes for instructions and the mov instruction
for i in wordsfinal:
   
   if i[0]=="mov":
      if i[2][0]=="$":
         binarycode.append("00010")
         binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+"0" #unused bits
         binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+register[i[1]]
         binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+binaryconvert(int(i[2][1::]))
      else:
         binarycode.append("00011")
         binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+"00000" #unused bits
         binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+register[i[1]]
         binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+register[i[2]]
   else:
      binarycode.append(opcode[i[0]])



#type-A
listA=['add', 'sub', 'mul', 'xor', 'or', 'and']
listB=['rs', 'ls']
listC=['div','not','cmp']
listD=['ld', 'st']
listE=["jmp",'jlt','jgt','je']





for i in wordsfinal:
   #A
   if i[0] in listA:
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+"00" #unused bits
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+register[i[1]]
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+register[i[2]]
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+register[i[3]]

   #B
   if i[0] in listB:
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+"0" #unused bits
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+register[i[1]]
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+binaryconvert(int(i[2][1::]))

   #C
   if i[0] in listC:
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+"00000" #unused bits
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+register[i[1]]
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+register[i[2]]

   #D
   if i[0] in listD:
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+"0" #unused bits
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+register[i[1]]
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+memory[i[2]]
   
   #E
   if i[0] in listE:
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+"0000" #unused bits
      binarycode[wordsfinal.index(i)]=binarycode[wordsfinal.index(i)]+memory[i[1]]
   
   #F
   if i[0]=="hlt":
      binarycode[-1]=binarycode[-1]+"00000000000"
      










#type-F



for i in binarycode:
   print(i)


#Type-A: add, sub, mul, xor, or, and   (3 register type)

#type-B: x mov(00010), rs, ls            (register and immediate type)

#type-C: x mov(00011), div, not, cmp     (2 register type)

#type-D: ld, st                   (reg and mem addr type)

#type-E: jmp, jlt, jgt, je             (mem addr type)

#type-F: halt                          (halt)

#type-special  mov(00010), mov(00011)



