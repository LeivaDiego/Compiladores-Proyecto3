# var num = 25;
# // Output 25 es impar
# if (num % 2 == 0){
#     print num + " es par";
# }
# else{
#     print num + " es impar";
# }

.data
    num: .word 25               # num = 25
    str0: .asciiz " es par\n"   # msg1 = " es par\n"
    str1: .asciiz " es impar\n" # msg2 = " es impar\n"

.text
    main:
    # Load the value of num into $t0
        lw $t0, num           # $t0 = num

        # TAC code
        li $t1, 2             # Load the constant 2
        div $t0, $t1          # num % 2
        mfhi $t1              # $t1 = hi -> remainder

        # Do the comparison (equal to 0)
        beq $t1, $zero, L_if_true   # if (num % 2 == 0) goto true
        # else
        # Print the number
        li $v0, 1             # syscall 1 is print_int
        move $a0, $t0         # load the number to print
        syscall               # print the number

        # Print the message " es impar"
        li $v0, 4             # syscall 4 is print_str
        la $a0, str1         # load the string to print
        syscall              # print the string

        j exit               # jump to exit

        L_if_true:
            # print the number
            li $v0, 1             # syscall 1 is print_int
            move $a0, $t0         # load the number to print
            syscall               # print the number

            # Print the message " es par"
            li $v0, 4             # syscall 4 is print_str
            la $a0, str0         # load the string to print
            syscall              # print the string

            j exit               # jump to exit

        exit:
            # Exit
            li $v0, 10            # syscall 10 is exit
            syscall               # exit the program