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
        modulos_encontrados = []
        for pgm in pgms:
            nome_modulo = pgm + extensao
            caminho_modulo = os.path.join(pasta_src, nome_modulo)
            if not os.path.exists(caminho_modulo):
                print(f"Modulo não encontrado: {nome_modulo}")
                continue
            with open(caminho_modulo, "r", encoding="utf-8", errors="ignore") as f:
                conteudo = f.read()
                if book in conteudo:
                    if pgm != book:
                        modulos_encontrados.append(pgm)
        if modulos_encontrados:
            resultados.append(f"{book} - {', '.join(modulos_encontrados)}")
        else:
            resultados.append(f"{book} - Nenhuma referencia encontrada")
    
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for linha in resultados:
            f.write(linha + "\n")
    return resultados

def gerar_excel(arquivo_txt, arquivo_excel):
    """Lê o arquivo de resultados e gera um Excel com colunas Book e Programa."""
    dados = []
    with open(arquivo_txt, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split(" - ")
            if len(partes) == 2:
                book, programas = partes
                dados.append([book, programas])
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
    arquivo_saida = os.path.join(os.getcwd(), "Resultado_Busca.txt")
    arquivo_excel = os.path.join(os.getcwd(), "Resultado_Busca.xlsx")

    if len(sys.argv) == 4:
        raiz_listas = sys.argv[1]
        raiz_modulos = sys.argv[2]
        extensao = sys.argv[3]
        arquivo_books = os.path.join(raiz_listas, "Lista_Books.txt")
        arquivo_pgms = os.path.join(raiz_listas, "Lista_Pgms.txt")
        pasta_src = os.path.join(raiz_modulos, "SRC")
        arquivo_saida = os.path.join(os.getcwd(), "Resultado_Busca.txt")
        arquivo_excel = os.path.join(os.getcwd(), "Resultado_Busca.xlsx")
    elif len(sys.argv) != 1:
        print("Uso: python busca_books_pgms.py <caminho_listas> <caminho_modulos> <extensao>")
        sys.exit(1)

    books = ler_lista(arquivo_books)
    pgms = ler_lista(arquivo_pgms)

    resultados = verificar_books_em_pgms(books, pgms, pasta_src, arquivo_saida, extensao)
    gerar_excel(arquivo_saida, arquivo_excel)

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
    print(f"\nProcesso concluído. Verifique os arquivos {arquivo_saida} e {arquivo_excel}.")

if __name__ == "__main__":
    main()