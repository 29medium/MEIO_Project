import random
from numpy import random

ciclos = 4
semanas = 50

media = 523
desvio = 57
initialS = 3767
initials = 2601

p1 = 0.26
p2 = 0.54
p3 = 0.2

C1 = 0.345
C2 = 20
C3 = 1500

procura = random.normal(loc=media, scale=desvio, size=50).astype(int).tolist()

def calculaTempoEncomenda(index, s, tempo_encomenda, stock):
    if (index%ciclos+1==ciclos) and stock[index]<s:
        tempo = random.random()
        if(tempo<p1):
            tempo_encomenda.append(1)
        elif(tempo<p1+p2):
            tempo_encomenda.append(2)
        else:
            tempo_encomenda.append(3)
    else:
        tempo_encomenda.append(0)


def calculaCustos(index, stock, custo_posse, custo_quebra, custo_encomenda, tempo_encomenda):
    if stock[index] > 0:
        custo_posse.append(stock[index]*C1)
        custo_quebra.append(0)
    else:
        custo_posse.append(0)
        custo_quebra.append(abs(stock[index]*C2))
    if tempo_encomenda[index] == 0:
        custo_encomenda.append(0)
    else:
        custo_encomenda.append(C3)

def printCustos(custoTotal, stockMedio, quebras, title):
    custo = "{:.2f}".format(custoTotal)
    print("\n----------------------")
    print(title)
    print("----------------------")
    print("Custo Total: " + str(custo) + "€")
    print("Stock Médio: " + str(int(stockMedio)))
    print("Número Quebras: " + str(quebras))
    print("----------------------")

def run(s, S, title):
    stock = []
    tempo_encomenda = []
    custo_posse = []
    custo_quebra = []
    custo_encomenda = []

    stock.append(S-procura[0])
    calculaTempoEncomenda(0, s, tempo_encomenda, stock)
    calculaCustos(0, stock, custo_posse, custo_quebra, custo_encomenda, tempo_encomenda)

    for i in range(1,ciclos):
        stock.append(stock[i-1]-procura[i])
        calculaTempoEncomenda(i, s, tempo_encomenda, stock)
        calculaCustos(i, stock, custo_posse, custo_quebra,
                      custo_encomenda, tempo_encomenda)

    for i in range(ciclos,semanas):
        cycleIndex = i%ciclos + 1
        cycle = (i//ciclos) * ciclos - 1 

        if tempo_encomenda[cycle]==cycleIndex and cycleIndex != ciclos:
            stock.append(stock[i-1]-procura[i]+S-stock[cycle])
        else:
            stock.append(stock[i-1]-procura[i])

        calculaTempoEncomenda(i, s, tempo_encomenda, stock)
        calculaCustos(i, stock, custo_posse, custo_quebra,
                      custo_encomenda, tempo_encomenda)

    custoTotal = sum(custo_posse) + sum(custo_quebra) + sum(custo_encomenda)
    stockMedio = sum(stock) / len(stock)
    quebras = len(list(filter(lambda x: (x<0), stock)))

    printCustos(custoTotal, stockMedio, quebras, title)


run(initials, initialS, "Para s e S")
run(initials*1.05, initialS, "Para s+5% e S")
run(initials*0.95, initialS, "Para s-5% e S")
run(initials, initialS*1.05, "Para s e S+5%")
run(initials, initialS*0.95, "Para s e S-5%")