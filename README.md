# Renderização de Modelos BYU com OpenGL e Pygame

Este projeto implementa um renderizador de modelos 3D no formato BYU usando OpenGL e Pygame. O programa permite a visualização de modelos 3D com iluminação, materiais e controles de câmera interativos.

## Requisitos

Antes de executar o projeto, certifique-se de ter instalado os seguintes pacotes:

- **Python 3.x**
- **Pygame**
- **PyOpenGL**
- **NumPy**

Para instalar as dependências, execute:

```bash
pip install pygame PyOpenGL numpy
```

## Como Executar

1. Coloque o arquivo do modelo BYU na pasta `objects` e ajuste o caminho do arquivo na variável `byu_file`.
2. Execute o script com:

```bash
python main.py
```

## Controles

### Movimentação da Câmera

- `W` - Move para frente
- `S` - Move para trás
- `A` - Move para a esquerda
- `D` - Move para a direita
- `Q` - Move para cima
- `E` - Move para baixo

### Rotação da Câmera

- Use o **mouse** para girar a câmera.

## Estrutura do Projeto

```plaintext
/
├── main.py  # Arquivo principal que carrega e renderiza o modelo 3D
├── objects/  # Pasta contendo os modelos BYU a serem renderizados
└── README.md  # Documentação do projeto
```

## Funcionalidades

✅ Carregamento de arquivos BYU.
✅ Renderização com OpenGL.
✅ Iluminação e materiais configuráveis.
✅ Controles de câmera interativos.

## Possíveis Melhorias

- 🔹 Suporte a outros formatos de arquivo.
- 🔹 Interface para seleção do modelo.
- 🔹 Sombras dinâmicas e shaders.


