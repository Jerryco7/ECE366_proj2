lui $8, 0xFA19
ori $8, $8, 0xE366
addi $17, $0, 0x2020
addi $18, $0, 1
addi $14, $0, 5
addi $19, $0, 100



big_loop:
add $9, $0, $18
loop:
hash $9, $8, $9
addi $14, $14, -1
bne $14, $0, loop
addi $14, $0, 5

add $16, $0, $9
srl $16, $16, 16
andi $9, $9, 0xFFFF
xor $15, $9, $16

add $16, $0, $15
srl $16, $16, 8
andi $15, $15, 0xFF
xor $15, $15, $16
sw $15, 0($17)
addi $17, $17, 4
addi $19, $19, -1
addi $18, $18, 1
bne $19, $0, big_loop


addi $14, $0, 0
addi $18, $0, 0
addi $19, $0, 100

addi $10, $0, 0x2000
addi $11, $0, 0x2004

back:
lw $20, -4($17)
sltu $18, $20, $14
bne $18, $0, next

add $21, $0, $17
sw $21, 0($10)
sw $20, 0($11)
add $14, $0, $20

next:
addi $17, $17, -4
addi $19, $19, -1
bne $19, $0, back



addi $19, $0, 100
addi $17, $0, 0x2020
addi $8, $0, 0
addi $10, $0, 0
addi $9, $0, 4
addi $13, $0, 0x1F
addi $15, $0, 0
addi $16, $0, 0x2008

next_C:
lw $11, 0($17)
add $14, $0, $11

check:
andi $12, $11, 0x1f
bne $12, $13, shift

addi $15, $15, 1
addi $10, $0, 0
addi $17, $17, 4
addi $8, $8, 1
bne $8, $19, next_C

shift:
srl $11, $11, 1
add $14, $0, $11
addi $10, $10, 1
bne $10, $9, check

addi $10, $0, 0
addi $17, $17, 4
addi $8, $8, 1
bne $8, $19, next_C

sw $15, 0($16)
