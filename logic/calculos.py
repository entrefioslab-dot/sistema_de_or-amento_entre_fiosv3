# -*- coding: utf-8 -*-
"""
Lógica de Cálculos de Orçamento - Entre Fios (V2)
Módulo responsável por realizar todos os cálculos matemáticos e de logística.
COM ALGORITMO INTELIGENTE DE EMPACOTAMENTO QUE UNIFICA PEÇAS INDEPENDENTEMENTE DO FORNECEDOR.
"""

from data.estampas import obter_custo_estampa, calcular_lucro_mao_obra, calcular_custos_fixos
from data.pagamentos import obter_taxa_percentual, obter_num_parcelas


def calcular_pacotes_envio_inteligente(itens):
    pacotes = []
    peso_total = 0

    capacidade_maxima = 10
    for item in itens:
        produto_info = item['produto_info']
        capacidade = produto_info.get('pacote_capacidade', 10)
        if capacidade > capacidade_maxima:
            capacidade_maxima = capacidade

    todas_as_pecas = []
    for item in itens:
        produto_info = item['produto_info']
        peso_unitario = produto_info['peso']

        for _ in range(item['quantidade']):
            todas_as_pecas.append({
                'produto_nome': item['produto_nome'],
                'fornecedor': item['fornecedor'],
                'peso_unitario': peso_unitario,
                'produto_info': produto_info
            })

    pecas_restantes = todas_as_pecas.copy()
    numero_pacote = 1

    while pecas_restantes:
        pacote_atual = {
            'id': numero_pacote,
            'peso': 0,
            'quantidade': 0,
            'itens': []
        }

        while pecas_restantes and pacote_atual['quantidade'] < capacidade_maxima:
            peca = pecas_restantes.pop(0)
            pacote_atual['quantidade'] += 1
            pacote_atual['peso'] += peca['peso_unitario']

            item_existente = None
            for item_pacote in pacote_atual['itens']:
                if (
                    item_pacote['nome'] == peca['produto_nome']
                    and item_pacote['fornecedor'] == peca['fornecedor']
                ):
                    item_existente = item_pacote
                    break

            if item_existente:
                item_existente['quantidade'] += 1
            else:
                pacote_atual['itens'].append({
                    'nome': peca['produto_nome'],
                    'fornecedor': peca['fornecedor'],
                    'quantidade': 1
                })

        pacotes.append(pacote_atual)
        peso_total += pacote_atual['peso']
        numero_pacote += 1

    return pacotes, peso_total


def calcular_resumo_orcamento(itens_selecionados, forma_pagamento):
    itens_calculados = []
    total_quantidade = 0
    custo_total = 0
    valor_venda_base = 0
    lucro_total = 0

    lucro_mao_obra = calcular_lucro_mao_obra()
    custos_fixos_un = calcular_custos_fixos()

    for item in itens_selecionados:
        produto_info = item['produto_info']
        quantidade = item['quantidade']
        total_quantidade += quantidade

        custo_frente = obter_custo_estampa(item['estampa_frente'])
        custo_costas = obter_custo_estampa(item['estampa_costas'])
        custo_estampas_total = custo_frente + custo_costas

        custo_unitario = produto_info['valor'] + custo_estampas_total + custos_fixos_un
        valor_venda_unitario = custo_unitario + lucro_mao_obra

        custo_total_item = custo_unitario * quantidade
        venda_total_item = valor_venda_unitario * quantidade
        lucro_total_item = lucro_mao_obra * quantidade

        itens_calculados.append({
            **item,
            'custo_unitario': custo_unitario,
            'valor_venda_unitario': valor_venda_unitario,
            'custo_total_item': custo_total_item,
            'venda_total_item': venda_total_item,
            'lucro_total_item': lucro_total_item
        })

        custo_total += custo_total_item
        valor_venda_base += venda_total_item
        lucro_total += lucro_total_item

    percentual_desconto = 0
    if total_quantidade >= 100:
        percentual_desconto = 0.15
    elif total_quantidade >= 50:
        percentual_desconto = 0.10
    elif total_quantidade >= 20:
        percentual_desconto = 0.05

    valor_desconto = valor_venda_base * percentual_desconto
    valor_apos_desconto = valor_venda_base - valor_desconto
    lucro_total -= valor_desconto

    taxa_percentual = obter_taxa_percentual(forma_pagamento)
    taxa_decimal = taxa_percentual / 100

    if taxa_decimal < 1:
        valor_final_com_taxa = valor_apos_desconto / (1 - taxa_decimal)
    else:
        valor_final_com_taxa = valor_apos_desconto * (1 + taxa_decimal)

    valor_taxa = valor_final_com_taxa - valor_apos_desconto
    num_parcelas = obter_num_parcelas(forma_pagamento)
    valor_parcela = valor_final_com_taxa / num_parcelas if num_parcelas > 0 else 0
    margem_percentual = (lucro_total / valor_final_com_taxa * 100) if valor_final_com_taxa > 0 else 0

    pacotes, peso_total = calcular_pacotes_envio_inteligente(itens_calculados)

    return {
        'itens': itens_calculados,
        'total_quantidade': total_quantidade,
        'valor_venda_base': valor_venda_base,
        'percentual_desconto': percentual_desconto,
        'valor_desconto': valor_desconto,
        'valor_apos_desconto': valor_apos_desconto,
        'taxa_percentual': taxa_percentual,
        'valor_taxa': valor_taxa,
        'valor_final_com_taxa': valor_final_com_taxa,
        'forma_pagamento': forma_pagamento,
        'num_parcelas': num_parcelas,
        'valor_parcela': valor_parcela,
        'lucro_total': lucro_total,
        'custo_total': custo_total,
        'margem_percentual': margem_percentual,
        'pacotes': pacotes,
        'num_pacotes': len(pacotes),
        'peso_total': peso_total,
    }
