import hashlib
import random
from miller_rabin import miller_rabin
from oaep import OAEP
from base64 import b64encode, b64decode, decode

#1º Passo Gerar dois números primos de 1024 bits p e q

#2º Passo Calcular o modulo RSA: n = p * q

#3º Passo Calcular o totiente de Euler: phi = (p-1) * (q-1)

#4º Passo Escolher um inteiro e tal que 1 < e < phi e e seja primo relativo a phi

#5º Passo Calcular o inverso modular de e: d = e^-1 mod phi
  #5.1º Algortimo de Euclides Estendido: phi*X + e*Y = 1 => phi = e*Y + k 

#######################################

#6º Passo Gerar a chave pública: (e, n)

#7º Passo Gerar a chave privada: (d, n)

#######################################

#8º Passo: Gerar o hash do arquivo a ser assinado

#9º Passo: Criptografar o hash com a chave privada c = m^e mod n

#10º Passo: Descriptografar o hash com a chave pública m = c^d mod n 
# e validar se o hash do arquivo é igual ao hash descriptografado


keysize = 1024
oaep = OAEP(keysize)
def calc_num_bytes(n: int):
    cnt = 0 
    while n != 0:
        n >>= 8
        cnt += 1
    return cnt

# Retorna True se o número for primo 
# Em caso de incerteza chama o algoritmo de Miller-Rabin para testar a primalidade
def isPrime(n): 
  if n < 2:
    return False

  lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
  if n in lowPrimes:
    return True
  
  for prime in lowPrimes:
    if n % prime == 0:
      return False

  if not miller_rabin(n):
    return False
  
  return True


  
def generateKeys(keysize=1024):
  e = d = N = 0

  #1º Passo Gerar dois números primos p e q
  p = generateLargePrime(keysize)
  q = generateLargePrime(keysize)
  print(f"p = {p}\nq = {q}\n\n")
  #2º Passo Calcular o modulo RSA: n = p * q
  N = p * q # Modulo RSA

  #3º Passo Calcular o totiente de Euler: phi = (p-1) * (q-1)
  phiN = (p - 1) * (q - 1) # Euler Totient

  #4º Passo Escolher um inteiro e tal que 1 < e < phiN e e seja primo relativo a phiN -> Public Key
  while True:
    e = random.randrange(2 ** (keysize-1), 2 ** keysize - 1)
    if (isCoprime(e, phiN)):
      break

  #5º Passo Calcular o inverso modular de e: d = e^-1 mod phi -> Private Key
  d = modularInverse(e, phiN)

  return e, d, N

def generateLargePrime(keysize): # Gera um número primo de 1024 bits
  
  while True:
    num = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
    
    if (isPrime(num)):
      return num

def isCoprime(p, q): #Verifica se dois números são primos relativos
  return gcd(p, q) == 1


def gcd(p, q): #Algoritmo de Euclides para calcular o gcd(Maior Divisor Comum) de dois números
  while q:
    p, q = q, p % q
  return p

def egcd(a, b):
  s = 0; old_s = 1
  t = 1; old_t = 0
  r = b; old_r = a

  while r != 0:
    quotient = old_r // r
    old_r, r = r, old_r - quotient * r
    old_s, s = s, old_s - quotient * s
    old_t, t = t, old_t - quotient * t
  #return gcd, x, y
  return old_r, old_s, old_t

def modularInverse(a, b):
  gcd, x, y = egcd(a, b)

  if x < 0:
    x += b

  return x


def rsa_encrypt_text(e, N, msg):
  cipher = ""

  for c in msg:
    m = ord(c)
    cipher += str(pow(m, e, N)) + " "

  return cipher

def rsa_decrypt_text(d, N, cipher):
  msg = ""
  parts = cipher.split()

  for part in parts:
    if part:
      c = int(part)
      msg += chr(pow(c, d, N))
  
  return msg


def rsa_encrypt_num(e, N, msg):
  cipher = pow(msg, e, N)
  return cipher

def rsa_decrypt_num(d, N, cipher):
  msg = pow(cipher, d, N)
  return msg
  

def main():
  sign_pub = sign_priv = sign_mod = 0
  pubKey = privKey = Modulo = 0
  while True:
    print("Selecione uma opção:")
    print("1 - RSA - Geração de Chaves")
    print("2 - RSA - Ler Chaves de Arquivo")
    print("3 - RSA - Gerar assinatura digital")
    print("4 - RSA - Verificar assinatura digital") 
    option = int(input("Opção: "))
    match option:
      case 1:
        pubKey, privKey, Modulo = generateKeys(keysize)
        save = input("Chaves geradas com sucesso! Deseja salvar em um arquivo? s/n:")
        if save == "s" or save == "S" or save == 'y' or save == 'Y':
          name = input("Nome do arquivo: ")
          with open(f"{name}.pub", "w") as file:
            file.write(str(pubKey))
            sign_pub = pubKey
          with open(f"{name}.mod", "w") as file:
            file.write(str(Modulo))
            sign_mod = Modulo
          with open(f"{name}.priv", "w") as file:
            file.write(str(privKey))
            sign_priv = privKey
      case 2:
        name = input("Nome do arquivo: ")
        with open(f"{name}.pub", "rb") as file:
          pubKey = int(file.readline())
        with open(f"{name}.mod", "rb") as file:
          Modulo = int(file.readline())
        with open(f"{name}.priv", "rb") as file:
          privKey = int(file.readline())
        if(pubKey == sign_pub): print("Chave pública válida!")
        if(privKey == sign_priv): print("Chave privada válida!")
        if(Modulo == sign_mod): print("Módulo válido!")
      case 3:
        file_name = input("Insira o nome do arquivo a ser assinado: ")
        with open(file_name, "rb") as file:
          file = file.read()
        hash_code = hashlib.sha3_256(file).hexdigest()
        hash_oaep, P1_Size = oaep.oaep_mask(int(hash_code, 16))
        hash_cipher = rsa_encrypt_num(privKey, Modulo, hash_oaep)
        hash_encoded = b64encode(hash_cipher.to_bytes(calc_num_bytes(hash_cipher), 'big'))
        with open(f'{file_name.split(".")[0]}_sign.bin', "wb") as file:
          file.write(hash_encoded)
      case 4:
        file_name = input("Insira o nome do arquivo a ser assinado: ")
        with open(file_name, "rb") as file:
          file = file.read()
        hash_code = hashlib.sha3_256(file).hexdigest()
        with open(f'{file_name.split(".")[0]}_sign.bin', "rb") as file:
          signature_cipher = b64decode(file.read())
        hash_code = int(hash_code, 16)
        msg_oaep = rsa_decrypt_num(pubKey, Modulo, int.from_bytes(signature_cipher, 'big'))
        signature = oaep.oaep_unmask(msg_oaep, P1_Size)
        if hash_code == signature:
          print("Arquivo validado!")
        else:
          print("Arquivo corrompido!")
if __name__ == '__main__':
  main()