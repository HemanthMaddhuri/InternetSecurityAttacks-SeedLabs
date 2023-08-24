section .text
  global _start
    _start:
	BITS 32
	jmp short two
    one:
 	pop ebx
 	xor eax, eax
 	mov edx, 0x31323334
 	mov [ebx+7], al
 	mov edx, 0x35363738
 	mov [ebx+8], ebx 
 	mov edx, 0x31323334
 	mov [ebx+12], eax
 	lea ecx, [ebx+8] 
 	xor edx, edx
 	mov al,  0x0b
 	int 0x80
     two:
 	call one
 	db '/usr/bin/env'   ; the command string
	db 'aaa'       ; placeholder for argv[0]
	db 'bbb'       ; placeholder for argv[1]
	db 'cccc'
