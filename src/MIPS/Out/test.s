.data
    prompt: .asciiz "Enter a number: "
    newline: .asciiz "\n"
    message: .asciiz "The number is: "

.text
    main:
        # Print prompt
        li $v0, 4
        la $a0, prompt
        syscall

        # Read integer
        li $v0, 5
        syscall

        # Move integer to $t0
        move $t0, $v0

        # Print newline
        li $v0, 4
        la $a0, newline
        syscall

        # Print integer
        li $v0, 4
        la $a0, message
        syscall
        li $v0, 1
        move $a0, $t0
        syscall


    # Exit
    li $v0, 10
    syscall