section .text
  global _start
    _start:
	BITS 32
	jmp short two
    one:
 	pop ebx
 	xor eax, eax
 	mov edx, 0x3131
 	mov [ebx+7], al
 	mov edx, 0x3232
 	mov [ebx+8], ebx 
 	mov [ebx+12], eax
 	lea ecx, [ebx+8] 
 	xor edx, edx
 	mov al,  0x0b
 	int 0x80
     two:
 	call one
 	db '/usr/bin/env'
 	db 'a'
 	db 'b' 
