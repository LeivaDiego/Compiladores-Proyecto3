# print "El factorial de " + numero + " es: " + resultado;
.data
    str0: .asciiz "El factorial de "
    str1: .asciiz " es: "
    numero: .word 5         # Number to calculate the factorial
    resultado: .word 120    # Result of the factorial

.text
    main:
        # Print "El factorial de "
        li $v0, 4               # syscall 4 is print_str
        la $a0, str0            # load address of string to print
        syscall                 # print the string

        # Print numero
        li $v0, 1               # syscall 1 is print_int
        lw $a0, numero          # load the number to print
        syscall                 # print the number

        # Print " es: "
        li $v0, 4               # syscall 4 is print_str
        la $a0, str1            # load address of string to print
        syscall                 # print the string

        # Print resultado
        li $v0, 1               # syscall 1 is print_int
        lw $a0, resultado       # load the number to print
        syscall                 # print the number

        # Exit
        li $v0, 10              # syscall 10 is exit
        syscall                 # exit the program

# 32 lines of code and 1 label in total (the main label)
# Simple logic with 4 print statements and 4 syscalls
# This is a much simpler logic than the concatenation of strings
# For the purposes of this project, the concatenation of strings is not necessary