.data

.text

    main:
        # Inicializacion de variables
        li $t0, 50
        li $t1, 100
        # Colocar los args de la funcion
        move $a0, $t0
        move $a1, $t1
        # Llamada a la funcion suma
        jal suma
        # Obtener el resultado
        move $t2, $v1
        # Imprimir el resultado
        li $v0, 1
        move $a0, $t2
        syscall

    # Exit
    li $v0, 10
    syscall

    suma:
        # Sumar los args
        add $v1, $a0, $a1
        # Regresar a la funcion main
        jr $ra