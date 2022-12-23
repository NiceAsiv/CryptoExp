import hashlib
import math
import random
from gmpy2 import *
# 无穷远点定义

INFINITY_POINT = (None, None)
# 椭圆曲线初始化
compress = 0
ecc_a, ecc_b, ecc_p, ecc_G, ecc_n, ecc_h, ecc_v = 0, 0, 0, (0, 0), 0, 0, 0
'''
        :Fp-256 参考来自文档page(90/93)   
        :素数p
        :8542D69E 4C044F18 E8B92435 BF6FF7DE 45728391 5C45517D 722EDB8B 08F1DFC3
        :系数a
        :787968B4 FA32C3FD 2417842E 73BBFEFF 2F3C848B 6831D7E0 EC65228B 3937E498
        :系数b
        :63E4C6D3 B23B0C84 9CF84241 484BFE48 F61D59A5 B16BA06E 6E12D1DA 27C5249A
        :基点G=(xG,yG)，其阶记为n。
        :坐标xG
        :421DEBD6 1B62EAB6 746434EB C3CC315E 32220B3B ADD50BDC 4C4E6C14 7FEDD43D
        :坐标yG
        :0680512B CBB42C07 D47349D2 153B70C4 E5D7FDFC BFA36EA1 A85841B9 E46E09A2
        :阶n
        :8542D69E 4C044F18 E8B92435 BF6FF7DD 29772063 0485628D 5AE74EE7 C32E79B7
'''


def get_curve(compress: int = 0):
    # 椭圆曲线参数
    ecc_a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    ecc_b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    # 域的规模q=p,p是大于3的素数
    ecc_p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    print("椭圆曲线方程为：y^2=x^3+ax+b")
    print("椭圆曲线参数：")
    print("a=", ecc_a)
    print("b=", ecc_b)
    print("p=", ecc_p)
    print("-----------------")
    # 基点G
    xG = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    yG = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    # 基点G=(xG,yG) 且G!=O
    ecc_G = (xG, yG)
    print("基点G=(xG,yG)")
    print("坐标xG=", xG)
    print("坐标yG=", yG)
    print("-----------------")
    # 阶n
    ecc_n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    # 选项余因子
    ecc_h = 1
    print("阶n=", ecc_n)
    print("余因子h=", ecc_h)
    # 椭圆曲线位数
    ecc_v = 256
    print()
    return ecc_a, ecc_b, ecc_p, ecc_G, ecc_n, ecc_h, ecc_v

# 数据类型转换


def intToBytes(x: int, k: int):
    '''
    输入:非负整数x,以及字符串的目标长度k(其中k满足2^(8k)>x))
    输出:长度为k的字节串M
    '''
    M = b''

    type(k)
    for _shift in range(k):
        # 将x的低8位取出,转化为字节,并与M拼接
        M = bytes([x >> 8*_shift & 0xFF])+M
    return M


def BytesToInt(M: bytes):
    '''
    输入:长度为k的字节串M
    输出:非负整数x
    '''
    x = 0
    for _shift in range(len(M)):
        # 将M的每个字节取出,转化为整数,并与x拼接
        x = x << 8 | M[_shift]
    return x


def BitsToBytes(s: str):
    '''
    输入:长度为m的比特串s
    输出:长度为m/8的字节串M
    '''
    length = len(s)
    k = math.ceil(length/8)
    # print("k=",k)
    s = s.zfill(k*8)
    # print("s=", s)
    M = b''
    for i in range(k):
        M = bytes([int(s[-(i*8+8):][:8], 2)])+M

        # M+=bytes([int(s[-(i*8+8):][:8], 2)])
        # 因为+=是将bytes([int(s[-(i*8+8):][:8], 2)])的值赋给M，而不是将M的值赋给bytes([int(s[-(i*8+8):][:8], 2)])
    # print("M=", M)
    return M


def BytesToBits(M: bytes):
    '''
    输入:长度为m的字节串M
    输出:长度为m*8的比特串s
    '''
    s = ""
    M = list(reversed(M))
    for i in range(len(M)):
        s = (bin(M[i])[2:]).zfill(8)+s
    return s


def DomainElementToBytes(a, l: int = 0):
    '''
    输入:域元素a
    输出:长度 l =⌈t/8⌉的字节串S，其中t =⌈log2q⌉
    '''
    q = ecc_p
    # q为素数
    if gmpy2.is_prime(q) and q > 2:
        assert a >= 0 and a <= q-1
        assert isinstance(a, int)
        l = math.ceil(math.log2(q)/8) if not l else l
        S = intToBytes(a, l)
        return S
    raise ValueError("a的取值范围为[0,q-1],q为奇素数")


def BytesToDomainElement(S: bytes):
    '''
    输入:长度 l =⌈t/8⌉的字节串S，其中t =⌈log2q⌉
    输出:F(q)中域元素a
    '''
    q = ecc_p
    # q为奇素数
    if gmpy2.is_prime(q) and q > 2:
        a = BytesToInt(S)
        assert a >= 0 and a <= q-1
        return a
    raise ValueError("a的取值范围为[0,q-1],q为奇素数")


def DomainElementToInt(a):
    '''
    输入:域元素a
    输出:整数x
    '''
    q = ecc_p
    # q为奇素数
    if gmpy2.is_prime(q) and q > 2:
        assert isinstance(a, int)
        return a
    raise ValueError("a不为整数")


def PointToBytes(P: tuple, compress: int = 0):
    '''
    输入:椭圆曲线上的点P(x,y)且P!=O
    输出:字节串S。若选用未压缩表示形式或混合表示形式，则输出字节串长度为2l+1；若选用压
缩表示形式，则输出字节串长度为l+1。(l =⌈(log2 q)/8⌉。)
    0-未压缩 1-压缩 2-混合表示
    '''
    q = ecc_p
    assert compress == 0 or compress == 1 or compress == 2
    l = math.ceil(math.log2(q)/8)
    xP, yP = P
    X1 = DomainElementToBytes(xP, l)
    # 这里默认compress为0
    if compress == 0:
        Y1 = DomainElementToBytes(yP, l)
        S = b'\x04'+X1+Y1
        return S
    raise ValueError


def BytesToPoint(S: bytes, compress: int = 0):
    '''
    输入:定义Fq上椭圆曲线的域元素a、b，字节串S
    输出:椭圆曲线上的点P(x,y)且P!=O
    '''
    q = ecc_p
    assert compress == 0 or compress == 1 or compress == 2
    assert len(S) > 1
    l = math.ceil(math.log2(q)/8)
    PC = S[0]
    X1 = S[1:l+1]
    Y1 = S[l+1:]
    xP = BytesToInt(X1)
    if (compress == 0):
        assert PC == 0x04  # 未压缩
        yP = BytesToInt(Y1)
    # 校验点是否在曲线上 yP^2=xP^3+axP+b mod p
    assert pow(yP, 2, q) == (pow(xP, 3) + ecc_a * xP + ecc_b) % q
    return (xP, yP)

# 定义Fp上的椭圆曲线的加法运算


def inv(x):
    '''
    输入:域元素x
    输出:域元素x的逆元
    '''
    # return gmpy2.invert(x, ecc_p)
    return pow(x, ecc_p-2, mod=ecc_p)


def add(a, b):
    '''
    输入:域元素a,b
    输出:域元素a+b
    '''
    return (a+b) % ecc_p


def sub(a, b):
    '''
    输入:域元素a,b
    输出:域元素a-b
    '''
    return (a-b) % ecc_p


def mul(a, b):
    '''
    输入:域元素a,b
    输出:域元素a*b
    '''
    return (a*b) % ecc_p


def reverse(y):
    return (-y) % ecc_p


def arg_in_double(x: int, y: int):
    a = mul(x, x)
    a = mul(a, 3)+ecc_a
    b = mul(y, 2)
    return mul(a, inv(b))


def arg_in_add(x1: int, y1: int, x2: int, y2: int):
    a = sub(y2, y1)
    b = sub(x2, x1)
    return mul(a, inv(b))


def PointAdd(P: tuple, Q: tuple):
    '''
    输入:椭圆曲线上的点P(xP,yP)和Q(xQ,yQ)
    输出:椭圆曲线上的点R(xR,yR)
    '''
    # 无穷远点
    if (P == INFINITY_POINT):
        return Q
    elif Q == INFINITY_POINT:
        return P
    assert isinstance(P, tuple) and isinstance(Q, tuple)
    xP, yP = P
    xQ, yQ = Q
    if xP == xQ:
        # 互逆
        if reverse(yP) == yQ:
            return INFINITY_POINT
        else:
            _lambda = arg_in_double(xP, yP)
    else:
        # lambda=(yQ-yP)/(xQ-xP)
        _lambda = arg_in_add(xP, yP, xQ, yQ)
    # x3=(lambda^2-xP-xQ) mod p
    x3 = sub(mul(_lambda, _lambda), add(xP, xQ))
    # y3=(lambda(xP-x3)-yP) mod p
    y3 = sub(mul(_lambda, sub(xP, x3)), yP)
    return (x3, y3)

# 多倍点算法


def k_times_point(k: int, P: tuple):
    '''
    输入:整数k和椭圆曲线上的点P(xP,yP)
    输出:椭圆曲线上的点Q(xQ,yQ)
    '''
    if (P == INFINITY_POINT):
        return INFINITY_POINT
    assert isinstance(P, tuple)
    # 二进制展开法
    k = list(reversed(bin(k)[2:]))
    l = len(k)
    Q = INFINITY_POINT
    # j从l-1到0
    for j in range(l-1, -1, -1):
        Q = PointAdd(Q, Q)
        if k[j] == '1':
            Q = PointAdd(Q, P)
    return Q


def bit_xor(x: str, y: str):
    maxlen = max(len(x), len(y))
    x.ljust(maxlen, '0')
    y.ljust(maxlen, '0')
    res = "".join([str(int(x[i]) ^ int(y[i])) for i in range(maxlen)])
    return res


def hash_sm3(data: str) -> int:
    '''
    输入:字符串data
    输出:字符串hash
    '''
    data = BitsToBytes(data)  # 字符串转字节串
    sm3 = hashlib.new('sm3')  # 创建SM3对象
    sm3.update(data)  # 传入数据
    # hash = sm3.hexdigest()  # 获取hash值
    # print(sm3.digest())
    return BytesToBits(sm3.digest())  # 字节串转字符串

# 秘钥派生函数


def KDF(Z: str, klen: int):
    '''
    输入:比特串Z，整数klen(表示要获得的密钥数据的比特长度，要求该值小于(2^32-1)v)
    输出:长度为klen的密钥数据比特串K
    '''
    # 计数器32bit
    ct = 0x00000001
    v = ecc_v
    Ha = {}
    for i in range(1, math.ceil(klen/v)+1):
        # Hai=Hv(Z||ct)
        Ha[i] = hash_sm3(Z+bin(ct)[2:].zfill(32))
        ct += 1
    if klen % v != 0:
        # 将Hv(Z||ct)的前前klen-(v*math.ceil(klen/v))比特作为密钥数据的一部分
        Ha[math.ceil(klen/v)] = Ha[math.ceil(klen/v)
                                   ][:klen-v*math.ceil(klen/v)]
    K = ''
    # 将Hai的比特串连接起来
    for i in range(1, math.ceil(klen/v)+1):
        K += Ha[i]
    return K


def keygenerate():
    '''
    输入:无
    输出(d,P)其中d为私钥,P为公钥。
    '''
    # 随机生成一个大于1小于n-2的整数d[1,n-2]
    d = random.randint(1, ecc_n-2)
    d = 0x1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0
    P = k_times_point(d, ecc_G)
    print('私钥为:', hex(d))
    print('公钥为:', hex(P[0]), hex(P[1]))
    return d, P


def encrypt(pub: tuple, M: bytes):
    '''
    输入:明文比特串M,长度为klen
    输出:密文C
    '''
    M = BytesToBits(M)
    klen = len(M)
    PB = pub
    while True:
        print("working...")
        # 随机生成一个大于1小于n-1的整数k
        #k = random.randint(1, ecc_n)
        k=0x4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F
        
        C1 = k_times_point(k, ecc_G)
        #(47090616174956914622899996468915772943882005751189840835333217072271144997738, 54168491087664091928749728426261095331246089435030531539076541181117877462243)
        C1 = BytesToBits(PointToBytes(C1))
        # C1='0000010001101000000111000101100000011111100011101110000000100011110011111101010100100011000110110000010100110001001111101101001001010111000111000111000010101011001111110110100001101101100000001110000111110100010010111000111011011101110011010010001101010011011010100111011111000010010001111000101100101000100000000001000110111000011101101000111110110110100000111011100111101101110111000110101001011110010011000000011011101000110100000000001011000011111101111111000000101001001101101011101001010001110011000010010011100011'
        # S=[h]PB 若S是无穷远点，则报错
        assert k_times_point(ecc_h, PB) != INFINITY_POINT
        # 计算[k]PB=(x2,y2)
        x2, y2 = k_times_point(k, PB)
        x2 = BytesToBits(DomainElementToBytes(x2))
        # 0110001010101000111111001100000011011110011111001001111011101011000001100001101011010000000000000011111000011000100110000011001011111010001110000010000000000110010010101111111010111011100010001000001110101001110101111100010000110101101000011001100000010100
        y2 = BytesToBits(DomainElementToBytes(y2))
        # 0001001011111111100011000011111110010010000110010001101110010011111010000111001010001001100111011000001010110011111001010110011001011100010000011101001001111110010100101010100101011110011110001011011000100000011010101111011011110001000001111010010011010100
        # 计算t=KDF(x2||y2,klen)
        t = KDF(x2+y2, klen)
        # print('t:',t)
        # 若t全为0比特串则返回第一步
        if t.find("1") != -1:
            break
    # 计算C2=M^t
    C2 = bit_xor(M, t)
    # C3=H(x2||M||y2)
    C3 = hash_sm3(x2+M+y2)
    # 返回密文C=C1||C2||C3
    C = C1+C2+C3
    print("随机数k:", hex(k))
    print("C1:", BitsToBytes(C1).hex())
    print("C2:", BitsToBytes(C2).hex())
    print("C3:", BitsToBytes(C3).hex())
    print("x2:", BitsToBytes(x2).hex())
    print("y2:", BitsToBytes(y2).hex())
    print("x2+y2:", BitsToBytes(x2+y2).hex())
    print("t:", BitsToBytes(t).hex())
    print("M:", BitsToBytes(M).hex())
    return BitsToBytes(C)


def decrypt(pri, C: bytes):
    C = BytesToBits(C)
    dB = pri
    p = ecc_p
    if compress == 0:
        C1_len = 8*(2*math.ceil(math.log2(p)/8)+1)
    C1 = C[:C1_len]
    C3_len = ecc_v
    C2_len = len(C)-C1_len-C3_len
    # 验证C1是否在椭圆曲线上
    C1 = BytesToPoint(BitsToBytes(C1))
    # 计算椭圆曲线点S=[h]C1
    S = k_times_point(ecc_h, C1)
    assert S != INFINITY_POINT
    # 计算[dB]C1=(x2,y2)
    x2, y2 = k_times_point(dB, C1)
    x2 = BytesToBits(DomainElementToBytes(x2))
    y2 = BytesToBits(DomainElementToBytes(y2))
    # 计算t=KDF(x2||y2,klen)
    t = KDF(x2+y2, C2_len)
    # 若t全为0比特串则报错
    assert t.find("1") != -1
    # 计算M=C2^t
    C2 = C[C1_len:C1_len+C2_len]
    M = bit_xor(C2, t)
    # 验证u=H(x2||M||y2)若u!=C3则报错
    u = hash_sm3(x2+M+y2)
    C3 = C[C1_len+C2_len:]
    assert u == C3
    return BitsToBytes(M)


def test():
    #求基点G*n
    print(k_times_point(ecc_n, ecc_G))
    


def main():
    # 初始化椭圆曲线参数
    global ecc_a, ecc_b, ecc_p, ecc_G, ecc_n, ecc_h, ecc_v
    ecc_a, ecc_b, ecc_p, ecc_G, ecc_n, ecc_h, ecc_v = get_curve()
    # 生成密钥对
    print("-----------------生成密钥对-----------------")
    d, P = keygenerate()
    # 明文
    M = b'encryption standard'
    # 加密
    print("-----------------加密-----------------")
    C = encrypt(P, M)
    # 解密
    Message_decrypted = decrypt(d, C)
    print("解密结果:", Message_decrypted)
    if Message_decrypted == M:
        print("解密成功")


if __name__ == "__main__":
    main()
