def collatz(numero):
    if numero % 2 == 0:
        return numero // 2
    elif numero % 2 == 1:
        return 3 * numero + 1

numeroSeq = int(input('Vamos pra prova real: '))

seq = 1
while numeroSeq != 1:
    seq += 1
    numeroSeq = collatz(numeroSeq)
print(seq)