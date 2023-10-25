# AssistenteV3

## Descrição

O Rs3 AssistenteV3 é uma ferramenta desenvolvida por Erick Esser, projetada para servir como assistente em jogos, utilizando técnicas avançadas como Redes Neurais Recorrentes, Reconhecimento Óptico de Caracteres (OCR) e automação para otimizar a experiência do jogador.

## Funcionalidades

- **Reconhecimento Óptico de Caracteres (OCR)**: Permite identificar e interpretar textos dentro do jogo, auxiliando em diversas tarefas.
- **Redes Neurais Recorrentes (RNN)**: Usadas para prever e automatizar ações específicas dentro do jogo.
- **Automação**: Facilita a execução de tarefas repetitivas, proporcionando eficiência e otimização ao jogador.

## Instalação

Para instalar todas as bibliotecas e dependências necessárias:

```bash
pip install torch torchvision torchaudio easyocr keyboard numpy opencv-python Pillow psutil PyGetWindow pyautogui pystray PyYAML win10toast pyzipper plyer

```

## Estrutura do Projeto

- **Class/**: Contém funções relacionadas à obtenção de "vida", "vida do pet" e "oração" usando OCR.
- **Config/**: Hospeda arquivos de configuração que definem coordenadas, teclas e outras informações essenciais.
- **Icon/**: Armazena os ícones usados no projeto.
- **Imagem/**: Hospeda imagens usadas em operações de OCR e possivelmente na interface do usuário.
- **img_return/**: Guarda imagens geradas ou usadas durante a execução.
- **Json/**: Armazena arquivos JSON para definir coordenadas e configurações de teclas.
- **Log/**: Módulo dedicado ao registro de logs, gerenciamento de erros e contato com suporte.
- **Main/**: Ponto de entrada do programa, contendo o principal arquivo de execução.
- **OCR/**: Módulo dedicado ao OCR, interpretando imagens e extraindo informações relevantes.

## Uso

Execute o script `run_main.bat` para iniciar o programa.

## Autoria e Contribuições

Este projeto foi meticulosamente desenvolvido por **Erick Esser**. Feedback são bem-vindos.

## Licença

Por favor, consulte o arquivo `LICENSE` para detalhes completos sobre a licença sob a qual este projeto está distribuído.

---

**Nota**: Para mais detalhes sobre cada arquivo ou módulo, é recomendado revisar o código-fonte ou entrar em contato com o autor.

