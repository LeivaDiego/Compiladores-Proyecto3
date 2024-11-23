# fun suma(a, b) {
#   return a + b;
# }
# var a = 3;
# var b = 4;
# var result = suma(a, b);
# print result; // Output: 7

.data
    a_var: .word 3          # Variable a
    b_var: .word 4          # Variable b
    result_var: .word 0     # Variable result

.text
    main:
        # Load a and b into registers
        lw $t0, a_var
        lw $t1, b_var

        # Reserve space for arguments
        sub $sp, $sp, 8

        # Load arguments
        move $a0, $t0         # load a into $a0
        move $a1, $t1         # load b into $a1
        
        # Call suma function
        jal suma

        # Load result into save register
        move $s0, $v0

        # Print result
        li $v0, 1           # syscall for print integer
        move $a0, $s0       # argument for print integer
        syscall

        # If we want to preserve the result, 
        # we can store it in a variable
        sw $s0, result_var

        # Exit
        li $v0, 10          # syscall for exit
        syscall

    suma:
        # Add the arguments
        add $v0, $a0, $a1

        # Return
        jr $ra