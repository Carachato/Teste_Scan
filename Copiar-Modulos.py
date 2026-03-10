import os
import time
import shutil
from datetime import timedelta

def ler_lista(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()
        #print(f"conteudo: {conteudo}")
    lista = eval(conteudo.split("=")[1].strip())
    return lista

def limpar_pasta(pasta_destino):
    """Remove todo o conteúdo da pasta destino antes da cópia."""
    if os.path.exists(pasta_destino):
        for item in os.listdir(pasta_destino):
            caminho_item = os.path.join(pasta_destino, item)
            try:
                if os.path.isfile(caminho_item) or os.path.islink(caminho_item):
                    os.remove(caminho_item)
                elif os.path.isdir(caminho_item):
                    shutil.rmtree(caminho_item)
            except Exception as e:
                print(f"Não foi possível remover {caminho_item}: {e}")
    else:
        os.makedirs(pasta_destino)

def copiar_arquivos(pgms, pasta_src_origem, pasta_src_destino, extensao, descricao):
    """Rotina dedicada para copiar arquivos com base na lista e extensão."""
    copiados = 0
    nao_encontrados = 0

    # Limpa a pasta destino antes de copiar
    limpar_pasta(pasta_src_destino)

    for nome in pgms:
        arquivo_origem = os.path.join(pasta_src_origem, nome + extensao)
        arquivo_destino = os.path.join(pasta_src_destino, nome + extensao)

        try:
            if os.path.exists(arquivo_origem):
                shutil.copy2(arquivo_origem, arquivo_destino)
                #print(f"Copiado: {arquivo_origem} -> {arquivo_destino}")
                copiados += 1
            else:
                #print(f"Arquivo não encontrado: {arquivo_origem}")
                nao_encontrados += 1
        except PermissionError:
            #print(f"Arquivo em uso, não foi possível copiar: {arquivo_origem}")
            nao_encontrados += 1

    # Estatísticas específicas do cenário
    print(f"\n=== Estatísticas ({descricao}) ===")
    print(f"Quantidade de itens lidos: {len(pgms)}")
    print(f"Copiados: {copiados}")
    print(f"Não encontrados: {nao_encontrados}")

    return copiados, nao_encontrados

def main():
    inicio = time.time()

    raiz_listas = os.path.join(os.getcwd(), "Listas")
    raiz_origem = os.path.join(os.getcwd(), "Modulos")
    raiz_destino = os.path.join(os.getcwd(), "Cenario_Novo")
    
    # Exemplo 1: copiando programas
    lista_pgms = os.path.join(raiz_listas, "Lista_Pgms.txt")
    pasta_src_origem = os.path.join(raiz_origem, "SRC")
    pasta_src_destino = os.path.join(raiz_destino, "SRC")
    extensao = ".cbl"

    pgms = ler_lista(lista_pgms)
    copiar_arquivos(pgms, pasta_src_origem, pasta_src_destino, extensao, "Exemplo 1: Programas")

    # Exemplo 2: copiando books
    lista_books = os.path.join(raiz_listas, "Lista_Books.txt")
    pasta_books_origem = os.path.join(raiz_origem, "CPY")
    pasta_books_destino = os.path.join(raiz_destino, "CPY")
    extensao_books = ".cpy"

    books = ler_lista(lista_books)
    copiar_arquivos(books, pasta_books_origem, pasta_books_destino, extensao_books, "Exemplo 2: Books")

    fim = time.time()
    tempo_decorrido = fim - inicio
    tempo_formatado = str(timedelta(seconds=int(tempo_decorrido)))

    # Estatísticas gerais
    print("\n=== Estatísticas gerais da execução ===")
    print(f"Tempo início: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inicio))}")
    print(f"Tempo final: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fim))}")
    print(f"Tempo decorrido: {tempo_formatado}")

if __name__ == "__main__":
    main()
