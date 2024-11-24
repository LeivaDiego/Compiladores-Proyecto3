# var edad = 1;
# while (edad < 5) {
#   edad = edad + 1;
#   print "Edad: " + edad;
# }

.data
    edad: .word 1;
    str0: .asciiz "Edad: "
    newline: .asciiz "\n"

.text
    main:
        # Load the value of the variable edad into $t0
        lw $t0, edad    # $t0 = 1

        li $t1, 5      # $t1 = 5

        jal while       # go to while

        # Exit the program
        li $v0, 10      # syscall 10 = exit
        syscall


    # While Loop
    while:
        # Print "Edad: "
        li $v0, 4           # syscall 4 = print_str
        la $a0, str0         # load the address of the string into $a0
        syscall

        # Print the value of $t0
        li $v0, 1           # syscall 1 = print_int
        move $a0, $t0       # move the value of $t0 into $a0
        syscall             # print the value of $t0

        # Print a new line
        li $v0, 4           # syscall 4 = print_str
        la $a0, newline     # load the address of the string into $a0
        syscall             # print a new line

        # Add 1 to edad
        addi $t0, $t0, 1            # $t0 = $t0 + 1

        # Check if $t0 < $t1
        blt $t0, $t1, while

        # Else
        jr $ra              # return to the main function
