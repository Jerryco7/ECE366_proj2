0x200820ff #addi $8, $0, 0x20ff
0x201320ff #addi $19, $0, 0x20ff
0x200900ff #addi $9, $0, 255

0xa1090000 #sb $9, 0($8)
0x2108ffff #addi $8, $8, -1

	  #loop_sb:
0xa1090000 #sb $9, 0($8)
0x2108ffff #addi $8, $8, -1
0x2129ffff #addi $9, $9, -1
0x1520fffc #bne $9, $0, loop_sb

0x200a0000 #addi $10, $0, 0 
0x200e0004 #addi $14, $0, 4

           #loop_lb:
0x81090000 #lb $9, 0($8)
0x200c0000 #addi $12, $0, 0
0x200d0008 #addi $13, $0, 8

           #loop_shift:
0x312b0001 #andi $11, $9, 1
0x11600001 #beq $11, $0, skip_one
0x218c0001 #addi $12, $12, 1

           #skip_one:
0x00094842 #srl $9, $9, 1
0x21adffff #addi $13, $13, -1
0x15a0fffa #bne $13, $0, loop_shift

0x118e0001 #beq $12, $14, skip_count
0x214a0001 #addi $10, $10, 1

           #skip_count:
0x21080001 #addi $8, $8, 1
0x1513fff3 #bne $8, $19, loop_lb
