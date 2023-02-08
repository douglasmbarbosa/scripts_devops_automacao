def processDict(dict):
    dict_response = [] # Array que conterá a resposta no final

    """
        Para que este algoritmo funcione, o dicionário deve estar ordenado de acordo com o valor de suas chaves,
        porém, naturalmente, dicionários em python não podem ser ordenados, o que faço nas 3 linhas abaixo é criar 
        uma estrutura equivalente à um dicionario com N chaves, do tipo [(key1, value1), (key2, value2), ..., (keyN, valueN)] (uma lista de duplas), 
        que por sua vez é ordenável.
    """
    false_dict_sort = list(dict.items()) # Obtém a estrutura mencionada acima a partir do dicionário
    false_dict_sort.sort(key=lambda e: e[1]) # Ordenando a estrutura de acordo com o valor das chaves

    """
        A função abaixo é recursiva e responsável por encontrar as chaves que possuem valores iguais
        e retorná-las em uma lista, porém é necessário que o dicionário esteja ordenando
        e por isso a estrutura criada acima é necessária
        
        :param index: indice em false_dict do valor à ser comparado
        :param false_dict: estrutura equivalente ao dicionária obtida acima na variável false_dict_sort
    """

    def getDuplicateValue(index, false_dict):

            if index + 1 < len(false_dict) and false_dict[index][1] == false_dict[index + 1][1]:
                return [false_dict[index][0]] + getDuplicateValue(index + 1, false_dict)
            else:
                return [false_dict[index][0]]

    i = 0
    while i < len(false_dict_sort):
        keys_list = getDuplicateValue(i, false_dict_sort) # retorna uma lista com as chaves que possuem valores iguais
        dict_response.append((keys_list, false_dict_sort[i][1])) # adiciona uma dupla com a lista de chaves (keys_list)
                                                                 # e o valor que essas chaves possuem em dict_response
        i += len(keys_list) #Incrementa i com o tamanho de keys

    return dict_response