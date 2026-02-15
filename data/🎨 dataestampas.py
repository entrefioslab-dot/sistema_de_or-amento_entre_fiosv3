🎨 data/estampas.py
# -*- coding: utf-8 -*-
"""
Dados de Estampas e Custos de Produção
Módulo que centraliza custos de estampa DTF e custos fixos de produção.
"""

CUSTOS_ESTAMPA = {
    'Nenhum': 0.00,
    'A8': 0.20,
    'A6': 0.79,
    'A5': 1.86,
    'A4': 3.71,
    'A3': 8.67,
    'A2': 26.00
}

CUSTOS_PRODUCAO = {
    'Eletricidade': 0.60,
    'Mão de Obra': 3.00,
    'Insumos': 0.50,
    'Marketing': 1.50,
    'Lucro': 10.00
}

def obter_custos_estampa():
    """Retorna dicionário com custos de estampa."""
    return CUSTOS_ESTAMPA.copy()

def obter_custo_estampa(formato):
    """Retorna custo unitário de um formato de estampa."""
    return CUSTOS_ESTAMPA.get(formato, 0.00)

def obter_custos_producao():
    """Retorna dicionário com custos de produção."""
    return CUSTOS_PRODUCAO.copy()

def calcular_lucro_mao_obra():
    """Retorna a soma de Lucro + Mão de Obra."""
    return CUSTOS_PRODUCAO['Lucro'] + CUSTOS_PRODUCAO['Mão de Obra']

def calcular_custos_fixos():
    """Retorna a soma de custos fixos (Eletricidade + Insumos + Marketing)."""
    return CUSTOS_PRODUCAO['Eletricidade'] + CUSTOS_PRODUCAO['Insumos'] + CUSTOS_PRODUCAO['Marketing']
