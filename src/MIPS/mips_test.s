.data
	var: .word 1
	true_msg: .asciiz "True\n"
	false_msg: .asciiz "False\n"
	test_String: .asciiz "This is a test string\n"

.text
	test:
		li $v0, 4
		la $a0, test_String
		syscall

.globl main
	main:

	lw $t0, var

	bne $t0, $zero, true_branch
	
	j false_branch

	false_branch:
		li $v0, 4
		la $a0, false_msg
		syscall
		j end

	true_branch:
		li $v0, 4
		la $a0, true_msg
		syscall
		j end
	
	# Exit the program
	end:
	li $v0, 10
	syscall