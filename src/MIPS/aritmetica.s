# var num = 20;
# var resultado = (num * 2) + (5 - 3) / 2;
# print resultado; // output: 21
.data
    num: .word 20           # num = 20
    resultado: .word 0      # resultado = 0

.text
    main:
        lw $s0, num     # Load the value of num into $s0
        
        # TAC code
        # Load all constants
        li $t0, 2
        li $t1, 5
        li $t2, 3

        # Start doing the operations
        mult $s0, $t0   # (num * 2)
        mflo $t3        # t3 = lo

        sub $t4, $t1, $t2   # (5 - 3)

        add $t5, $t3, $t4   # (num * 2) + (5 - 3)

        div $t5, $t0    # ((num * 2) + (5 - 3)) / 2
        mflo $s1        # t6 = lo

        # Store the result in resultado
        sw $s1, resultado

        # Print the result
        li $v0, 1       # syscall 1 is print_int
        lw $a0, resultado   # load the number to print
        syscall         # print the number

        # Exit
        li $v0, 10      # syscall 10 is exit
        syscall         # exit the program