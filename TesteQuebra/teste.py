import pandas as pd

# Lê a planilha sem cabeçalhos (ou com cabeçalhos irrelevantes)
df = pd.read_excel("entrada.xlsm", header=0)  # header=0 se tiver cabeçalho na primeira linha

linhas_expandidas = []

for _, linha in df.iterrows():
    # Coluna E é índice 4 (A=0, B=1, C=2, D=3, E=4)
    valores_coluna_e = str(linha.iloc[2]).split(",")
    
    for valor in valores_coluna_e:
        nova_linha = linha.copy()
        nova_linha.iloc[2] = valor.strip()
        linhas_expandidas.append(nova_linha)

df_resultado = pd.DataFrame(linhas_expandidas)
df_resultado.to_excel("resultado.xlsx", index=False)

print("Processamento concluído! Arquivo 'resultado.xlsx' gerado.")
