lui $8, 0xFA19      # initializes B
ori $8, $8, 0xE366
addi $17, $0, 0x2020    
addi $18, $0, 1	  # A (1-100)	
addi $14, $0, 5     # loop counter for finding A1-A5
addi $19, $0, 100   # For counter



big_loop:
add $9, $0, $18
loop:
multu $8, $9        # Set hi & lo based off product
mfhi $10            # Get lo
mflo $11            # Get hi
xor $9, $10, $11    # Get A_n from hi xor lo
addi $14, $14, -1   # decrement counter
bne $14, $0, loop
addi $14, $0, 5

add $16, $0, $9   
srl $16, $16, 16    # Getting A5[31:16]
andi $9, $9, 0xFFFF # Getting A5[0:15]
xor $15, $9, $16    # Getting C

add $16, $0, $15    # Reusing $16
srl $16, $16, 8     # Getting C[15:8]
andi $15, $15, 0xFF # Getting C[0:7]
xor $15, $15, $16   # Getting official C
sw $15, 0($17)      # Store C into 0x2020
addi $17, $17, 4    # Move to next address
addi $19, $19, -1
addi $18, $18, 1
bne $19, $0, big_loop


addi $14, $0, 0
addi $18, $0, 0  # Used for 1 or 0 to find greatest
addi $19, $0 100

addi $10, $0, 0x2000  
addi $11, $0, 0x2004

back:
lw $20, -4($17)
sltu $18, $20, $14  
bne $18, $0, next

add $21, $0, $17  # memory address of largest
sw $21, 0($10)
sw $20, 0($11)
add $14, $0, $20  

next:
addi $17, $17, -4
addi $19, $19, -1
bne $19, $0, back



addi $19, $0 100  #reuse to iterate through all C values
addi $17, $0, 0x2020  #start from first C
addi $8, $0, 0  # to loop through 100 times
addi $10, $0, 0  # to loop through 4 times
addi $9, $0, 4  # 4 srl to check for 11111
addi $13, $0, 0x1F # to compare
addi $15 $0, 0 # match tracker
addi $16, $0, 0x2008

next_C:
lw $11, 0($17)  # get C
add $14, $0 $11  # clone C for comparison

check:
andi $12, $11, 0x1F  
bne $12, $13, shift  #if we did not find a match shift the reg

addi $15, $15, 1  # increment counter 
addi $10, $0, 0   # reset shift iterator
addi $17, $17, 4  # move to next mem address
addi $8, $8, 1    # increment C iterator
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
