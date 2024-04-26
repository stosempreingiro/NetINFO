
def subnet_decimal(ip_user,info=None):
    list_info=ip_user.split("/")  #I split the user input in IP and Subnet
    ip=list_info[0].split(".") #IP
    sub=list_info[1] #SUBNET
    nzeros=32-int(sub)    #number of zeros for the binary subnet   
    sub_net_bin=""              #Empty variable that will contain the subnet in binary 
    for i in range (0,int(sub)):
        sub_net_bin+='1'
        if len(sub_net_bin)==8 or len(sub_net_bin)==17 or len(sub_net_bin)==26: #Condition that allows you to insert dots.
            sub_net_bin+='.'
    for i in range(0,nzeros):
        sub_net_bin+='0'
        if len(sub_net_bin)==8 or len(sub_net_bin)==17 or len(sub_net_bin)==26:
            sub_net_bin+='.'
    listina_binari=sub_net_bin.split(".")   #I create a list of 4 elements, each of which will be made up of 8 of the 32 bits of the subnet
    subnet_decimal=""       #creo subnet in decimale
    punto=0
    for numero in listina_binari: #Start creating a subnet in decimal
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
    gateway_bin=""       #IDKW start calculating the gateway and the net_addr (host_min) in binary
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
    gateway_decimal=""          #Start Calculating Gateway and Broadcast in decimal
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
    elif info=="all":
        return [subnet_decimal,host_min_decimal,broad_cast,(2**(32-int(sub))),(2**(32-int(sub)))-2]  #LIST:  subnet , net address , broadcast , Total IP , possible host device
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


class Output:
    def __init__(self,subnet,net_addr,broadcast,totalIP,n_device):
        self.subnet=subnet
        self.net_addr=net_addr
        self.broadcast=broadcast
        self.totalIP=totalIP
        self.n_device=n_device

