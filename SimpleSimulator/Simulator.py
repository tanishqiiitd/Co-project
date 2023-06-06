
def binaryconvert(number):  
  bin = ""
  if number == 0:
    return "0000000"
  while number > 0:
    bin = str(number % 2) + bin
    number = number // 2
  while (len(bin) < 7):
    bin = "0" + bin
  return bin


def decimalconvert(binary):
    decimal = 0
    power = len(binary) - 1

    for digit in binary:
        decimal += int(digit) * (2 ** power)
        power -= 1

    return decimal






registerfile={"000":"0000000000000000",         #R0,R1,R2,R3,...,R7,FLAGS
          "001":"0000000000000000",
          "010":"0000000000000000",
          "011":"0000000000000000",
          "100":"0000000000000000",
          "101":"0000000000000000",
          "110":"0000000000000000",
          "111":"0000000000000000"}

opcode = {
  "add": '00000',
  "sub": '00001',
  "mov_imm": '00010',
  "mov_reg": '00011',
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

MEM={}



#program counter
pc=0


#input from file reading
'''
f=open("output.txt","r")
binarylist=f.readlines()
for i in range(len(binarylist)):
    binarylist[i]=binarylist[i].replace("\n","")
'''

#automated testing

test=[]
while True:
    try:
        testline=input()
        test.append(testline)
    except EOFError:
        break

binarylist=test



#manual testing
'''
binarylist=[]
inp=input()
while inp!="":
   binarylist.append(inp)
   inp=input()



'''




#print(binarylist)


systemmemory=[]
for i in range(128):
    systemmemory.append(format(0,'016b'))




for i in range(len(binarylist)):
    systemmemory[i]=binarylist[i]

#print(systemmemory)


#instruction handling

listA = ['00000', '00001', '00110', '01010', '01011', '01100']  # 00001-00-reg1-reg2-reg3
listB = ['01000', '01001', '00010']  # 01000-0-reg1-imm_value
listC = ['00011', '00111', '01101', '01110']  # 00011-00000-reg1-reg2
listD = ['00100', '00101'] # 00100-0-reg1-mem_addr
listE = ['01111', '11100', '11101', '11111'] # 01111-0000-mem_addr

l=1
while (l==1):
   
   condition="notdone"
   pc1="nope"


   if systemmemory[pc][:5] in listA:                    #------------------------------------------
      dest= systemmemory[pc][7:10] 
      reg1=systemmemory[pc][10:13]
      reg2=systemmemory[pc][13:16] 

      if systemmemory[pc][:5]=="00000":   #add
         
         result=format(int (registerfile[reg1], 2) + int (registerfile[reg2], 2), '016b')
         
         stat="normal"

      elif systemmemory[pc][:5]=="00001":   #sub
         if int (registerfile[reg1], 2) < int (registerfile[reg2], 2):
            stat="overflow"
         else:
            stat="normal"
         result=format(int (registerfile[reg1], 2) - int (registerfile[reg2], 2), '016b')
         
      
      elif systemmemory[pc][:5]=="00110":   #mul
         result=format(int (registerfile[reg1], 2) * int (registerfile[reg2], 2), '016b')
         stat="normal"
    
      elif systemmemory[pc][:5]=="01010":   #xor
         result=format(int (registerfile[reg1], 2) ^ int (registerfile[reg2], 2), '016b')
         stat="normal"
    
      elif systemmemory[pc][:5]=="01011":   #or
         result=format(int (registerfile[reg1], 2) | int (registerfile[reg2], 2), '016b')
         stat="normal"
    
      elif systemmemory[pc][:5]=="01100":   #and
         result=format(int (registerfile[reg1], 2) & int (registerfile[reg2], 2), '016b')
         stat="normal"

      if result> "1111111111111111":
         registerfile["111"]="0000000000001000"
         registerfile[dest]="0000000000000000"               #doubt
      
      elif stat=="overflow":
         registerfile["111"]="0000000000001000"
         registerfile[dest]="0000000000000000" 
     
      else:
         registerfile["111"]="0000000000000000"
         registerfile[dest]=result

   elif systemmemory[pc][:5] in listB:       #---------------------------------------------
      dest= systemmemory[pc][6:9] 
      imm= systemmemory[pc][9:]

      if systemmemory[pc][:5]=="00010":  #mov_imm
         registerfile[dest]="000000000"+imm
         registerfile['111']="0000000000000000"
    
      elif systemmemory[pc][:5]=="01000":  #right shift
         result=int(dest, 2) >> int(imm, 2)
         resultfinal=format(result, '016b')
         registerfile[dest]=resultfinal
         registerfile['111']="0000000000000000"

      elif systemmemory[pc][:5]=="01001":  #left shift
         result=int(dest, 2) << int(imm, 2)
         resultfinal=format(result, '016b')
         registerfile[dest]=resultfinal
         registerfile['111']="0000000000000000"

   elif systemmemory[pc][:5] in listC:     #---------------------------------------
      reg1=systemmemory[pc][10:13]
      reg2=systemmemory[pc][13:]
      

      if systemmemory[pc][:5]=="00011":   #mov reg
         registerfile[reg1]=registerfile[reg2]
         registerfile['111']="0000000000000000"
    
      elif systemmemory[pc][:5]=="00111":  # divide
         if registerfile[reg2]=="0000000000000000":
            registerfile["000"]= '0000000000000000'
            registerfile["001"]= '0000000000000000'
            registerfile['111'] = "0000000000001000"

         registerfile["000"]= format( int(registerfile[reg1], 2) // int(registerfile[reg2], 2), '016b')
         registerfile["001"]= format( int(registerfile[reg1], 2) % int(registerfile[reg2], 2), '016b')
         registerfile['111'] = '0000000000000000'
        
      elif systemmemory[pc][:5]=="01101":  # invert
         registerfile[reg1]= ''.join(["1" if i=="0" else "0" for i in registerfile[reg2]])
         registerfile["111"]="0000000000000000"
    
      elif systemmemory[pc][:5]=="01110":  # compare
         if registerfile[reg1] == registerfile[reg2]:
            registerfile["111"]="0000000000000001"
        
         elif registerfile[reg1] > registerfile[reg2]:
            registerfile["111"]="0000000000000010"
        
         elif registerfile[reg1] < registerfile[reg2]:
            registerfile["111"]="0000000000000100"


   elif systemmemory[pc][:5] in listD:          #--------------------------------------
      reg= systemmemory[pc][6:9]
      memaddr= systemmemory[pc][9:]
      
      memaddr=decimalconvert(memaddr)
      

      if systemmemory[pc][:5] == "00101":  # store
         systemmemory[memaddr]=registerfile[reg]
         
        
      elif systemmemory[pc][:5] == "00100":  # store
         registerfile[reg]=systemmemory[memaddr]

      registerfile["111"]="0000000000000000"

 
   elif systemmemory[pc][:5] in listE:     #-------------------------------------
      flag=registerfile['111']        #markkkkkk
      memaddr= systemmemory[pc][9:]
      memaddr=decimalconvert(memaddr)

      if systemmemory[pc][:5] == "01111":   #jmp
         pc=memaddr
         condition="done"
    
      elif systemmemory[pc][:5] == "11100":  #jlt
         if registerfile['111']=="0000000000000100":
            pc=memaddr
            conditon="done"

      elif systemmemory[pc][:5] == "11101":  #jgt
         if registerfile['111']=="0000000000000010":
            pc=memaddr
            print("memaddr is: ", pc)
            conditon="done"
    
      elif systemmemory[pc][:5] == "11111":  #je
         if registerfile['111']=="0000000000000001":
            pc=memaddr
            conditon="done"   #markkkkkkk
      registerfile['111']="0000000000000000"
         
      

   elif systemmemory[pc][:5]=='11010':        #------------------------------------------------------
         
         registerfile['111']="0000000000000000"
         
            




   print(binaryconvert(pc), end=" ")
   for i in registerfile:
      print(registerfile[i], end=" ")
   print()

   if systemmemory[pc][:5] in listE:     #-------------------------------------
      memaddr= systemmemory[pc][9:]
      memaddr=decimalconvert(memaddr)

      if systemmemory[pc][:5] == "01111":   #jmp
         pc=memaddr
         condition="done"
    
      elif systemmemory[pc][:5] == "11100":  #jlt
         if flag=="0000000000000100":
            pc=memaddr
            conditon="done"

      elif systemmemory[pc][:5] == "11101":  #jgt
         if flag=="0000000000000010":
            pc=memaddr
            print("memaddr is: ", pc, "instruction is: ", systemmemory[pc])
            
            conditon="done"
    
      elif systemmemory[pc][:5] == "11111":  #je
         if flag=="0000000000000001":
            pc=memaddr
            conditon="done"


   if systemmemory[pc][:5]=='11010':        #------------------------------------------------------
         break
   
   
   
   if condition=="notdone":
     pc+=1


for i in systemmemory:
   print(i)

