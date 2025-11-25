import json
import os
import google.generativeai as genai
import time

# --- Configuração ---
ARQUIVO_PARA_TRADUZIR = '../db/exercicios_com_instrucoes.json'
ARQUIVO_SAIDA_TRADUZIDO = '../db/exercicios_traduzidos.json'

# Tamanho do lote. Use um valor conservador (20) para o Free Tier
TAMANHO_LOTE = 20 

# Limite diário do Free Tier: 250 requisições (ajuste se seu limite for menor)
LIMITE_DIARIO = 250 

# Chave da API (Lê da variável de ambiente)
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("ERRO: Configure a variável de ambiente 'GOOGLE_API_KEY'.")
    exit()

def traduzir_instrucoes():
    
    # 1. Carregar dados
    try:
        with open(ARQUIVO_PARA_TRADUZIR, 'r', encoding='utf8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {ARQUIVO_PARA_TRADUZIR} não encontrado.")
        return

    # 2. Determinar o progresso e o limite
    # Tentamos descobrir quantos itens já foram traduzidos
    start_index = 0
    
    # Suponha que, se o arquivo traduzido existir, ele contém o progresso.
    # Se você for rodar em vários dias, você deve criar uma lógica de checkpoint.
    
    # Para o primeiro dia, vamos processar o máximo que pudermos.
    
    total_exercicios = len(data)
    total_lotes = (total_exercicios + TAMANHO_LOTE - 1) // TAMANHO_LOTE
    
    print(f"Total de exercícios: {total_exercicios}")
    print(f"Total de lotes (no máximo): {total_lotes}")

    # 3. Instrução Mestra para o Gemini
    SYSTEM_PROMPT = """
    Você é um tradutor especializado em terminologia de fitness. Sua tarefa é traduzir o texto das instruções do inglês para o português.
    Preserve a estrutura de lista (array) e retorne APENAS o array JSON traduzido, sem texto adicional.
    """

    json_config = {"response_mime_type": "application/json"}
    model = genai.GenerativeModel('gemini-2.5-flash', generation_config=json_config)

    # 4. Loop de Processamento (com controle de cota)
    lotes_processados_hoje = 0
    all_results = []
    
    for i in range(0, total_exercicios, TAMANHO_LOTE):
        if lotes_processados_hoje >= LIMITE_DIARIO:
            print("\n❌ LIMITE DIÁRIO ATINGIDO (250 REQUISIÇÕES). Retomando amanhã.")
            break
            
        current_batch = data[i: i + TAMANHO_LOTE]
        numero_lote = (i // TAMANHO_LOTE) + 1
        
        # Criar a carga de trabalho: apenas o exerciseId e as instruções
        # Usamos o 'name' apenas como referência para a IA
        payload = [
            {'exerciseId': item['exerciseId'], 'name': item['name'], 'instructions_en': item['instructions_en']}
            for item in current_batch if item.get('instructions_en')
        ]
        
        if not payload:
            continue # Pula se não houver instruções

        print(f"Processando Lote {numero_lote}/{total_lotes} ({len(payload)} itens)...")
        
        try:
            prompt = f"{SYSTEM_PROMPT}\n\nINSTRUÇÕES A TRADUZIR (JSON):\n{json.dumps(payload, ensure_ascii=False)}"
            
            response = model.generate_content(prompt)
            traduzidos = json.loads(response.text)
            
            lotes_processados_hoje += 1
            
            # 5. Mesclar resultados (necessário para o caso de o Gemini reordenar ou mudar algo)
            # A forma mais simples é remapear os resultados traduzidos.
            
            traducao_map = {item['exerciseId']: item.get('instructions_pt', []) for item in traduzidos}
            
            for item in current_batch:
                item['instructions_pt'] = traducao_map.get(item['exerciseId'], item.get('instructions_en', []))
                all_results.append(item)
            
            # --- SALVAR CHECKPOINT APÓS CADA LOTE (CRUCIAL PARA O FREE TIER) ---
            with open(ARQUIVO_SAIDA_TRADUZIDO, 'w', encoding='utf8') as f:
                json.dump(all_results, f, indent=2, ensure_ascii=False)
                
            print(f"✔️ Lote {numero_lote} salvo. Progresso: {len(all_results)}/{total_exercicios}")
            time.sleep(1) # Pequena pausa para respeitar o limite de 10 requisições/minuto
            
        except Exception as e:
            print(f"❌ Erro no Lote {numero_lote}: {e}")
            print("Tentativa falhou. Retomando no próximo lote...")
            time.sleep(5) # Pausa maior após erro

    print(f"\nProcessamento de {len(all_results)} exercícios concluído.")
    print(f"Total de requisições de API feitas hoje: {lotes_processados_hoje}.")


# Exemplo de execução (Comente ou adapte)
# Se você rodou a consolidação e criou 'exercicios_consolidado.json', execute:
traduzir_instrucoes()