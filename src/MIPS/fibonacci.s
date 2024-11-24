.data
    numero: .word 10
    resultado: .word 0
    str0: .asciiz "El termino "
    str1: .asciiz " de la serie de Fibonacci es: "

.text
    main:
        # Load the number to a register
        lw $t0, numero

        # Load the arguments for fibonacci
        move $a0, $t0

        # Call the fibonacci function
        jal fibonacci

        # Store the result into resultado variable
        sw $v0, resultado

        # Print "El termino "
        li $v0, 4
        la $a0, str0
        syscall

        # Print numero
        li $v0, 1
        lw $a0, numero
        syscall

        # Print " de la serie de Fibonacci es: "
        li $v0, 4
        la $a0, str1
        syscall

        # Print resultado
        li $v0, 1
        lw $a0, resultado
        syscall

        # Exit program
        li $v0, 10
        syscall

    
    fibonacci:
        # Reserve space in stack for return address and temp argument
        sub $sp, $sp, 8
        sw $ra, 4($sp)      # Save return address

        # Base case
        # if n <= 1
        move $v0, $a0   # Move n to return value

        # Check if n <= 1
        ble $a0, 1, return_fibonacci    # Return n if n <= 1

        # Else
        # Get fibonacci(n-1)
        sw $a0, 0($sp)  # Save n to stack
        sub $a0, $a0, 1 # n-1
        jal fibonacci   # Call fibonacci(n-1)
        # Get return value
        lw $a0, 0($sp)  # Get orignal n from stack
        sw $v0, 0($sp)  # Save fibonacci(n-1) to stack

        # Get fibonacci(n-2)
        sub $a0, $a0, 2 # n-2
        jal fibonacci   # Call fibonacci(n-2)
        # Get return value
        lw $v1, 0($sp)  # Get fibonacci(n-1) from stack

        # Add fibonacci(n-1) + fibonacci(n-2)
        add $v0, $v0, $v1


        return_fibonacci:
            # Restore return address
            lw $ra, 4($sp)
            # Clean stack pointer
            add $sp, $sp, 8
            # Return to caller
            jr $ra


