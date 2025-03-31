# Criador de Layouts de Teclado

Projeto da disciplina de Introdução à Programação da pós-graduação.

## Sobre o Projeto
Esta aplicação auxilia na criação de layouts de teclado otimizados através da análise de entradas de documentos de texto. Além disso, aplica otimizações inspiradas em layouts alternativos, como DVORAK e COLEMAK-DH.

## Público-Alvo
Destinado a usuários que digitam por longos períodos, especialmente aqueles que trabalham com múltiplos idiomas ou linguagens de programação. O projeto busca fornecer layouts personalizados para melhorar a eficiência da digitação.

## Tecnologias Utilizadas
- Python 3
- JSON para armazenamento de dados

## Estrutura do Projeto
- `inputs.json` → Armazena os textos analisados e suas estatísticas
- `layout.json` → Contém a matriz de caracteres do layout gerado
- `main.py` → Ponto de entrada da aplicação
- `classes/` → Contém as classes responsáveis pelo processamento

## Como Executar o Projeto
### Pré-requisitos
- Python 3 instalado
- Criar e ativar um ambiente virtual (Dentro da pasta backend)
  ```sh
  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  venv\Scripts\activate     # Windows
  ```

### Executando o Programa (Dentro da pasta backend)
	```sh
	univorn main:app --reload
	```

## Estrutura das Classes
### `TextInput`
- `process_text()`: Analisa o texto e conta caracteres, bigramas e trigramas.
- `to_dict()`: Retorna os contadores em formato de dicionário.

### `InputStorage`
- `load_inputs()`: Carrega os inputs salvos.
- `save_inputs()`: Salva os inputs no arquivo JSON.
- `get_inputs()`: Retorna os dados dos inputs.

### `LayoutStorage`
- `load_layout()`: Carrega o layout salvo.
- `save_layout()`: Salva o layout atualizado.
- `update_matrix()`: Atualiza a matriz do layout com base nos dados processados.

