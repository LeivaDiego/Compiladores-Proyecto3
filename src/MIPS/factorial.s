# fun factorial(n) {
#   if (n <= 1) {
#     return 1;
#   } else {
#     return n * factorial(n - 1);
#   }
# }
# var numero = 5;
# var resultado = factorial(numero);
# print "El factorial de " + numero + " es: " + resultado; // 120


.data
    numero: .word 5     # Variable numero
    resultado: .word 0  # Variable resultado
    str0: .asciiz "El factorial de "
    str1: .asciiz " es: "

.text
    main:
        # Load numero into register
        lw $t0, numero

        # Load arguments for factorial function
        move $a0, $t0

        # Call factorial function
        jal factorial

        # Store result into resultado variable
        sw $v0, resultado

        # Print "El factorial de "
        la $a0, str0
        li $v0, 4
        syscall

        # Print numero
        lw $a0, numero
        li $v0, 1
        syscall

        # Print " es: "
        la $a0, str1
        li $v0, 4
        syscall

        # Print resultado
        lw $a0, resultado
        li $v0, 1
        syscall

        # Exit program
        li $v0, 10
        syscall
        

    factorial:
        # Reserve space in stack for return address and temp argument
        sub $sp, $sp, 8
        sw $a0, 0($sp)  # Save temp argument
        sw $ra, 4($sp)  # Save return address

        # Base case (first if statement)
        li $v0, 1       # Load 1 into return register
        
        # Check if n <= 1
        ble $a0, 1, return_factorial

        # Else
        # get the factorial of n - 1
        sub $a0, $a0, 1         # n - 1
        jal factorial           # factorial(n - 1)
        # Retrieve previous n
        lw $a0, 0($sp)          # Load temp argument
        # Multiply n * factorial(n - 1)
        mul $v0, $a0, $v0


        return_factorial:
            # Restore return address and temp argument
            lw $ra, 4($sp)
            # Clean stack
            add $sp, $sp, 8
            # Return to caller
            jr $ra