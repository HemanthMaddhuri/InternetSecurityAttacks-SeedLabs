section .text
  global _start
    _start:
      ; Store the argument string on stack
      mov edx, "h***"	 ; moving string "h***" to register edx
      shl edx, 24       ; shifting the bits left for 24 bits
      shr edx, 24       ; shifting the bits right for 24 bits
      push edx          ; Now the register edx has the value "h/0/0/0"
      push "/bas"
      push "/bin"
      push "/usr"
      mov  ebx, esp     ; Get the string address

      ; Construct the argument array argv[]
      push eax          ; argv[1] = 0 
      push ebx          ; argv[0] points "/bin//sh"
      mov edx,'"-al"'
      lea ecx, [edx+3]
      mov edx, '"ls"'
      lea ecx, [edx+10]
      mov edx, '-c'
      lea ecx, [edx+4]
      mov  ecx, esp     ; Get the address of argv[]
   
      ; For environment variable 
      xor  edx, edx     ; No env variables 

      ; Invoke execve()
      xor  eax, eax     ; eax = 0x00000000
      mov   al, 0x0b    ; eax = 0x0000000b
      int 0x80
