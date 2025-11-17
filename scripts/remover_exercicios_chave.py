import json
import os

def remover_exercicios_por_palavra_chave(caminho_entrada: str, caminho_saida: str, palavras_chaves: list):
    """
    Lê um arquivo JSON contendo uma lista de objetos e remove aqueles
    cujo campo 'name' contém a palavra-chave (case-insensitive).
    """
    print(f"Iniciando a leitura do arquivo: {caminho_entrada}")

    try:
        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            conteudo = f.read() 

        conteudo = conteudo.strip()
        conteudo = conteudo.replace("```json", "").replace("```", "")
        
        dados = json.loads(conteudo) 

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_entrada}' não foi encontrado.")
        return
    except json.JSONDecodeError as e:
        print(f"Erro: O arquivo '{caminho_entrada}' não é um JSON válido.")
        print(f"Detalhes do erro JSONDecodeError: {e}")
        return
    
    if not isinstance(dados, list):
        print("Erro: O conteúdo do arquivo não é uma lista de objetos JSON.")
        return

    total_original = len(dados)
    
    chave_lower = [chave.lower() for chave in palavras_chaves]
    
    dados_filtrados = [
        objeto for objeto in dados 
        if isinstance(objeto, dict) and 'name' in objeto and all(chave not in objeto['name'].lower() for chave in chave_lower)
    ]
    
    total_filtrado = len(dados_filtrados)
    removidos = total_original - total_filtrado
    
    print(f"Total de objetos originais: {total_original}")
    print(f"Total de objetos removidos: {removidos}")
    print(f"Total de objetos restantes: {total_filtrado}")

    try:
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            json.dump(dados_filtrados, f, indent=4, ensure_ascii=False)
        
        print(f"\nSucesso! O arquivo filtrado foi salvo em: {caminho_saida}")

    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")


# --- Configurações do Script ---
NOME_ARQUIVO_ENTRADA = '../db/exercicios-ptbr-gemini.json'
NOME_ARQUIVO_SAIDA = '../db/exercicios-ptbr-gemini.json'
PALAVRA_A_REMOVER = ['unilateral', ' unilateral ', ' unilaterais', ' unilaterais ', ' unilateral.', ' unilateral,', ' unilaterais.', ' unilaterais,' 'isométrico', ' isométrico ', ' isométricos', ' isométricos ', ' isométrico.', ' isométrico,', ' isométricos.', ' isométricos,', 'isometrico', ' isometrico ', ' isometricos', ' isometricos ', ' isometrico.', ' isometrico,', ' isometricos.', ' isometricos,', 'estático', ' estático ', ' estáticos', ' estáticos ', ' estático.', ' estático,', ' estáticos.', ' estáticos,', 'estatico', ' estatico ', ' estaticos', ' estaticos ', ' estatico.', ' estatico,', ' estaticos.', ' estaticos,' 'contralateral', ' contralateral ', ' contralaterais', ' contralaterais ', ' contralateral.', ' contralateral,', ' contralaterais.', ' contralaterais,' 'kettlebell', 'alongamento', ' alongamento ', ' alongamentos', ' alongamentos ', ' alongamento.', ' alongamento,', ' alongamentos.', ' alongamentos,', 'parede', ' parede ', ' paredes', ' paredes ', ' parede.', ' parede,', ' paredes.', ' paredes,' 'v. 2', ' v. 2 ', ' v2', ' v2 ', 'isometria', ' isometria ', ' isometrias', ' isometrias ', ' isometria.', ' isometria,', ' isometrias.', ' isometrias,', 'estilo', ' estilo ', ' estilos', ' estilos ', ' estilo.', ' estilo,', ' estilos.', ' estilos,', 'variação', ' variação ', ' variações', ' variações ', ' variação.', ' variação,', ' variações.', ' variações,']
# ------------------------------


if __name__ == '__main__':
    remover_exercicios_por_palavra_chave(NOME_ARQUIVO_ENTRADA, NOME_ARQUIVO_SAIDA, PALAVRA_A_REMOVER)