# Projeto de Regressão Linear Interativa com Gradiente Descendente

## Introdução
Este projeto é uma aplicação interativa desenvolvida em Python utilizando a biblioteca Pygame para visualização e ajuste de uma reta de regressão linear sobre pontos definidos pelo usuário. O ajuste é feito por métodos de Gradiente Descendente (GD) e Gradiente Descendente Estocástico (SGD), permitindo observar a convergência da reta em tempo real.

## Estrutura do Projeto
O projeto é composto pelos seguintes arquivos principais:

- `main.py`: Interface gráfica, controle de eventos, desenho dos pontos e da reta.
- `objects.py`: Define as classes principais do projeto:
  - `Button`: Botão interativo para a interface.
  - `RegressionLine`: Implementa a lógica de regressão linear e atualização dos coeficientes via GD/SGD.
### Bibliotecas Utilizadas
- `pygame`: Para interface gráfica e manipulação de eventos.
- `random`: Para seleção aleatória de pontos no SGD.
- `sys`: Para controle de encerramento da aplicação.

## Explicação Técnica

### Fluxo Geral
1. O usuário clica na tela para adicionar pontos.
2. Ao clicar em "Começar", a reta de regressão começa a ser ajustada usando GD ou SGD.
3. O usuário pode alternar entre GD e SGD, ou limpar os pontos.
4. A reta é desenhada em tempo real, mostrando a convergência.

### Classes Principais

#### Classe `RegressionLine`
```python
class RegressionLine:
    def __init__(self, m=0.0, b=0.0, learning_rate=1e-2):
        self.m = m
        self.b = b
        self.learning_rate = learning_rate
    ...
    def update(self, points, method="GD"):
        # Normaliza os dados
        # Atualiza m e b via GD ou SGD
        # Desnormaliza os coeficientes para uso na tela
```
- Os coeficientes são aprendidos no espaço normalizado, mas são desnormalizados para desenhar a reta corretamente na tela:
```python
self.m_real = self.m * (max_y / max_x)
self.b_real = self.b * max_y
```

#### Classe `Button`
```python
class Button:
    def __init__(self, rect, text, font, ...):
        ...
    def draw(self, screen):
        ...
    def verify_click(self, event):
        ...
```
- Permite criar botões interativos para limpar pontos, alternar método e iniciar a regressão.

#### Desenho da Reta
No `main.py`, a reta é desenhada usando os coeficientes desnormalizados:
```python
m = getattr(regression_line, 'm_real', regression_line.m)
b = getattr(regression_line, 'b_real', regression_line.b)
```

## Instrução de Compilação e Execução

1. **Pré-requisitos:**
   1.1 Python 3.x instalado
   1.2 Clone ou baixe esse repositório
   1.3 Dentro do diretório, rode comande:
     ```bash
     pip install -r ./requirements.txt
     ```
     > O comando instala as bibliotecas necessárias (nesse caso, apenas o Pygame).

2. **Execução:**
   - No terminal, navegue até a pasta do projeto e execute:
     ```bash
     python ./main.py
     ```

## Instrução de Uso

- **Adicionar pontos:** Clique na área gráfica para adicionar pontos.
- **Começar regressão:** Clique no botão "Começar" para iniciar o ajuste da reta.
- **Alternar método:** Clique no botão "GD"/"SGD" para alternar entre Gradiente Descendente e Gradiente Descendente Estocástico.
- **Limpar pontos:** Clique em "Limpar pontos" para remover todos os pontos e resetar a reta.
- **Visualização:** A reta azul será ajustada em tempo real conforme o método escolhido.

---

Este projeto é ideal para fins didáticos, permitindo visualizar o funcionamento do gradiente descendente na prática e a diferença entre GD e SGD.

## Autor
Miguel Filippo Rocha Calhabeu - Bacharelado de Sistemas de Informação - ICMC USP
