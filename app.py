# -*- coding: utf-8 -*-
"""
Sistema de Orçamento Entre Fios - Interface Streamlit Completa (V2)
COM ALGORITMO INTELIGENTE DE EMPACOTAMENTO
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from datetime import datetime

# IMPORTS CORRIGIDOS (nomes reais dos módulos)
from data.fornecedores import obter_fornecedores, obter_produtos_fornecedor, obter_produto_info
from data.estampas import obter_custos_estampa
from data.pagamentos import obter_formas_pagamento
from logic.calculos import calcular_resumo_orcamento

# Se você tiver a função de PDF, descomente a linha abaixo:
# from logic.calculos import gerar_proposta_pdf


# --- Configuração da Página ---
st.set_page_config(
    layout="wide",
    page_title="Entre Fios - Orçamentos (V2)",
    initial_sidebar_state="expanded"
)

# --- Estilização Minimalista ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { border-radius: 2px; border: 1px solid #e0e0e0; background-color: #ffffff; color: #333333; }
    .stButton>button:hover { border-color: #8B7355; color: #8B7355; }
    .contact-button { display: inline-flex; align-items: center; justify-content: center; padding: 10px 15px; margin: 5px 0; border: 1px solid #eeeeee; border-radius: 4px; text-decoration: none; color: #555555; font-size: 14px; width: 100%; }
    .contact-button:hover { background-color: #f9f9f9; border-color: #cccccc; color: #000000; }
    .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 5px solid #8B7355; }
    </style>
    """, unsafe_allow_html=True)

# --- Inicialização do Estado ---
if "orcamento_itens" not in st.session_state:
    st.session_state.orcamento_itens = []

# --- Cabeçalho ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.markdown("### Entre Fios")
with col_title:
    st.title("Entre Fios")
    st.caption("Sistema de Gestão de Orçamentos | Versão V2 - Com Empacotamento Inteligente")

st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### Entre Fios Lab")
    st.markdown("---")
    st.markdown(f"""
        <a href="https://wa.me/5511915922431" target="_blank" class="contact-button">
            <img src="https://cdn-icons-png.flaticon.com/16/733/733585.png" style="margin-right:10px; opacity:0.7;"> WhatsApp
        </a>
        <a href="https://www.instagram.com/entrefios.lab/" target="_blank" class="contact-button">
            <img src="https://cdn-icons-png.flaticon.com/16/2111/2111463.png" style="margin-right:10px; opacity:0.7;"> Instagram
        </a>
    """, unsafe_allow_html=True )
    st.markdown("---")
    st.markdown(f"""<div style="font-size: 12px; color: #888888;"><strong>CNPJ:</strong> 53.497.169/0001-65  
<strong>E-mail:</strong> entrefioslab@gmail.com</div>""", unsafe_allow_html=True)
    st.markdown("---")
    with st.expander("Instruções"):
        st.write("1. Selecione os produtos e estampas.")
        st.write("2. Adicione ao orçamento.")
        st.write("3. Escolha a forma de pagamento.")
        st.write("4. Gere o PDF final.")
    st.markdown("---")
    st.info("V2: Empacotamento inteligente que unifica peças de diferentes fornecedores!")

# --- 1. ADIÇÃO DE ITENS ---
st.subheader("1. Adicionar Item")
c1, c2, c3, c4, c5 = st.columns([2, 2, 1.5, 1.5, 1])
with c1: fornecedor = st.selectbox("Fornecedor", obter_fornecedores())
with c2: produto = st.selectbox("Produto", obter_produtos_fornecedor(fornecedor))
with c3: est_f = st.selectbox("Estampa Frente", list(obter_custos_estampa().keys()))
with c4: est_c = st.selectbox("Estampa Costas", list(obter_custos_estampa().keys()))
with c5: qtd = st.number_input("Qtd", min_value=1, value=1)

if st.button("Adicionar ao Orçamento", use_container_width=True):
    p_info = obter_produto_info(fornecedor, produto)
    if p_info:
        st.session_state.orcamento_itens.append({
            'fornecedor': fornecedor, 'produto_nome': produto, 'produto_info': p_info,
            'estampa_frente': est_f, 'estampa_costas': est_c, 'quantidade': qtd,
        })
        st.toast(f"Adicionado: {qtd}x {produto}")

st.divider()

# --- 2. ITENS DO ORÇAMENTO ---
st.subheader("2. Itens do Orçamento")
if not st.session_state.orcamento_itens:
    st.info("Nenhum item no orçamento.")
else:
    df = pd.DataFrame([{
        "Produto": i["produto_nome"], "Frente": i["estampa_frente"],
        "Costas": i["estampa_costas"], "Qtd": i["quantidade"], "Fornecedor": i["fornecedor"]
    } for i in st.session_state.orcamento_itens])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    col_rem1, col_rem2 = st.columns([4, 1])
    with col_rem1:
        idx_rem = st.selectbox(
            "Remover item:",
            range(len(st.session_state.orcamento_itens)), 
            format_func=lambda x: f"{st.session_state.orcamento_itens[x]['quantidade']}x {st.session_state.orcamento_itens[x]['produto_nome']}"
        )
    with col_rem2:
        if st.button("Remover Selecionado", use_container_width=True):
            st.session_state.orcamento_itens.pop(idx_rem)
            st.rerun()

st.divider()

# --- 3. RESUMO DO ORÇAMENTO ---
if st.session_state.orcamento_itens:
    st.subheader("3. Resumo do Orçamento")
    
    col_pag_sel, _ = st.columns([2, 4])
    with col_pag_sel:
        forma_pag = st.selectbox("Forma de Pagamento", obter_formas_pagamento())
    
    resumo = calcular_resumo_orcamento(st.session_state.orcamento_itens, forma_pag)
    
    st.markdown("### Orçamento")
    m1, m2, m3 = st.columns(3)
    m1.metric("Quantidade", f"{resumo['total_quantidade']} peças")
    m2.metric("Valor Unitário (Médio)", f"R$ {resumo['valor_final_com_taxa']/resumo['total_quantidade']:.2f}")
    m3.metric("Valor Total", f"R$ {resumo['valor_final_com_taxa']:.2f}")
    
    # ... (restante do seu código segue igual)

# ⚠️ PDF: se não existir gerar_proposta_pdf, comente esse bloco para não quebrar
