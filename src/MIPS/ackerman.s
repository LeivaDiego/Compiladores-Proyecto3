# fun ackerman(m, n){
#     if (m == 0){
#         return n + 1;
#     }
#     if (m > 0 and n == 0){
#         return ackerman(m - 1, 1);
#     }
#     if (m > 0 and n > 0){
#         return ackerman(m - 1, ackerman(m, n - 1));
#     }
# }
# var m = 2;
# var n = 2;
# var result = ackerman(m,n);
# print "ackerman(" + m + "," + n + ") = " + result; -> 7

.data
    m: .word 2
    n: .word 2
    result: .word 0
    str0: .asciiz "ackerman("
    str1: .asciiz ","
    str2: .asciiz ") = "

.text
    main:
        # Load m and n
        lw $s0, m
        lw $s1, n
        
        # Load the arguments for ackerman
        move $a0, $s0   # m
        move $a1, $s1   # n

        # Call ackerman
        jal ackerman

        # Store the result
        sw $v0, result

        # Print the result
        # Print "ackerman("
        li $v0, 4
        la $a0, str0
        syscall

        # Print m
        lw $a0, m
        li $v0, 1
        syscall

        # Print ","
        li $v0, 4
        la $a0, str1
        syscall

        # Print n
        lw $a0, n
        li $v0, 1
        syscall

        # Print ") = "
        li $v0, 4
        la $a0, str2
        syscall

        # Print result
        lw $a0, result
        li $v0, 1
        syscall

        # Exit
        li $v0, 10
        syscall



    ackerman:
        # Reserve space for the return address
        sub $sp, $sp, 4    # 3 words * 4 bytes = 12 bytes
        sw $ra, 0($sp)      # Save the return address

        # Base case: m == 0
        beq $a0, $zero, m_is_zero  # if m == 0, return n + 1

        # Else: we can assume m > 0
        # Check if n == 0
        # If n == 0, call ackerman(m - 1, 1)
        beq $a1, $zero, n_is_zero

        # Else: we can assumne n > 0
        # if n > 0, call ackerman(m - 1, ackerman(m, n - 1))
        j m_n_greater

        m_is_zero:
            # Return n + 1
            addi $v0, $a1, 1
            j ackerman_return

        n_is_zero:
            # Call ackerman(m - 1, 1)
            # Reserve space for the arguments in the stack
            sub $sp, $sp, 8
            sw $a0, 0($sp)  # Save m
            sw $a1, 4($sp)  # Save n
            
            # Adjust the arguments
            sub $a0, $a0, 1     # preload m - 1
            li $a1, 1           # preload n = 1

            # Call ackerman
            jal ackerman

            # Retrieve the arguments
            lw $a0, 0($sp)  # Restore m
            lw $a1, 4($sp)  # Restore n

            # Clean the stack
            add $sp, $sp, 8

            # Return
            j ackerman_return

        m_n_greater:
            # Reserve space for the arguments in the stack
            sub $sp, $sp, 8
            sw $a0, 0($sp)  # Save m
            sw $a1, 4($sp)  # Save n

            # First call ackerman(m, n - 1)
            # Adjust the arguments
            sub $a1, $a1, 1    # preload n - 1

            # Call ackerman
            jal ackerman

            # Retrieve and adjust the arguments
            # Second call ackerman(m - 1, ackerman(m, n - 1))
            move $a1, $v0   # preload ackerman(m, n - 1) as n
            sub $a0, $a0, 1    # preload m - 1

            # Call ackerman
            jal ackerman

            # Retrieve the arguments and clean the stack
            lw $a0, 0($sp)  # Restore m
            lw $a1, 4($sp)  # Restore n
            # Clean the stack
            add $sp, $sp, 8

            # Return
            j ackerman_return


        ackerman_return:
            # Restore the return address
            lw $ra, 0($sp)
            # Clean the stack
            add $sp, $sp, 4
            # Return to the caller
            jr $ra