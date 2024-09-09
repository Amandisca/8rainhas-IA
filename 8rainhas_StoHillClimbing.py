import random
import time
import math

def começa_estado():
    # Cria um estado inicial aleatório
    return [random.randint(0, 7) for _ in range(8)]

def quantidade_ataques(state):
    # Avalia quantos ataques as rainhas estão fazendo
    attacks = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

def cria_vizinhos(state):
    # Gera vizinhos trocando as rainhas de posição
    vizinhos = []
    for i in range(len(state)):
        for row in range(8):
            if row != state[i]:
                neighbor = state[:]
                neighbor[i] = row
                vizinhos.append(neighbor)
    return vizinhos

def stochastic_hill_climbing(max_iteracoes=500):
    # Implementa o algoritmo Stochastic Hill Climbing para o problema das oito rainhas.
    estado_atual = começa_estado()
    ataques_atuais = quantidade_ataques(estado_atual)
    iteracoes = 0
    
    while ataques_atuais > 0 and iteracoes < max_iteracoes:
        vizinhos = cria_vizinhos(estado_atual)
        proximo_estado = random.choice(vizinhos)
        proximo_ataque = quantidade_ataques(proximo_estado)
        
        if proximo_ataque <= ataques_atuais:
            estado_atual, ataques_atuais = proximo_estado, proximo_ataque

        iteracoes += 1
    
    return estado_atual, ataques_atuais, iteracoes

# Executar o algoritmo (programa)
# solucao, iteracoes = stochastic_hill_climbing()

# if iteracoes < 500 or quantidade_ataques(solucao) == 0:
#     print("Uma solução foi encontrada:", solucao)
#     print("Quantidade de ataques:", quantidade_ataques(solucao))
#     print("Quantidade de iteraçoes:", iteracoes)

# else:
#     print("Uma solução não foi encontrada  :(")
#     print("Solução mais próxima:", solucao)
#     print("Quantidade de ataques:", quantidade_ataques(solucao))
#     print("Quantidade de iteraçoes:", iteracoes)


def calcular_media(valores):
    # Calcula a média de uma lista de valores
    if not valores:
        return 0
    return sum(valores) / len(valores)

def calcular_desvio_padrao(valores):
    # Calcula o desvio padrão de uma lista de valores
    media = calcular_media(valores)
    variancia = sum((x - media) ** 2 for x in valores) / len(valores) if valores else 0
    return math.sqrt(variancia)

def executar_e_calcular_estatisticas(num_experimentos=50, max_iterations=500):
    # Executa o algoritmo várias vezes e calcula estatísticas
    lista_iteracoes = []
    lista_tempo = []
    melhores_solucoes = []

    for _ in range(num_experimentos):
        tempo_inicio = time.time()
        solucao, _, iteracoes = stochastic_hill_climbing(max_iterations)
        tempo_final = time.time()

        tempo_execucao = tempo_final - tempo_inicio

        lista_iteracoes.append(iteracoes)
        lista_tempo.append(tempo_execucao)

        # Adiciona a solução à lista de melhores soluções se for uma solução válida ou próxima
        if quantidade_ataques(solucao) == 0:
            melhores_solucoes.append(solucao)

    # Calcular média e desvio padrão
    media_iteracoes = calcular_media(lista_iteracoes)
    desvio_iteracoes = calcular_desvio_padrao(lista_iteracoes)
    media_tempos = calcular_media(lista_tempo)
    desvio_tempos = calcular_desvio_padrao(lista_tempo)

    # Encontrar as 5 melhores soluções distintas
    solucoes_distintas = []
    for solucao in melhores_solucoes:
        if solucao not in solucoes_distintas:
            solucoes_distintas.append(solucao)
        if len(solucoes_distintas) >= 5:
            break

    return media_iteracoes, desvio_iteracoes, media_tempos, desvio_tempos, solucoes_distintas

def mostrar_melhores_solucoes(solucoes_distintas):
    # Mostra as melhores soluções distintas encontradas
    print("\nCinco melhores soluções distintas encontradas:")
    for i, solucao in enumerate(solucoes_distintas, 1):
        print(f"Solução {i}: {solucao} com custo {quantidade_ataques(solucao)}")

# Exemplo de uso
if __name__ == "__main__":
    media_iteracoes, desvio_iteracoes, media_tempos, desvio_tempos, melhores_solucoes = executar_e_calcular_estatisticas()
    print(f"")
    print(f"Média das iterações: {media_iteracoes:.2f}")
    print(f"Desvio padrão das iterações: {desvio_iteracoes:.2f}")
    print(f"Média do tempo de execução: {media_tempos:.4f} segundos")
    print(f"Desvio padrão do tempo de execução: {desvio_tempos:.4f} segundos")
    
    mostrar_melhores_solucoes(melhores_solucoes)
