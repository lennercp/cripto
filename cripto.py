import sys
from math import gcd


def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1

    gc, x1, y1 = gcdExtended(b % a, a)

    x = y1 - (b // a) * x1
    y = x1

    return gc, x, y

print(gcdExtended(27,513))

class Ww2:
    tab = []
    word = ""
    mapp = {}

    def __init__(self):
        r = "ADFGVX"
        print("Digite a tabela:")
        print(*list(r))

        self.tab = {}
        self.tab2 = {}
        for i in range(len(r)):
            row = input().upper().split()
            for l in range(len(row)):
                self.tab[row[l]] = f"{r[i]}{r[l]}"
                self.tab2[f"{r[i]}{r[l]}"] = row[l]

        self.word = input("Digite a palavra de transposição: ").upper()
        s_word = sorted(self.word)

        self.mapp = dict([(i, self.word.index(s_word[i])) for i in range(len(s_word))])

    def encriptar(self, text):

        cypher = {l: [] for l in self.word}
        text = text.upper()
        l = 0
        c = 0
        while True:
            drupa = self.tab[text[c]]
            cypher[self.word[l % len(self.word)]].append(drupa[0])
            l += 1
            cypher[self.word[(l) % len(self.word)]].append(drupa[1])
            l += 1

            c += 1
            if c > len(text) - 1: break

        sorted = list(cypher.keys())
        sorted.sort()

        cypher2 = ""
        for k in sorted:
            cypher2 += "".join(cypher[k])
            cypher2 += ' '

        return cypher2

    def decriptar(self, cypher):
        cypher = cypher.split()

        tab = [None for _ in range(len(cypher))]
        for i in range(len(cypher)):
            tab[self.mapp[i]] = cypher[i]

        tabela = []
        for i in range(len(tab[0])):
            linha = []
            for j in range(len(tab)):
                try:
                    linha.append(tab[j][i])
                except:
                    pass
            tabela.append(linha)

        chars = []
        t_linha = len(tabela[0])
        for i in range(0, len(tabela) * len(tabela[0]), 2):
            try:
                chars.append(tabela[i // t_linha][i % t_linha] + tabela[(i + 1) // t_linha][(i + 1) % t_linha])
            except:
                break

        return "".join(self.tab2[c] for c in chars)


class Rsa:
    n = 0
    e = 0
    d = 0

    def __init__(self):

        p, q = [int(x) for x in input("Digite p e q: ").split()]

        self.n = p * q

        print(f"Temos n = {self.n}")

        totiente = (p - 1) * (q - 1)

        print(f"Temos totiente(n) = {totiente}")

        self.e = int(input("E = Digite um número que seja coprimo com o totiente: "))
        _, _, self.d = gcdExtended(totiente, self.e)
        self.d = (self.d % totiente + totiente) % totiente
        print(f"D = {self.d}")

    def encriptar(self, cypher):
        return pow(int(cypher), self.e, self.n)

    def decriptar(self, cypher):
        return pow(int(cypher), self.d, self.n)


class Gm:
    a = 0
    p = 0
    q = 0
    def __init__(self):
        self.p, self.q = [int(x) for x in input("Digite p e q, tal que p e q seja congruente a 3 mod 4: ").split()]
        self.n = self.p * self.q

        print(f"Temos n = {self.n}")

        
        for a in range(2, self.n):
            if pow(a, (self.p - 1)//2, self.p) == self.p-1:
                if pow(a, (self.q-1)//2, self.q) == self.q-1:
                    break
        self.a = self.n-1
        print(f"Chegamos em a = {self.a}")

    def encriptar(self, mensagem):
        mensagem = [int(c) for c in mensagem]
        b = [int(x) for x in input(f"B = Digite {len(mensagem)} valores entre 2 e {self.n-1} que não seja {self.p} e {self.q}: ").split()]

        cypher = [((b[i] ** 2) * (self.a ** mensagem[i])) % self.n for i in range(len(mensagem))]
        return cypher

    def decriptar(self, cypher):
        cypher = [int(c) for c in cypher.split()]
        bits = [0 if pow(c, (self.p-1)//2, self.p) == 1 and pow(c, (self.q-1)//2, self.q) == 1 else 1 for c in cypher]
        return ''.join(map(str, bits))


class Gamal:
    q = 0
    g = 0
    y = 0
    x = 0

    def __init__(self):
        self.q = int(input('Digite o valor de q (ordem do grupo): '))

        self.g = int(input("Digite um gerador do grupo: "))
        self.x = int(input(f"X = Digite um numero entre 2 e {self.q - 1}: "))
        print("X = ", self.x)

        self.y = pow(self.g, self.x, self.q)

        print(f"Temos que a chave pública é: ({self.y}, {self.q}, {self.g}).")

    def encriptar(self, num):
        num = int(num)

        r = int(input(f"R = Digite um numero: "))
        print("R = ", r)

        c1 = pow(self.g, r, self.q)

        s = pow(self.y, r, self.q)

        c2 = (num % self.q) * s % self.q

        return (c1, c2)

    def decriptar(self, cypher):
        c1, c2 = [int(m) for m in cypher.split()]

        t = pow(c1, self.x, self.q)
        _, _, t_1 = gcdExtended(self.q, t)
        print('t', t_1)
        m_1 = c2 * t_1

        return m_1 % self.q


nome_metodo = sys.argv[1].capitalize()

try:
    classe = eval(f'{nome_metodo}()')
    encriptar, decriptar = eval(f'{nome_metodo}.encriptar, {nome_metodo}.decriptar')
except:
    print(f"Algoritmo {nome_metodo} não suportado, a forma correta é python3 cripto.py {{nome_metodo}}")
    sys.exit(0)

while True:
    opcao = input("Você quer encriptar ou decriptar? [E/D/Q para sair] ").upper()
    if opcao == 'E':
        try:
            plain = input("Digite o texto/número para ser encriptado ")
            print(f"Cypher: {encriptar(classe,plain)} ")
        except:
            print("Formato errado")
            continue

    elif opcao == 'D':
        try:
            cypher = input("Digite o texto/número para ser decriptado ")
            print(f"Plain: {decriptar(classe,cypher)} ")
        except:
            print("Formato errado")
    
    elif opcao == 'Q':
        print("Até mais ver! ")
        break
    else:
        print("Deixa de ser burro pow!")
