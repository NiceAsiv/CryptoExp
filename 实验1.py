import random
#实验1-Fermat素性检测算法
#求最大公因数
def gcd(a,b):
    if a<b:
        a,b=b,a
    while b!=0:
        a,b=b,a%b
    return a

def check_fermat(n):
   #生成[2,n-2]之间一个随机数
    b=int(random.randrange(2,n-1))
    print("[!]生成的随机数为：",b)
    #判断是否互素
    if gcd(b,n)!=1:
        #print("n=",str(n),"不是素数")
        return False
    #判断是否满足费马小定理
    if pow(b,n-1,n)!=1:#pow(a,b,c)表示a的b次方对c取模
        #print("n=",str(n),"在该次检验中不是素数")
        return False
   # print("n=",str(n),"可能是素数")
    return True

#输入：待检测的数n，检测次数k
n=int(input("请输入待检测的数n："))
k=int(input("请输入检测次数k："))
#检测
if "__main__"==__name__:
    possible=(1-1/2**k)*100
    while(k>0):
        if check_fermat(n):
            k-=1
        else:
            break
    if(k==0):
        print("[!]最终结果n=",str(n),"可能是素数，n为素数的概率为",str(possible),"%")
    else:
        print("[!]最终结果:n=",str(n),"为合数")
    