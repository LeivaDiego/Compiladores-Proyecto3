# for (var i = 1; i <= 5; i = i + 1) {
#   if (i % 2 == 0) {
#     print i + " es par";
#   } else {
#     print i + " es impar";
#   }
# }

.data
    str0: .asciiz " es par"
    str1: .asciiz " es impar"
    newline: .asciiz "\n"

.text
    main:
        # Load i and initialize it to 1
        li $t0, 1               # Load 1 to $t0
        li $t1, 2               # Load 2 to $t1

        # Call the for loop
        jal for_loop

        # Exit the program
        li $v0, 10
        syscall

    for_loop:
        # Check if i <= 5
        bgt $t0, 5, end_for

        # Check if i % 2 == 0
        li $t2, 2               # Load 2 to $t2
        div $t0, $t2            # Divide i by 2
        mfhi $t3                # Get the remainder

        # If i % 2 == 0
        beq $t3, $zero, is_even

        # Else
        j is_odd


        is_even:
            # Print i
            li $v0, 1           # syscall 1 = print_int
            move $a0, $t0       # move the value of $t0 into $a0
            syscall             # print the value of $t0

            # Print " es par"
            li $v0, 4           # syscall 4 = print_str
            la $a0, str0        # load the address of the string into $a0
            syscall             # print " es par"

            # Print a new line
            li $v0, 4           # syscall 4 = print_str
            la $a0, newline     # load the address of the string into $a0
            syscall             # print a new line

            j increment

        is_odd:
            # Print i
            li $v0, 1           # syscall 1 = print_int
            move $a0, $t0       # move the value of $t0 into $a0
            syscall             # print the value of $t0

            # Print " es impar"
            li $v0, 4           # syscall 4 = print_str
            la $a0, str1        # load the address of the string into $a0
            syscall             # print " es impar"

            # Print a new line
            li $v0, 4           # syscall 4 = print_str
            la $a0, newline     # load the address of the string into $a0
            syscall             # print a new line

            j increment

        increment:
            # Add 1 to i
            addi $t0, $t0, 1    # $t0 = $t0 + 1

            # Go back to the beginning of the loop
            j for_loop

        end_for:
            jr $ra              # Return to the main function