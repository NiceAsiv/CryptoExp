#ElGamal公钥密码算法
from Crypto.Util.number import *
import random
import gmpy2
def get_safe_prime(bits=1024):
    #生成随机大素数q
    while True:
        q=getPrime(bits)
        #生成p=2q+1
        p=2*q+1
        #判断p是否为素数
        if isPrime(p):
            return p,q
def get_generator(p,q):
    while True:
        g=random.randint(2,p-1)
        #因为p是一个强素数，因此只有1，2，q，p-1.因此只需要验证2和q即可
        if gmpy2.powmod(g,2,p)!=1 and gmpy2.powmod(g,q,p)!=1:
            return g

#秘钥生成
def keygen(nbits):
    #生成强素数p
    # In this context p is a strong prime if p-1 and p+1 have at least one large prime factor.
    # N should be a multiple of 128 and > 512.
    p,q=get_safe_prime(nbits)
    print("Find a safe prime p:",p)
    print(">------------------")
    #求原根
    g=get_generator(p,q)
    print("Find a generator g:",g)
    print(">------------------")
    x=random.randint(1,p-2)
    print("private key a is:",x)
    print(">---------------------")
    #计算y=g^x(mod p)
    y=gmpy2.powmod(g,x,p)
    print("public key g^a is:")
    print(y)
    print(">---------------------")
    return p,g,y,x

#加密
def encrypt(m,p,g,y): 
    #生成随机大素数k，满足1≤k≤p-2 k在每次加密中都不同
    k=random.randint(1,p-2)
    print("random k is:",k)
    print(">---------------------")
    #计算a=g^k(mod p)
    y1=gmpy2.powmod(g,k,p)
    #计算b=m*y^k(mod p)
    y2=m*gmpy2.powmod(y,k,p)
    return y1,y2

#解密
def decrypt(y1,y2,p,x):
    #计算y1^x(mod p)
    y=gmpy2.powmod(y1,x,p)
    #计算y^-1(mod p)
    y=gmpy2.invert(y,p)
    #计算m=y2*y(mod p)
    m=(y2*y)%p
    return m
if __name__ == '__main__':
    # m=int(input("input the message:"))
    m=9327260388393076415930260479153046010064951650867096323260782111903507989221223155043829435161867334962529353992935468294479465522637777146290777
    n=512
    p,g,y,x=keygen(n)
    y1,y2=encrypt(m,p,g,y)
    print("the encrypted message is:")
    print("C1:",y1)
    print("C2:",y2)
    print(">---------------------")
    decrypted_m=decrypt(y1,y2,p,x)
    if decrypted_m==m:
        print("The message is correct!")
    else:
        print("The message is wrong!")