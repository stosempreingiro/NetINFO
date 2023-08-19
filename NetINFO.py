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
    list_info=ip_user.split("/")  #divido l'input dell'utente in indirizzo IP e subnet
    ip=list_info[0].split(".")
    sub=list_info[1]
    x=32-int(sub)
    sub_net_bin=""              #Creo la subnet in binario
    n=0
    for i in range (0,int(sub)):
        sub_net_bin+='1'
        if len(sub_net_bin)==8 or len(sub_net_bin)==17 or len(sub_net_bin)==26: #condizione che permettere di inserire i punti.
            sub_net_bin+='.'
    for i in range(0,x):
        sub_net_bin+='0'
        if len(sub_net_bin)==8 or len(sub_net_bin)==17 or len(sub_net_bin)==26:
            sub_net_bin+='.'
    listina_binari=sub_net_bin.split(".")   #creo una lista con i singoli valori della subnet in binario
    subnet_decimal=""       #creo subnet in decimale
    punto=0
    for numero in listina_binari:
        if punto!=3:
            numero=int(numero,2)
            numero=str(numero)
            subnet_decimal+=(numero+'.')
            punto+=1
        elif punto==3:
            numero=int(numero,2)
            numero=str(numero)
            subnet_decimal+=numero
    ip_bin=""               #riscrivo l'indirizzo IP in binario.
    for val in ip:
        bin_val=bin(int(val))[2:].zfill(8)
        ip_bin+=bin_val
        if len(ip_bin)==8 or len(ip_bin)==17 or len(ip_bin)==26:
            ip_bin+='.'
    gateway_bin=""       #Calcolo e scrivo il gateway e l'host min in binario
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
    gateway_decimal=""      #calcolo e scrivo il gateway e il broadcast in decimale
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

    host_min_decimal=""     #scrivo l'host min in decimale
    i=0
    for val in list_host_min:
        i+=1
        val_dec=int(val,2)
        host_min_decimal+=str(val_dec)
        if i!=4:
            host_min_decimal+='.'
    if info=="solo_sub":        #valori di ritorno
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
    
def check_input_ip(ip_user):        #funzione che verifica l'input dell'utente
    try:
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
        z=input("(Invio per proseguire, CTRL+C per interrompere)")
        if z=="":
            os.system(clear)
except KeyboardInterrupt:
    print("\nByebye\n")