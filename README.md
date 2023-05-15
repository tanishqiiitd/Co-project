# Co-project
ASSEMBLER


Project by: 
            Tanishq Dass(2022533)
            Raima Aggarwal(2022393)
            Nikita Bhatia(2022323)
            Rohan Devgon(2022414)
                         
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

WORKFLOW:

1) The assembler starts by initializing the following:
* opcode dictionary(stores all opcodes)
* register dictionary(stores all registers)
* memory dictionary
* label dictionary
* instructions list

2) the assembler first stores all the variables in the memory.

3) It stores all the labels and deletes them from the instructions so that only the instruction part is left.

3) It then adds opcodes to all the instructions.

4) Next, it adds all the remaining parts of the instructions like unused bits, register code, label address, memory address and immediate value.

5) finally it prints all the binary code generated in the output file.

6) If any of the errors are triggered then only the error is printed in the file.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ERROR REPORTING:

The assembler can find the following types of errors:
a) Typos in instruction name or register name

b) Use of undefined variables

c) Use of undefined labels

d) Illegal use of FLAGS register

e) Illegal Immediate values (more than 7 bits)

f) Misuse of labels as variables or vice-versa

g) Variables not declared at the beginning

h) Missing hlt instruction

i) hlt not being used as the last instruction
