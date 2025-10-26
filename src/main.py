"""
=================================================================================
ALGORITMO PARA ENCONTRAR A LONGEST INCREASING SUBSEQUENCE (LIS)
Subsequência Crescente Mais Longa
=================================================================================

Este programa implementa um algoritmo eficiente para encontrar a LIS de uma
sequência de números inteiros.

O algoritmo utiliza a técnica do Principal Row of Young Tableaux (PRYT),
também conhecida como mecanismo de Knuth, combinada com busca binária para
alcançar complexidade de tempo O(n log n).

Baseado nos conceitos do artigo:
"Improvised divide and conquer approach for the LIS problem"
por Seema Rani e Dharmveer Singh Rajpoot
Journal of Discrete Algorithms 48 (2018) 17-26

Autor: Python Implementation
Data: Outubro 2025
=================================================================================
"""

from typing import List, Tuple
import bisect


def encontrar_lis(sequencia: List[int]) -> Tuple[int, List[int]]:
    """
    Encontra a Longest Increasing Subsequence (LIS) de uma sequência.
    
    === O QUE É UMA LIS? ===
    
    Uma subsequência crescente é um conjunto de elementos da sequência original
    que mantém a ordem relativa e está em ordem crescente estrita.
    
    Exemplo:
        Sequência: [3, 10, 2, 1, 20, 15, 30, 13]
        Uma LIS possível: [3, 10, 15, 30] (comprimento 4)
        Outra LIS possível: [1, 20, 30] (comprimento 3)
        A maior LIS: [3, 10, 15, 30] ou [3, 10, 20, 30] (comprimento 4)
    
    === COMO FUNCIONA O ALGORITMO? ===
    
    O algoritmo usa uma estrutura chamada PRYT (Principal Row of Young Tableaux):
    
    1. PRYT (tails): Um array onde tails[i] armazena o MENOR elemento que pode
       terminar uma subsequência crescente de comprimento i+1.
       
    2. Para cada elemento da sequência:
       a) Usa busca binária para encontrar onde ele pode ser inserido em tails
       b) Atualiza tails na posição encontrada
       c) Registra o predecessor para poder reconstruir a LIS depois
       
    3. No final, o comprimento de tails é o comprimento da LIS
    
    === POR QUE tails[i] ARMAZENA O MENOR ELEMENTO? ===
    
    Manter o menor elemento possível em cada posição maximiza as chances de
    estender a subsequência com elementos futuros.
    
    Exemplo passo a passo com [3, 10, 2, 1, 20, 15, 30, 13]:
    
    i=0, elem=3:  tails = [3]                    (LIS de tam 1: termina em 3)
    i=1, elem=10: tails = [3, 10]                (LIS de tam 2: termina em 10)
    i=2, elem=2:  tails = [2, 10]                (substitui 3 por 2, menor!)
    i=3, elem=1:  tails = [1, 10]                (substitui 2 por 1, menor!)
    i=4, elem=20: tails = [1, 10, 20]            (estende para tam 3)
    i=5, elem=15: tails = [1, 10, 15]            (substitui 20 por 15, menor!)
    i=6, elem=30: tails = [1, 10, 15, 30]        (estende para tam 4)
    i=7, elem=13: tails = [1, 10, 13, 30]        (substitui 15 por 13, menor!)
    
    Comprimento final da LIS: 4
    
    Args:
        sequencia: Lista de números inteiros
        
    Returns:
        Tupla contendo:
        - comprimento: Tamanho da LIS
        - lis: Lista com os valores da LIS em ordem crescente
        
    Complexidade de Tempo: O(n log n)
    Complexidade de Espaço: O(n)
    """
    
    # === CASO ESPECIAL: SEQUÊNCIA VAZIA ===
    if not sequencia:
        return 0, []
    
    n = len(sequencia)
    
    # === ESTRUTURAS DE DADOS ===
    
    # tails[i] armazena o menor elemento que termina uma LIS de comprimento i+1
    # Exemplo: se tails[2] = 15, significa que 15 é o menor elemento que pode
    # terminar uma subsequência crescente de comprimento 3
    tails = []
    
    # predecessor[i] armazena o índice do elemento anterior na LIS que termina em i
    # Isso permite reconstruir a LIS completa no final
    # Exemplo: se predecessor[5] = 2, o elemento antes de sequencia[5] na LIS
    # é sequencia[2]
    predecessor = [-1] * n
    
    # indices_tails[i] armazena em qual posição do array tails está o elemento i
    # Isso ajuda a encontrar predecessores corretos
    indices_tails = [0] * n
    
    # === PROCESSAMENTO DE CADA ELEMENTO ===
    
    for i in range(n):
        elemento_atual = sequencia[i]
        
        # --- PASSO 1: BUSCA BINÁRIA ---
        # Encontra a posição onde elemento_atual deve ser inserido em tails
        # usando busca binária (função bisect_left do Python)
        # 
        # bisect_left retorna o índice mais à esquerda onde elemento_atual
        # pode ser inserido mantendo tails ordenado
        #
        # Exemplo:
        #   tails = [1, 10, 15, 30], elemento_atual = 13
        #   posicao = 2 (13 deve substituir 15)
        
        posicao = bisect.bisect_left(tails, elemento_atual)
        
        # --- PASSO 2: ENCONTRA O PREDECESSOR ---
        # O predecessor é o elemento na posição anterior de tails
        # que seja menor que o elemento atual
        
        if posicao > 0:
            # Precisa encontrar qual elemento está em tails[posicao-1]
            # Percorre de trás para frente procurando o elemento correto
            for j in range(i - 1, -1, -1):
                # Verifica se o elemento j está na posição correta do tails
                # e é menor que o elemento atual (condição de crescente)
                if (indices_tails[j] == posicao - 1 and 
                    sequencia[j] < elemento_atual):
                    predecessor[i] = j
                    break
        
        # --- PASSO 3: ATUALIZA O ARRAY tails ---
        # Se a posição está dentro do array, substitui o elemento
        # Caso contrário, adiciona no final (estendendo a LIS)
        
        if posicao < len(tails):
            # Substitui o elemento existente por um menor
            # Isso não muda o comprimento da LIS, mas melhora as chances
            # de estendê-la com elementos futuros
            tails[posicao] = elemento_atual
        else:
            # Adiciona um novo elemento no final
            # Isso significa que encontramos uma LIS maior!
            tails.append(elemento_atual)
        
        # --- PASSO 4: REGISTRA A POSIÇÃO ---
        # Guarda em que posição do tails este elemento está
        indices_tails[i] = posicao
    
    # === RECONSTRUÇÃO DA LIS ===
    
    comprimento_lis = len(tails)
    
    # --- PASSO 1: ENCONTRA O ÚLTIMO ELEMENTO DA LIS ---
    # O último elemento é aquele que está na posição mais alta de tails
    # e aparece mais à direita na sequência original
    
    ultimo_indice = -1
    for i in range(n - 1, -1, -1):
        # Procura de trás para frente o primeiro elemento que está
        # na última posição do tails
        if indices_tails[i] == comprimento_lis - 1:
            ultimo_indice = i
            break
    
    # --- PASSO 2: RECONSTRÓI A LIS SEGUINDO OS PREDECESSORES ---
    # Começa do último elemento e vai seguindo a cadeia de predecessores
    
    lis = []
    indice_atual = ultimo_indice
    
    while indice_atual != -1:
        # Adiciona o elemento atual à LIS
        lis.append(sequencia[indice_atual])
        # Move para o predecessor
        indice_atual = predecessor[indice_atual]
    
    # --- PASSO 3: INVERTE A LIS ---
    # Como construímos de trás para frente, precisa inverter
    lis.reverse()
    
    return comprimento_lis, lis


def validar_lis(sequencia: List[int], lis: List[int]) -> bool:
    """
    Valida se a LIS encontrada é realmente uma subsequência crescente válida.
    
    Verifica duas coisas:
    1. Todos os elementos da LIS estão na sequência original
    2. Os elementos da LIS estão em ordem crescente estrita
    
    Args:
        sequencia: Sequência original
        lis: LIS a ser validada
        
    Returns:
        True se a LIS é válida, False caso contrário
    """
    if not lis:
        return True
    
    # Verifica se está em ordem crescente estrita
    for i in range(len(lis) - 1):
        if lis[i] >= lis[i + 1]:
            return False
    
    # Verifica se é uma subsequência da sequência original
    # (mantém a ordem relativa)
    idx_sequencia = 0
    idx_lis = 0
    
    while idx_sequencia < len(sequencia) and idx_lis < len(lis):
        if sequencia[idx_sequencia] == lis[idx_lis]:
            idx_lis += 1
        idx_sequencia += 1
    
    return idx_lis == len(lis)


def imprimir_passo_a_passo(sequencia: List[int]) -> None:
    """
    Demonstra o algoritmo passo a passo para fins educacionais.
    
    Args:
        sequencia: Sequência para analisar
    """
    print(f"\n{'='*70}")
    print(f"EXECUÇÃO PASSO A PASSO DO ALGORITMO")
    print(f"{'='*70}")
    print(f"Sequência: {sequencia}")
    print(f"{'-'*70}\n")
    
    if not sequencia:
        print("Sequência vazia - não há LIS")
        return
    
    n = len(sequencia)
    tails = []
    
    for i in range(n):
        elem = sequencia[i]
        pos = bisect.bisect_left(tails, elem)
        
        acao = ""
        if pos < len(tails):
            acao = f"substitui {tails[pos]} por {elem}"
            tails[pos] = elem
        else:
            acao = f"adiciona {elem} no final"
            tails.append(elem)
        
        print(f"Passo {i+1}: elemento = {elem:3d}, posição = {pos}, {acao}")
        print(f"         tails = {tails}")
        print()
    
    print(f"{'-'*70}")
    print(f"Comprimento final da LIS: {len(tails)}")
    print(f"Array tails final: {tails}")
    print(f"{'='*70}\n")


def main():
    """
    Função principal com exemplos de teste do algoritmo.
    """
    print("="*80)
    print(" " * 10 + "ALGORITMO PARA LONGEST INCREASING SUBSEQUENCE (LIS)")
    print(" " * 15 + "Subsequência Crescente Mais Longa")
    print("="*80)
    print()
    
    # === EXEMPLO 1: SEQUÊNCIA DO ARTIGO ===
    print("EXEMPLO 1: Sequência do artigo científico")
    print("-" * 80)
    seq1 = [8, 9, 5, 2, 3, 7, 10, 4, 1, 6]
    print(f"Sequência: {seq1}")
    
    comprimento, lis = encontrar_lis(seq1)
    valida = validar_lis(seq1, lis)
    
    print(f"Comprimento da LIS: {comprimento}")
    print(f"LIS encontrada: {lis}")
    print(f"Válida: {'✓ Sim' if valida else '✗ Não'}")
    print()
    
    # === EXEMPLO 2: SEQUÊNCIA CRESCENTE ===
    print("EXEMPLO 2: Sequência totalmente crescente")
    print("-" * 80)
    seq2 = [1, 2, 3, 4, 5]
    print(f"Sequência: {seq2}")
    
    comprimento, lis = encontrar_lis(seq2)
    valida = validar_lis(seq2, lis)
    
    print(f"Comprimento da LIS: {comprimento}")
    print(f"LIS encontrada: {lis}")
    print(f"Válida: {'✓ Sim' if valida else '✗ Não'}")
    print(f"Observação: Toda sequência crescente é sua própria LIS")
    print()
    
    # === EXEMPLO 3: SEQUÊNCIA DECRESCENTE ===
    print("EXEMPLO 3: Sequência totalmente decrescente")
    print("-" * 80)
    seq3 = [5, 4, 3, 2, 1]
    print(f"Sequência: {seq3}")
    
    comprimento, lis = encontrar_lis(seq3)
    valida = validar_lis(seq3, lis)
    
    print(f"Comprimento da LIS: {comprimento}")
    print(f"LIS encontrada: {lis}")
    print(f"Válida: {'✓ Sim' if valida else '✗ Não'}")
    print(f"Observação: Em sequência decrescente, LIS tem comprimento 1")
    print()
    
    # === EXEMPLO 4: MÚLTIPLAS LIS ===
    print("EXEMPLO 4: Sequência com múltiplas LIS possíveis")
    print("-" * 80)
    seq4 = [10, 22, 9, 33, 21, 50, 41, 60, 80]
    print(f"Sequência: {seq4}")
    
    comprimento, lis = encontrar_lis(seq4)
    valida = validar_lis(seq4, lis)
    
    print(f"Comprimento da LIS: {comprimento}")
    print(f"LIS encontrada: {lis}")
    print(f"Válida: {'✓ Sim' if valida else '✗ Não'}")
    print(f"Observação: Outras LIS possíveis de mesmo comprimento podem existir")
    print()
    
    # === EXEMPLO 5: SEQUÊNCIA ALEATÓRIA ===
    print("EXEMPLO 5: Sequência aleatória")
    print("-" * 80)
    seq5 = [3, 10, 2, 1, 20, 15, 30, 13]
    print(f"Sequência: {seq5}")
    
    comprimento, lis = encontrar_lis(seq5)
    valida = validar_lis(seq5, lis)
    
    print(f"Comprimento da LIS: {comprimento}")
    print(f"LIS encontrada: {lis}")
    print(f"Válida: {'✓ Sim' if valida else '✗ Não'}")
    print()
    
    # === EXEMPLO 6: EXEMPLO CLÁSSICO ===
    print("EXEMPLO 6: Exemplo clássico de livros de algoritmos")
    print("-" * 80)
    seq6 = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
    print(f"Sequência: {seq6}")
    
    comprimento, lis = encontrar_lis(seq6)
    valida = validar_lis(seq6, lis)
    
    print(f"Comprimento da LIS: {comprimento}")
    print(f"LIS encontrada: {lis}")
    print(f"Válida: {'✓ Sim' if valida else '✗ Não'}")
    print()
    
    # === CASOS ESPECIAIS ===
    print("EXEMPLO 7: Casos especiais")
    print("-" * 80)
    
    # Sequência vazia
    seq_vazia = []
    comp, l = encontrar_lis(seq_vazia)
    print(f"Sequência vazia []: comprimento = {comp}, LIS = {l}")
    
    # Um elemento
    seq_um = [42]
    comp, l = encontrar_lis(seq_um)
    print(f"Um elemento [42]: comprimento = {comp}, LIS = {l}")
    
    # Todos iguais
    seq_iguais = [5, 5, 5, 5]
    comp, l = encontrar_lis(seq_iguais)
    print(f"Todos iguais [5,5,5,5]: comprimento = {comp}, LIS = {l}")
    print()
    
    # === DEMONSTRAÇÃO PASSO A PASSO ===
    print("\n" + "="*80)
    print("DEMONSTRAÇÃO: Como o algoritmo funciona passo a passo")
    print("="*80)
    
    seq_demo = [3, 10, 2, 1, 20, 15, 30, 13]
    imprimir_passo_a_passo(seq_demo)
    
    # === EXPLICAÇÃO DO ALGORITMO ===
    print("="*80)
    print("RESUMO DO ALGORITMO")
    print("="*80)
    print()
    print("CONCEITO PRINCIPAL:")
    print("  - Mantém um array 'tails' onde tails[i] é o MENOR elemento que pode")
    print("    terminar uma subsequência crescente de comprimento i+1")
    print()
    print("VANTAGEM:")
    print("  - Manter o menor elemento possível maximiza as chances de estender")
    print("    a subsequência com elementos futuros")
    print()
    print("PASSOS DO ALGORITMO:")
    print("  1. Para cada elemento da sequência:")
    print("     a) Usa busca binária para encontrar sua posição em 'tails'")
    print("     b) Substitui o elemento nessa posição (se existir)")
    print("     c) Ou adiciona no final (se estende a LIS)")
    print("     d) Registra o predecessor para reconstrução")
    print()
    print("  2. No final:")
    print("     a) O comprimento de 'tails' é o comprimento da LIS")
    print("     b) Reconstrói a LIS seguindo os predecessores")
    print()
    print("COMPLEXIDADE:")
    print("  - Tempo: O(n log n) - n elementos × busca binária log n")
    print("  - Espaço: O(n) - arrays de tamanho n")
    print()
    print("="*80)


if __name__ == "__main__":
    main()
