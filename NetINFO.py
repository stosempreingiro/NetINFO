import os
import platform
import time

#check del sistema operativo per usare il comando 'clear'. Se hai qualche problema su Windows prova a commentare la riga 143
so=platform.system()
if so=="Windows":
    clear="cls"
else:
    clear="clear"

def subnet_decimal(ip_user,info=None):
    list_info=ip_user.split("/")  #I split the user input in IP and Subnet
    ip=list_info[0].split(".")
    sub=list_info[1]
    x=32-int(sub)     #number of zeros for the binary subnet
    sub_net_bin=""              #Empty variable that will contain the subnet in binary 
    n=0
    for i in range (0,int(sub)):
        sub_net_bin+='1'
        if len(sub_net_bin)==8 or len(sub_net_bin)==17 or len(sub_net_bin)==26: #Condition that allows you to insert dots.
            sub_net_bin+='.'
    for i in range(0,x):
        sub_net_bin+='0'
        if len(sub_net_bin)==8 or len(sub_net_bin)==17 or len(sub_net_bin)==26:
            sub_net_bin+='.'
    listina_binari=sub_net_bin.split(".")   #I create a list of 4 elements, each of which will be made up of 8 of the 32 bits of the subnet
    subnet_decimal=""   
    punto=0
    for numero in listina_binari:   #Start creating a subnet in decimal
        if punto!=3:
            numero=int(numero,2)
            numero=str(numero)
            subnet_decimal+=(numero+'.')
            punto+=1
        elif punto==3:
            numero=int(numero,2)
            numero=str(numero)
            subnet_decimal+=numero
    ip_bin=""               #Start writing IP in binary
    for val in ip:
        bin_val=bin(int(val))[2:].zfill(8)
        ip_bin+=bin_val
        if len(ip_bin)==8 or len(ip_bin)==17 or len(ip_bin)==26:
            ip_bin+='.'
    gateway_bin=""       #start calculating the gateway and the net_addr (host_min) in binary
    host_min=""
    for i in range(0,len(sub_net_bin)):
        if sub_net_bin[i]=='.':
            gateway_bin+='.'
            host_min+='.'
            continue
        elif sub_net_bin[i]=='0':
            gateway_bin+='1'
            host_min+='0'
        else:
            gateway_bin+=ip_bin[i]
            host_min+=ip_bin[i]
    list_gateway_bin=gateway_bin.split(".")
    list_host_min=host_min.split(".")
    gateway_decimal=""      #Start Calculating Gateway and Broadcast in decimal
    broad_cast=""
    i=0
    for val in list_gateway_bin:
        i+=1
        val_dec=int(val,2)
        broad_cast+=str(val_dec)
        if i==4:
            val_dec-=1
        gateway_decimal+=str(val_dec)
        if i!=4:
            gateway_decimal+='.'
            broad_cast+='.'

    host_min_decimal=""     #Calculating Net Addr in decimal
    i=0
    for val in list_host_min:
        i+=1
        val_dec=int(val,2)
        host_min_decimal+=str(val_dec)
        if i!=4:
            host_min_decimal+='.'

     #Manage the return value of the function
    if info=="solo_sub":       
        return subnet_decimal
    elif info=="tutto":
        return f"-SUBNET: {subnet_decimal}\n-HOST MIN/NETADDRESS: {host_min_decimal}\n-BROADCAST/HOST MAX: {broad_cast}\n-Possible GATEWAY: {gateway_decimal}\n-INDIRIZZI IP TOTALI nella RETE: {2**(32-int(sub))}\n-DEVICE CHE POSSONO ESSERE CONNESSI: {(2**(32-int(sub)))-2}"
    elif info=="gateway_subnet":
        only_ip=""
        for carattere in ip_user:
            if carattere=="/":
                break
            else:
                only_ip+=carattere
        return f"{only_ip} {subnet_decimal}"     
    
def check_input_ip(ip_user):        #Verify user input
    try:
        ip_user=ip_user.strip()
        punti=0
        val=True
        for char in ip_user:
            if char not in "1234567890./":
                val=False
                return val
            if char == '.' or char=='/':
                punti+=1
        if punti!=4 or len(ip_user)>18:
            val=False
            return val
        lista_val_ip_user=ip_user.split("/")
        slash=lista_val_ip_user[1]
        if int(slash)>=32 or int(slash)==0:
            val=False
            return val
        lista_val_ip=lista_val_ip_user[0].split(".")
        for valore in lista_val_ip:
            if valore=='.':
                pass
            elif int(valore) > 255:
                val=False
                return val
    except ValueError:
        val=False
    return val

banner="""
 _   _      _     ___ _   _ _____ ___  
| \ | | ___| |_  |_ _| \ | |  ___/ _ \ 
|  \| |/ _ \ __|  | ||  \| | |_ | | | |
| |\  |  __/ |_   | || |\  |  _|| |_| |
|_| \_|\___|\__| |___|_| \_|_|   \___/ 
                                     
~By stosempreingiro
-Interrompi con CTRL+C
"""

try:
    while True:
        print(banner)
        ip_user=input("Inserisci IP e Subnet (in C.I.D.R.): ")
        check=check_input_ip(ip_user)
        if not check:
            print("[!] Errore: indirizzo IP non valido.\n")
            time.sleep(1.5)
            os.system(clear)
            continue
        subnet_gateway_out=subnet_decimal(ip_user,info="tutto")
        print(f"\n{subnet_gateway_out}\n")
        to_do=input("(Invio per proseguire, CTRL+C per interrompere)")
        if to_do=="":
            os.system(clear)
except KeyboardInterrupt:
    print("\nByebye\n")
