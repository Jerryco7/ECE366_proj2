addi $8, $0, 0x20ff
addi $19, $0, 0x20ff
addi $9, $0, 255

sb $9, 0($8)
addi $8, $8, -1

loop_sb:
sb $9, 0($8)
addi $8, $8, -1
addi $9, $9, -1
bne $9, $0, loop_sb

addi $10, $0, 0
addi $14, $0, 4

loop_lb:
lb $9, 0($8)
addi $12, $0, 0
addi $13, $0, 8

loop_shift:
andi $11, $9, 1
beq $11, $0, skip_one
addi $12, $12, 1

skip_one:
srl $9, $9, 1
addi $13, $13, -1
bne $13, $0, loop_shift

beq $12, $14, skip_count
addi $10, $10, 1

skip_count:
addi $8, $8, 1
bne $8, $19, loop_lb