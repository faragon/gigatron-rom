
#-----------------------------------------------------------------------
#
#       Loader-specific SYS extensions
#
#-----------------------------------------------------------------------

from asm import *

# Peek into the ROM's symbol table
videoY = symbol('videoY')
sysArgs = symbol('sysArgs0')
vPC = symbol('vPC')
vLR = symbol('vPC')

#-----------------------------------------------------------------------
# Extension SYS_LoaderNextByteIn_32
#-----------------------------------------------------------------------

# sysArgs[0:1] Current address
# sysArgs[2]   Checksum
# sysArgs[3]   Wait value (videoY)

label('SYS_LoaderNextByteIn_32')
ld([videoY])                    #15
xora([sysArgs+3])               #16
bne('.sysNbi')                  #17
ld([sysArgs+0], X)              #18
ld([sysArgs+1], Y)              #19
ld(IN)                          #20
st([Y,X])                       #21
adda([sysArgs+2])               #22
st([sysArgs+2])                 #23
ld([sysArgs+0])                 #24
adda(1)                         #25
st([sysArgs+0])                 #26
ld(hi('REENTER'),Y)             #27
jmp(Y,'REENTER')                #28
ld(-32/2)                       #29
# Restart instruction
label('.sysNbi')
ld([vPC])                       #19
suba(2)                         #20
st([vPC])                       #21
ld(-28/2)                       #22
ld(hi('REENTER'),Y)             #23
jmp(Y,'REENTER')                #24
nop()                           #25

#-----------------------------------------------------------------------
# Extension SYS_LoaderProcessInput_48
#-----------------------------------------------------------------------

# sysArgs[0:1] Source address
# sysArgs[2]   Checksum
# sysArgs[4]   Copy count
# sysArgs[5:6] Destination address

label('SYS_LoaderProcessInput_48')
ld([sysArgs+1],Y)               #15
ld([sysArgs+2])                 #16
bne('.sysPi0')                  #17
ld([sysArgs+0])                 #18
suba(65, X)                     #19 Point at first byte of buffer
ld([Y,X])                       #20 Command byte
st([Y,Xpp])                     #21 X++
xora(ord('L'))                  #22 This loader lumps everything under 'L'
bne('.sysPi1')                  #23
ld([Y,X]);                      C('Valid command')#24 Length byte
st([Y,Xpp])                     #25 X++
anda(63)                        #26 Bit 6:7 are garbage
st([sysArgs+4])                 #27 Copy count
ld([Y,X])                       #28 Low copy address
st([Y,Xpp])                     #29 X++
st([sysArgs+5])                 #30
ld([Y,X])                       #31 High copy address
st([Y,Xpp])                     #32 X++
st([sysArgs+6])                 #33
ld([sysArgs+4])                 #34
bne('.sysPi2')                  #35
# Execute code (don't care about checksum anymore)
ld([sysArgs+5]);                C('Execute')#36 Low run address
suba(2)                         #37
st([vPC])                       #38
st([vLR])                       #39
ld([sysArgs+6])                 #40 High run address
st([vPC+1])                     #41
st([vLR+1])                     #42
ld(hi('REENTER'),Y)             #43
jmp(Y,'REENTER')                #44
ld(-48/2)                       #45
# Invalid checksum
label('.sysPi0')
wait(25-19);                    C('Invalid checksum')#19 Reset checksum
# Unknown command
label('.sysPi1')
ld(ord('g'));                   C('Unknown command')#25 Reset checksum
st([sysArgs+2])                 #26
ld(hi('REENTER'),Y)             #27
jmp(Y,'REENTER')                #28
ld(-32/2)                       #29
# Loading data
label('.sysPi2')
ld([sysArgs+0]);                C('Loading data')#37 Continue checksum
suba(1, X)                      #38 Point at last byte
ld([Y,X])                       #39
st([sysArgs+2])                 #40
ld(hi('REENTER'),Y)             #41
jmp(Y,'REENTER')                #42
ld(-46/2)                       #43

#-----------------------------------------------------------------------
# Extension SYS_LoaderPayloadCopy_34
#-----------------------------------------------------------------------

# sysArgs[0:1] Source address
# sysArgs[4]   Copy count
# sysArgs[5:6] Destination address

label('SYS_LoaderPayloadCopy_34')
ld([sysArgs+4])                 #15 Copy count
beq('.sysCc0')                  #16
suba(1)                         #17
st([sysArgs+4])                 #18
ld([sysArgs+0],X)               #19 Current pointer
ld([sysArgs+1],Y)               #20
ld([Y,X])                       #21
ld([sysArgs+5],X)               #22 Target pointer
ld([sysArgs+6],Y)               #23
st([Y,X])                       #24
ld([sysArgs+5])                 #25 Increment target
adda(1)                         #26
st([sysArgs+5])                 #27
bra('.sysCc1')                  #28
label('.sysCc0')
ld(hi('REENTER'),Y)             #18,29
wait(30-19)                     #19
label('.sysCc1')
jmp(Y,'REENTER')                #30
ld(-34/2)                       #31

#-----------------------------------------------------------------------
#
#-----------------------------------------------------------------------

