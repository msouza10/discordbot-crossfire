# Discord Bot Crossfire

## Descrição

Este é um bot para Discord desenvolvido para capturar e exibir informações detalhadas de clãs do jogo Crossfire. Ele utiliza a biblioteca `discord.py` para interações no Discord, `selenium` para scraping de dados do site do Crossfire e `dotenv` para gerenciamento de variáveis de ambiente.

## Funcionalidades

- **Comando `/ping`**: Responde com "Pong!".
- **Comando `/featured_clans`**: Captura e exibe os clãs em destaque da página do clã do Crossfire.
- **Comando `/recent_matches`**: Captura e exibe as partidas recentes da página do clã do Crossfire.
- **Comando `/top_clans`**: Captura e exibe os melhores clãs do dia da página do clã do Crossfire.
- **Comando `/ranking`**: Captura e exibe o ranking de clãs da página de leaderboard do Crossfire.
- **Comando `/buscar_clan`**: Busca informações detalhadas de um clã pelo nome.
- **Comando `/sobre`**: Exibe informações sobre o desenvolvedor.

## Instalação

1. Clone este repositório:
    ```bash
    git clone https://github.com/seu-usuario/discordbot-crossfire.git
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd discordbot-crossfire
    ```

3. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    ```

4. Ative o ambiente virtual:

    - Windows:
        ```bash
        venv\Scripts\activate
        ```
    - MacOS/Linux:
        ```bash
        source venv/bin/activate
        ```

5. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

6. Crie um arquivo `.env` na raiz do projeto e adicione seu token do bot do Discord:
    ```env
    DISCORD_BOT_TOKEN=seu-token-aqui
    ```

7. Execute o bot:
    ```bash
    python bot.py
    ```

## Utilização

- Adicione o bot ao seu servidor do Discord.
- Utilize os comandos mencionados acima para interagir com o bot e obter informações sobre os clãs do Crossfire.

## Contribuição

Se você deseja contribuir com este projeto, siga estas etapas:

1. Faça um fork deste repositório.
2. Crie um branch para sua feature ou correção:
    ```bash
    git checkout -b minha-feature
    ```
3. Faça commit das suas alterações:
    ```bash
    git commit -m 'Adicionando minha feature'
    ```
4. Faça push para o branch:
    ```bash
    git push origin minha-feature
    ```
5. Abra um Pull Request.

## Contato

- GitHub: [msouza10](https://github.com/msouza10)
- Doações: [LivePix](https://livepix.gg/bigpapa567)

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
