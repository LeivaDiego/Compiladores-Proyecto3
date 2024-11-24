# print "El factorial de " + numero + " es: " + resultado;
.data
    str1: .asciiz "El factorial de "
    str2: .asciiz " es: "
    str_output: .space 64      # Space for the output string
    number: .word 5            # Number to calculate the factorial
    result: .word 120          # Result of the factorial
    
.text
    main:
        # Copy str1 to result
        la $t0, str1                # load the base address of str1 into $t0
        la $t1, result              # load the base address of result into $t1

    copy_str1:
        lb $t2, 0($t0)              # load a byte from str1
        sb $t2, 0($t1)              # store the byte in result
        beq $t2, $zero, copy_str2   # if we found the end, continue with str2
        addi $t0, $t0, 1            # advance to the next byte in str1
        addi $t1, $t1, 1            # advance to the next byte in result
        j copy_str1

    # Copy str2 to result
    copy_str2:
        la $t0, str2                # load the base address of str2 into $t0

    copy_loop2:
        lb $t2, 0($t0)              # load a byte from str2
        sb $t2, 0($t1)              # store the byte in result
        beq $t2, $zero, end         # if we found the end, finish
        addi $t0, $t0, 1            # else, advance to the next byte in str2
        addi $t1, $t1, 1            # advance to the next byte in result
        j copy_loop2                # repeat the loop

    # Print the result
    end:
        li $v0, 4           # syscall 4 is print_str
        la $a0, result      # load the address of the string to print
        syscall             # print the string


        # Exit
        li $v0, 10          # syscall 10 is exit
        syscall

# 43 lines of code and a 5 labels in total (including the main label)
# Complex logic with 2 loops and 2 branches