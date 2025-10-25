# ------------------------------------------------------------
# baseado no artigo:
# "Improvised Divide and Conquer Approach for the LIS Problem"
# ------------------------------------------------------------
# Autor: Lucas Farias e Vicente Gregório (baseado em Seema Rani)
# Divisão e Conquista
# ------------------------------------------------------------

def combine_LIS(left, right):
    """
    combina as subsequências crescentes da metade esquerda e direita.
    A ideia é verificar se podemos unir uma subsequência crescente
    que termina na esquerda com outra que começa na direita.
    """
    best = []
    for i in range(len(left)):
        for j in range(len(right)):
            if left[i] < right[j]:  # condição de crescimento
                combined = left[:i+1] + right[j:]
                if len(combined) > len(best):
                    best = combined
    return best


def LIS_divide_and_conquer(arr):
    """
    encontra a maior subsequência crescente (LIS)
    usando o método de Divisão e Conquista.
    """
    # Caso base: vetor com 1 ou 0 elementos
    if len(arr) <= 1:
        return arr

    # Passo 1: Divisão
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    # Passo 2: Conquista (chamada recursiva)
    lis_left = LIS_divide_and_conquer(left)
    lis_right = LIS_divide_and_conquer(right)

    # Passo 3: Combinação
    lis_cross = combine_LIS(lis_left, lis_right)

    # Retorna a subsequência mais longa
    return max([lis_left, lis_right, lis_cross], key=len)


# ------------------------------------------------------------
# Exemplo de uso prático
# ------------------------------------------------------------
if __name__ == "__main__":
    seq = [3, 10, 2, 1, 20, 4, 6]
    result = LIS_divide_and_conquer(seq)
    print("Sequência original:", seq)
    print("Maior subsequência crescente (LIS):", result)
    print("Comprimento:", len(result))
