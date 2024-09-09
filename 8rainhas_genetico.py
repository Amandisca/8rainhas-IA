import time
import math
import random

# Funções auxiliares
def calcular_media(valores):
    if not valores:
        return 0
    return sum(valores) / len(valores)

def calcular_desvio_padrao(valores):
    media = calcular_media(valores)
    variancia = sum((x - media) ** 2 for x in valores) / len(valores) if valores else 0
    return math.sqrt(variancia)

# Função de aptidão externa para verificar soluções finais
def aptidao_externa(solucao):
    NUM_RAINHAS = 8
    conflitos = 0
    for i in range(NUM_RAINHAS):
        for j in range(i + 1, NUM_RAINHAS):
            if solucao[i] == solucao[j] or abs(solucao[i] - solucao[j]) == j - i:
                conflitos += 1
    return conflitos

# Algoritmo Genético que será executado várias vezes
def algoritmo_genetico():
    TAMANHO_POPULACAO = 20
    TAXA_CRUZAMENTO = 0.8
    TAXA_MUTACAO = 0.03
    MAX_GERACOES = 1000
    NUM_RAINHAS = 8
    BIT_LENGTH = 3

    # Função de aptidão interna, usada durante o algoritmo genético
    def aptidao_interna(individuo):
        def decodificar_individuo(individuo):
            return [int("".join(map(str, individuo[i:i+BIT_LENGTH])), 2) for i in range(0, len(individuo), BIT_LENGTH)]

        rainhas = decodificar_individuo(individuo)
        conflitos = 0
        for i in range(NUM_RAINHAS):
            for j in range(i + 1, NUM_RAINHAS):
                if rainhas[i] == rainhas[j] or abs(rainhas[i] - rainhas[j]) == j - i:
                    conflitos += 1
        return conflitos

    def inicializar_populacao():
        return [[random.randint(0, 1) for _ in range(NUM_RAINHAS * BIT_LENGTH)] for _ in range(TAMANHO_POPULACAO)]

    def decodificar_individuo(individuo):
        return [int("".join(map(str, individuo[i:i+BIT_LENGTH])), 2) for i in range(0, len(individuo), BIT_LENGTH)]

    def selecao_roleta(populacao, fitness):
        soma_fitness = sum(fitness)
        pick = random.uniform(0, soma_fitness)
        corrente = 0
        for i, fit in enumerate(fitness):
            corrente += fit
            if corrente > pick:
                return populacao[i]

    def cruzamento(pai1, pai2):
        if random.random() < TAXA_CRUZAMENTO:
            ponto_corte = random.randint(1, NUM_RAINHAS * BIT_LENGTH - 1)
            return pai1[:ponto_corte] + pai2[ponto_corte:]
        return pai1

    def mutacao(individuo):
        for i in range(len(individuo)):
            if random.random() < TAXA_MUTACAO:
                individuo[i] = 1 if individuo[i] == 0 else 0
        return individuo

    def elitismo(populacao, fitness):
        return [populacao[i] for i in sorted(range(len(fitness)), key=lambda k: fitness[k])[:2]]

    populacao = inicializar_populacao()

    for geracao in range(MAX_GERACOES):
        fitness = [aptidao_interna(individuo) for individuo in populacao]
        
        if 0 in fitness:
            solucao = populacao[fitness.index(0)]
            return decodificar_individuo(solucao), geracao + 1  # Solução ótima encontrada

        nova_populacao = elitismo(populacao, fitness)

        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1 = selecao_roleta(populacao, fitness)
            pai2 = selecao_roleta(populacao, fitness)
            filho = cruzamento(pai1, pai2)
            filho = mutacao(filho)
            nova_populacao.append(filho)

        populacao = nova_populacao

    fitness_final = [aptidao_interna(individuo) for individuo in populacao]
    melhor_solucao = populacao[fitness_final.index(min(fitness_final))]
    return decodificar_individuo(melhor_solucao), MAX_GERACOES

# Função que executa o algoritmo genético várias vezes e coleta estatísticas
def executar_e_calcular_estatisticas(num_experimentos=50, max_iterations=500):
    lista_iteracoes = []
    lista_tempo = []
    melhores_solucoes = []

    for _ in range(num_experimentos):
        tempo_inicio = time.time()
        solucao, iteracoes = algoritmo_genetico()
        tempo_final = time.time()

        tempo_execucao = tempo_final - tempo_inicio

        lista_iteracoes.append(iteracoes)
        lista_tempo.append(tempo_execucao)

        # Adiciona a solução à lista de melhores soluções se for válida
        if aptidao_externa(solucao) == 0:
            solucao_tuple = tuple(solucao)
            if solucao_tuple not in melhores_solucoes:
                melhores_solucoes.append(solucao_tuple)

    # Calcular média e desvio padrão
    media_iteracoes = calcular_media(lista_iteracoes)
    desvio_iteracoes = calcular_desvio_padrao(lista_iteracoes)
    media_tempos = calcular_media(lista_tempo)
    desvio_tempos = calcular_desvio_padrao(lista_tempo)

    # Encontrar as 5 melhores soluções distintas
    solucoes_distintas = melhores_solucoes[:5]

    return media_iteracoes, desvio_iteracoes, media_tempos, desvio_tempos, solucoes_distintas

# Função para mostrar as melhores soluções encontradas
def mostrar_melhores_solucoes(solucoes_distintas):
    print("\nCinco melhores soluções distintas encontradas:")
    for i, solucao in enumerate(solucoes_distintas, 1):
        print(f"Solução {i}: {solucao} com {aptidao_externa(solucao)} conflitos")

# Exemplo de uso
if __name__ == "__main__":
    media_iteracoes, desvio_iteracoes, media_tempos, desvio_tempos, melhores_solucoes = executar_e_calcular_estatisticas()

    print(f"Média das iterações: {media_iteracoes:.2f}")
    print(f"Desvio padrão das iterações: {desvio_iteracoes:.2f}")
    print(f"Média do tempo de execução: {media_tempos:.4f} segundos")
    print(f"Desvio padrão do tempo de execução: {desvio_tempos:.4f} segundos")
    
    mostrar_melhores_solucoes(melhores_solucoes)
