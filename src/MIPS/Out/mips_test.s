.data
	newLine: .asciiz "\n"
	str0: .asciiz "El factorial de "
	str1: .asciiz " es: "

.text
	main:

	# Exit the program
	li $v0, 10
	syscall