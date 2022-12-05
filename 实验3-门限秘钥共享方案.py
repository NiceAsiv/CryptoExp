#基于中国剩余定理的(t,n)门限秘钥共享方案

#挑选五个素数，满足严格递增
import random
import gmpy2

def is_coprime(list,bignum):
    for i in list:
        if gmpy2.gcd(i,bignum)!=1:
            return False
    return True
def find_d(n,t):
    d=[]#初始化d
    #向下取整
    minlen=int(500/t)
    maxlen=int(500/(t-1))
    while len(d)<n:
        temp=random.randint(pow(10,minlen),pow(10,maxlen))
        if is_coprime(d,temp):
            d.append(temp)
    d.sort()
    return d#返回一个递增的素数列表

def generate_key(message,n,t):
    while True:
        d=find_d(n,t)
        M=1
        N=1
        for i in range(t):
            N*=d[i]
        for i in range(len(d)-t+1,len(d)):
            M*=d[i]
        if M<message and message<N:
            break
    print("[!] Find d is:")
    for i in d:
        print(i)
    print("--------------------")
    print("N is:",N)
    print("M is:",M)
    print("--------------------")
    return M,N,d

def encrypt(message,d):
    k=[]
    for i in d:
        k.append(((message%i),i))
    print("k is:")
    for i,j in k:
        print(i) 
    print("--------------------")
    return k

def chinese_remainder(data):
    #判断是否互质
    for i in range(len(data)):
        for j in range(i+1,len(data)):
            if gmpy2.gcd(data[i][1],data[j][1])!=1:
                return -1,-1
    #计算n的乘积
    N=1
    for a,m in data:
        N*=m
    #计算Ni
    Ni=[]
    for a,m in data:
        Ni.append(N//m)
    #计算Ni的逆元
    Ni_inv=[]
    for i in range(len(Ni)):
        Ni_inv.append(gmpy2.invert(Ni[i],data[i][1]))
    #计算x
    x=0
    for i in range(len(Ni)):
        x+=data[i][0]*Ni[i]*Ni_inv[i]
    x=x%N
    return x

def decrypt(k,t):
    #任选t个k中的元素
    key_x=random.sample(k,t)
    x=chinese_remainder(key_x)
    # print("the decrypted message is:")
    # print(x)
    key_y=random.sample(k,t-1)
    y=chinese_remainder(key_y)
    return x,y

if __name__ == '__main__':
    message=34513712707371090043400509009985458207561435293144665050156734850970676055150464106635392035854544862922520495601217956585479796115422265889272312112460676286676002639176428018428110501603858423653391913799566813168343496159580747338826480697660522927181825310390154470363345038219192650075737129895819591216748784152267758174110791876279446873375543750375483617833468974263170064305100280485303368221268987883665789183494148190239289344532645805573919693262044556121484486211305720303265273494061665
    print("oringnal message is:")
    print(message)
    #输入n,t
    n,t=map(int,input("please input n,t:").split())
    # print(n)
    # print(t)
    M,N,d=generate_key(message,n,t)
    k=encrypt(message,d)
    x,y=decrypt(k,t)
    if(x==message and y!=message):
        print("message is successfully decrypted!")
    else:
        print("encryption failed!")