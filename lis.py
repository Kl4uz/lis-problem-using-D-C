from typing import List, Tuple
def encontrar_lis(sequencia: List[int]) -> Tuple[int, List[int]]:
    import bisect
    if not sequencia:
        return 0, []
    n = len(sequencia)
    tails = []
    predecessor = [-1] * n 
    indices_tails = [0] * n 
    
    for i in range(n):
        elemento_atual = sequencia[i]        
        posicao = bisect.bisect_left(tails, elemento_atual)
        
        if posicao > 0:
            for j in range(i - 1, -1, -1):
                if (indices_tails[j] == posicao - 1 and 
                    sequencia[j] < elemento_atual):
                    predecessor[i] = j
                    break
                
        if posicao < len(tails):
            tails[posicao] = elemento_atual
        else:
            tails.append(elemento_atual)
        
        indices_tails[i] = posicao
    
    comprimento_lis = len(tails)      
    ultimo_indice = -1
    for i in range(n - 1, -1, -1):
        if indices_tails[i] == comprimento_lis - 1:
            ultimo_indice = i
            break

    lis = []
    indice_atual = ultimo_indice
    
    while indice_atual != -1:
        lis.append(sequencia[indice_atual])
        indice_atual = predecessor[indice_atual]
    
    lis.reverse()   
    return comprimento_lis, lis