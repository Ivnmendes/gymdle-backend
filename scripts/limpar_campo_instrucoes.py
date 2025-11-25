import json
import os

# --- Configuração ---
# O arquivo que contém as instruções em inglês
ARQUIVO_ENTRADA = '../db/exercicios_traduzidos.json' 
# Novo arquivo para salvar os dados limpos, pronto para tradução
ARQUIVO_SAIDA_LIMPO = '../db/exercicios.json' 
CAMPO_A_REMOVER = 'instructions_en'

def remover_campo(arquivo_entrada, arquivo_saida, campo):
    """Carrega o JSON de entrada, remove o campo especificado de cada objeto e salva."""
    try:
        # 1. Carregar dados
        with open(arquivo_entrada, 'r', encoding='utf8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo de entrada '{arquivo_entrada}' não encontrado.")
        return
    except json.JSONDecodeError:
        print(f"❌ Erro: O arquivo '{arquivo_entrada}' não é um JSON válido.")
        return

    # 2. Processar e remover o campo
    exercicios_removidos = 0
    
    for item in data:
        # item.pop(key, default) remove a chave se ela existir, garantindo que o script não falhe
        if item.pop(campo, None) is not None:
            exercicios_removidos += 1

    # 3. Salvar o resultado
    with open(arquivo_saida, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ Remoção concluída.")
    print(f"Campo '{campo}' removido de {exercicios_removidos} exercícios.")
    print(f"Arquivo salvo em '{ARQUIVO_SAIDA_LIMPO}'.")

# --- Execução ---
if __name__ == '__main__':
    remover_campo(ARQUIVO_ENTRADA, ARQUIVO_SAIDA_LIMPO, CAMPO_A_REMOVER)