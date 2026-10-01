"""
TPC2 - Conversor de Markdown para HTML
Processamento de Linguagens e Compiladores

Elementos suportados (Basic Syntax):
  - Cabeçalhos:      # / ## / ###          -> <h1> / <h2> / <h3>
  - Negrito:         **texto**             -> <b>texto</b>
  - Itálico:         *texto*               -> <i>texto</i>
  - Lista numerada:  1. item  2. item ...  -> <ol><li>...</li></ol>
  - Link:            [texto](url)          -> <a href="url">texto</a>
  - Imagem:          ![alt](url)           -> <img src="url" alt="alt"/>

Uso:
  python3 tpc2.py ficheiro.md          (escreve o HTML no ecrã)
  python3 tpc2.py < ficheiro.md
"""

import re
import sys

# --- Expressões regulares (compiladas uma vez) ---------------------------

# Cabeçalho: 1 a 3 '#' no início da linha, seguidos de espaço e do texto
ER_CABECALHO = re.compile(r'^(#{1,3})\s+(.+?)\s*$')

# Item de lista numerada: número, ponto, espaço, texto
ER_ITEM = re.compile(r'^\s*\d+\.\s+(.*)$')

# Imagem: ![alt](url)  -> tem de ser tratada ANTES do link
ER_IMAGEM = re.compile(r'!\[([^\]]*)\]\(([^)]*)\)')

# Link: [texto](url)
ER_LINK = re.compile(r'\[([^\]]*)\]\(([^)]*)\)')

# Negrito: **texto**  -> tem de ser tratado ANTES do itálico
ER_NEGRITO = re.compile(r'\*\*(.+?)\*\*')

# Itálico: *texto*
ER_ITALICO = re.compile(r'\*(.+?)\*')


def converte_inline(texto):
    """Converte os elementos que aparecem dentro de uma linha."""
    texto = ER_IMAGEM.sub(r'<img src="\2" alt="\1"/>', texto) 
    texto = ER_LINK.sub(r'<a href="\2">\1</a>', texto)
    texto = ER_NEGRITO.sub(r'<b>\1</b>', texto)
    texto = ER_ITALICO.sub(r'<i>\1</i>', texto)
    return texto


def converte_cabecalho(m):
    """Recebe o Match de um cabeçalho e devolve o HTML correspondente."""
    nivel = len(m.group(1))  # número de '#'
    conteudo = converte_inline(m.group(2))
    return f'<h{nivel}>{conteudo}</h{nivel}>'


def md_para_html(md):
    linhas = md.split('\n')
    resultado = []
    dentro_lista = False

    for linha in linhas:
        item = ER_ITEM.match(linha)

        # Se estávamos numa lista e esta linha não é item, fecha a lista
        if dentro_lista and not item:
            resultado.append('</ol>')
            dentro_lista = False

        if item:
            if not dentro_lista:
                resultado.append('<ol>')
                dentro_lista = True
            resultado.append(f'<li>{converte_inline(item.group(1))}</li>')
            continue

        cab = ER_CABECALHO.match(linha)
        if cab:
            resultado.append(converte_cabecalho(cab))
        else:
            resultado.append(converte_inline(linha))

    # Se o texto terminar a meio de uma lista, fecha-a
    if dentro_lista:
        resultado.append('</ol>')
        return '\n'.join(resultado)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8') as f:
            md = f.read()
    else:
        md = sys.stdin.read()
    print(md_para_html(md))


if __name__ == '__main__':
    main()
