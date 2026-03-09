import os
import sys
import pandas as pd
import time

def ler_lista(arquivo):
    """Lê um arquivo .txt contendo uma lista no formato Python e retorna como lista."""
    with open(arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()
    lista = eval(conteudo.split("=")[1].strip())
    return lista

def verificar_books_em_pgms(books, pgms, pasta_src, arquivo_saida, extensao=".cbl"):
    resultados = []
    for book in books:
        encontrado = False
        for pgm in pgms:
            nome_arquivo = pgm + extensao  # concatena extensão apenas para busca
            caminho_modulo = os.path.join(pasta_src, nome_arquivo)
            if not os.path.exists(caminho_modulo):
                print(f"Módulo não encontrado: {nome_arquivo}")
                continue
            with open(caminho_modulo, "r", encoding="utf-8", errors="ignore") as f:
                conteudo = f.read()
                if book in conteudo:
                    # Evita gravar se o resultado for exatamente igual (ex: "CSC00900 - CSC00900")
                    if book != pgm:
                        resultados.append(f"{book} - {pgm}")
                    encontrado = True
        if not encontrado:
            resultados.append(f"{book} - Nenhuma referência encontrada")
    
    # Grava resultados em arquivo de saída TXT
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for linha in resultados:
            f.write(linha + "\n")

    return resultados

def gerar_excel(arquivo_txt, arquivo_excel):
    """Lê o arquivo TXT e gera um Excel com colunas Book e Programa."""
    dados = []
    with open(arquivo_txt, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split(" - ")
            if len(partes) == 2:
                dados.append({"Book": partes[0], "Programa": partes[1]})
    
    df = pd.DataFrame(dados, columns=["Book", "Programa"])
    df.to_excel(arquivo_excel, index=False)

def main():
    inicio = time.time()

    raiz_listas = os.path.join(os.getcwd(), "Listas")
    raiz_modulos = os.path.join(os.getcwd(), "Modulos")
    extensao = ".cbl"
    arquivo_books = os.path.join(raiz_listas, "Lista_Books.txt")
    arquivo_pgms = os.path.join(raiz_listas, "Lista_Pgms.txt")
    pasta_src = os.path.join(raiz_modulos, "SRC")
    arquivo_saida_txt = os.path.join(os.getcwd(), "Resultado_Busca2.txt")
    arquivo_saida_excel = os.path.join(os.getcwd(), "Resultado_Busca2.xlsx")

    books = ler_lista(arquivo_books)
    pgms = ler_lista(arquivo_pgms)

    resultados = verificar_books_em_pgms(books, pgms, pasta_src, arquivo_saida_txt, extensao)
    gerar_excel(arquivo_saida_txt, arquivo_saida_excel)

    fim = time.time()
    tempo_decorrido = fim - inicio

    # Estatísticas
    print("\n=== Estatísticas da execução ===")
    print(f"Quantidade de Books: {len(books)}")
    print(f"Quantidade de Programas: {len(pgms)}")
    print(f"Linhas gravadas em Resultado_Busca.txt: {len(resultados)}")
    print(f"Tempo início: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inicio))}")
    print(f"Tempo final: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fim))}")
    print(f"Tempo decorrido: {tempo_decorrido:.2f} segundos")
    print("Processo concluído. Verifique os arquivos Resultado_Busca2.txt e Resultado_Busca2.xlsx.")

if __name__ == "__main__":
    main()