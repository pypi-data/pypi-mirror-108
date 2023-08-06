# -*- coding: utf-8 -*-
"""
Created on Wed May 12 19:56:10 2021

@author: rodri
"""
import numpy as np

# FUNÇÃO: numpy_convert 
# Função para testar (e converter se necessário) listas de python em arrays numpy
def numpy_convert(array):
    '''
    Argumentos:
    ----------
    array - lista de valores a ser validada
    '''
    if isinstance(array, list):
        array = np.array(array)
    return array


# FUNÇÃO: number_to_string 
# Converte um array em uma string compatível com a linguagem Latex
def number_to_string(array):
    '''
    Argumentos:
    ----------
    array: numpy.array contendo os vetores que será convertido em string
    '''      
    rounded = (round(x,4) for x in array)
    if array.dtype == np.float64:
        # retorna as duas primeiras casas decimais se forem valores decimais
        return ('%.2f' % val if str(val)[-2:] != '.0' else '%d' % val for val in rounded)
    else:
        return map(str, rounded)



