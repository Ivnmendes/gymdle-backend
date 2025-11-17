import json
import os
import google.generativeai as genai
import math
import time
import concurrent.futures

# --- 1. Configuração ---

# Tente carregar a chave de API do ambiente.
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("ERRO: A variável de ambiente 'GOOGLE_API_KEY' não foi definida.")
    print("Execute 'export GOOGLE_API_KEY=\"SUA_CHAVE_AQUI\"' no seu terminal.")
    exit()

# Quantos lotes processar em paralelo.
# 5 é um bom começo para um plano pago. Aumente se quiser mais velocidade.
MAX_WORKERS = 5

# Nome dos seus arquivos
ARQUIVO_ENTRADA = "../db/exercicios-ptbr-gemini.json"
ARQUIVO_SAIDA = "../db/exercicios_completos.json"
ARQUIVO_ERROS = "../db/lotes_com_erro.json"

# Tamanho do lote. Com um plano pago, 50 é um tamanho seguro e eficiente.
TAMANHO_LOTE = 50

# Instrução mestra para a API (JÁ ATUALIZADA)
MASTER_PROMPT = """
Você é um assistente de processamento de dados especialista em ciência do exercício.
Sua tarefa é receber um array de objetos JSON e adicionar TRÊS novos campos a cada objeto: `tipo`, `pegada` e `popularidade`.

REGRAS DE CLASSIFICAÇÃO:

1.  Campo `tipo`:
    * `"push"`: Exercícios de "empurrar" (ex: supinos, desenvolvimentos, extensões de tríceps, elevação lateral, agachamento, leg press, extensão de quadríceps).
    * `"pull"`: Exercícios de "puxar" (ex: remadas, puxadas, roscas de bíceps, flexão de posterior, levantamento terra, encolhimento).
    * `"core"`: Exercícios focados no abdômen ou lombar (ex: pranchas, abdominais, rotação russa).
    * `"outro"`: Se não se encaixar claramente (ex: panturrilhas, exercícios de mobilidade).

2.  Campo `pegada`: (Baseado principalmente no campo `name`)
    * `"neutra"`: Palmas voltadas uma para a outra (ex: "martelo", "pegada neutra").
    * `"supinada"`: Palmas voltadas para cima/frente (ex: "rosca direta", "barra W", "pegada supinada").
    * `"pronada"`: Palmas voltadas para baixo/trás (ex: "rosca inversa", "pegada pronada", "pull down pronado").
    * `"nenhuma"`: Para exercícios onde a pegada não é relevante ou aplicável (ex: agachamento, leg press, abdominais, elevação de panturrilha).

3.  Campo `popularidade`: (Baseado no quão comum o exercício é)
    * `"alta"`: Exercícios fundamentais e extremamente comuns (ex: supino reto, agachamento livre, levantamento terra, rosca direta, pull-up).
    * `"media"`: Exercícios auxiliares populares (ex: rosca martelo, elevação lateral, tríceps corda, leg press, remada cavalinho, elevação pélvica).
    * `"baixa"`: Exercícios muito específicos, variações raras ou pouco conhecidos (ex: rosca zottman, sissy squat, drag curl, jefferson squat).

FORMATO DE SAÍDA:
Retorne APENAS o array JSON modificado, sem nenhum texto, explicação ou markdown.
"""

# Configuração do modelo (use 'models/gemini-2.5-flash' para velocidade)
generation_config = {
    "response_mime_type": "application/json",
}
# Usamos o 2.5-flash para melhor velocidade no plano pago
model = genai.GenerativeModel('models/gemini-2.5-flash',
                              generation_config=generation_config)

# --- 2. Lógica do Script ---

def carregar_dados(arquivo):
    """Carrega os dados do arquivo JSON de entrada."""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERRO: Arquivo de entrada '{arquivo}' não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"ERRO: O arquivo '{arquivo}' não contém um JSON válido.")
        return None

def salvar_dados(dados, arquivo):
    """Salva os dados processados no arquivo JSON de saída."""
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def processar_lote_api(lote_atual, numero_lote):
    """
    Função que envia UM lote para a API.
    Esta função será executada em paralelo.
    """
    print(f"Iniciando processamento do lote {numero_lote}...")
    try:
        # Converte o lote para uma string JSON
        lote_json_str = json.dumps(lote_atual, indent=2, ensure_ascii=False)
        
        # Constrói o prompt final para a API
        prompt_final = f"{MASTER_PROMPT}\n\n**DADOS DE ENTRADA:**\n{lote_json_str}"
        
        # Envia para a API
        response = model.generate_content(prompt_final)
        
        # A API deve retornar uma string JSON que precisa ser parseada
        resposta_json = response.text
        lote_processado = json.loads(resposta_json)
        
        print(f"Lote {numero_lote} processado COM SUCESSO.")
        # Retorna o status e os dados
        return (numero_lote, "sucesso", lote_processado)

    except Exception as e:
        # Se falhar (ex: 504 Timeout), tentamos uma vez
        if "504" in str(e):
             print(f"AVISO: Lote {numero_lote} deu Timeout (504). Tentando novamente...")
             time.sleep(5) # Pausa antes de tentar de novo
             # Tente novamente
             response = model.generate_content(prompt_final)
             resposta_json = response.text
             lote_processado = json.loads(resposta_json)
             print(f"Lote {numero_lote} processado COM SUCESSO (na 2ª tentativa).")
             return (numero_lote, "sucesso", lote_processado)

        print(f"ERRO no lote {numero_lote}: {e}")
        # Retorna o status e o lote original (que falhou)
        return (numero_lote, "erro", lote_atual)

def processar_em_paralelo():
    """Função principal que gerencia o processamento paralelo."""
    
    # Carrega os dados
    todos_exercicios = carregar_dados(ARQUIVO_ENTRADA)
    if not todos_exercicios:
        return

    print(f"Total de {len(todos_exercicios)} exercícios carregados.")

    # Cria a lista de todos os lotes
    lista_de_lotes = [
        todos_exercicios[i : i + TAMANHO_LOTE]
        for i in range(0, len(todos_exercicios), TAMANHO_LOTE)
    ]
    
    total_lotes = len(lista_de_lotes)
    print(f"Dividido em {total_lotes} lotes de {TAMANHO_LOTE} exercícios.")
    print(f"Iniciando processamento paralelo com {MAX_WORKERS} workers...\n")

    # Listas para guardar resultados
    resultados_brutos = [] # Guarda (numero_lote, status, dados)

    # Executa em paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i, lote in enumerate(lista_de_lotes):
            numero_lote = i + 1
            futures.append(
                executor.submit(processar_lote_api, lote, numero_lote)
            )

        for future in concurrent.futures.as_completed(futures):
            resultados_brutos.append(future.result())
    
    print("\nProcessamento paralelo concluído. Organizando resultados...")

    # Ordena os resultados pela ordem original
    resultados_brutos.sort(key=lambda x: x[0])

    # Separa os sucessos dos erros
    dados_processados = []
    lotes_com_erro = []
    
    for numero_lote, status, dados in resultados_brutos:
        if status == "sucesso":
            dados_processados.extend(dados)
        else:
            lotes_com_erro.append(dados)

    # --- 3. Finalização ---
    
    if dados_processados:
        salvar_dados(dados_processados, ARQUIVO_SAIDA)
        print(f"\nSucesso! {len(dados_processados)} exercícios processados.")
        print(f"Resultados salvos em '{ARQUIVO_SAIDA}'.")

    if lotes_com_erro:
        lotes_falhos_flat = [item for sublist in lotes_com_erro for item in sublist]
        salvar_dados(lotes_falhos_flat, ARQUIVO_ERROS)
        print(f"\n{len(lotes_falhos_flat)} exercícios não puderam ser processados.")
        print(f"Os lotes com erro foram salvos em '{ARQUIVO_ERROS}' para revisão.")
    
    print("\nScript finalizado.")

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    start_time = time.time()
    processar_em_paralelo()
    end_time = time.time()
    print(f"Tempo total de execução: {end_time - start_time:.2f} segundos.")