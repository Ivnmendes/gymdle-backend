import json

# --- Configuração ---
ARQUIVO_ORIGINAL_EN = '../db/exercises.json'
ARQUIVO_DESTINO_PT = '../db/exercicios_completos.json'
ARQUIVO_SAIDA_CONSOLIDADO = '../db/exercicios_com_instrucoes.json'

def consolidar_instrucoes(arquivo_en, arquivo_pt, arquivo_saida):
    try:
        # Carregar dados em inglês (com instructions)
        with open(arquivo_en, 'r', encoding='utf8') as f:
            data_en = json.load(f)
        
        # Carregar dados em português (destino)
        with open(arquivo_pt, 'r', encoding='utf8') as f:
            data_pt = json.load(f)
            
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado: {e}")
        return

    # 1. Mapear instruções do JSON original pelo exerciseId
    instructions_map = {item['exerciseId']: item.get('instructions', []) for item in data_en}

    # 2. Adicionar instruções ao JSON de destino
    consolidated_data = []
    for item_pt in data_pt:
        exercise_id = item_pt['exerciseId']
        
        # Pega as instruções mapeadas (ou lista vazia se não encontrar)
        instructions = instructions_map.get(exercise_id, [])
        
        # Adiciona o novo campo
        item_pt['instructions_en'] = instructions
        consolidated_data.append(item_pt)

    # 3. Salvar o resultado
    with open(arquivo_saida, 'w', encoding='utf8') as f:
        json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ Consolidação concluída. {len(consolidated_data)} exercícios salvos em '{ARQUIVO_SAIDA_CONSOLIDADO}'.")


# Exemplo de execução (Comente ou adapte o nome dos arquivos)
consolidar_instrucoes(ARQUIVO_ORIGINAL_EN, ARQUIVO_DESTINO_PT, ARQUIVO_SAIDA_CONSOLIDADO)