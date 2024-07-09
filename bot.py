import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from dotenv import load_dotenv
import os
from logger import logger
from selenium_scraper import SeleniumScraper
import embeds

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Inicializando o bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)
        self.scraper = SeleniumScraper()

    async def setup_hook(self):
        await self.tree.sync()
        logger.debug("Comandos de barra sincronizados")

    async def close(self):
        await super().close()
        self.scraper.close()

client = MyClient(intents=intents)

class ClanButton(discord.ui.Button):
    def __init__(self, label, clan_url):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.clan_url = clan_url

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            clan_details_html = client.scraper.get_clan_details(self.clan_url)
            if clan_details_html:
                embed = embeds.create_clan_details_embed(clan_details_html)
                await interaction.followup.edit_message(interaction.message.id, embed=embed, view=None)
                logger.debug('Informações do clã capturadas e enviadas.')
            else:
                await interaction.followup.edit_message(interaction.message.id, content="Não foi possível capturar os detalhes do clã.", view=None)
        except Exception as e:
            logger.error(f'Erro ao capturar detalhes do clã: {e}')
            await interaction.followup.edit_message(interaction.message.id, content=f"Erro ao capturar detalhes do clã: {e}", view=None)

@client.event
async def on_ready():
    logger.info(f'Bot conectado como {client.user.name}')
    logger.info(f'Bot ID: {client.user.id}')
    logger.info('Comandos disponíveis:')
    for command in client.tree.get_commands():
        logger.info(f'/{command.name} - {command.description}')

@client.tree.command(name="ping", description="Responde com pong!")
async def ping(interaction: discord.Interaction):
    logger.debug(f'Comando /ping recebido de {interaction.user}')
    await interaction.response.send_message("Pong!")
    logger.debug('Resposta enviada: Pong!')

@client.tree.command(name="featured_clans", description="Captura clãs em destaque da página do clã do Crossfire.")
async def featured_clans(interaction: discord.Interaction):
    await interaction.response.send_message("Capturando dados dos clãs em destaque. por favor espere. ⏳ ")
    logger.debug(f'Comando /featured_clans recebido de {interaction.user}')
    clan_url = "http://br.crossfire.z8games.com/clan/home"
    
    try:
        featured_clans = client.scraper.get_featured_clans(clan_url)
        embed = embeds.create_featured_clans_embed(featured_clans)
        await interaction.followup.send(embed=embed)
        logger.debug('Dados dos clãs em destaque capturados e enviados.')
    except Exception as e:
        logger.error(f'Erro ao capturar dados: {e}')
        await interaction.followup.send(f"Erro ao capturar dados: {e}")

@client.tree.command(name="recent_matches", description="Captura partidas recentes da página do clã do Crossfire.")
async def recent_matches(interaction: discord.Interaction):
    await interaction.response.send_message("Capturando dados das partidas recentes, por favor espere. ⏳ ")
    logger.debug(f'Comando /recent_matches recebido de {interaction.user}')
    clan_url = "http://br.crossfire.z8games.com/clan/home"
    
    try:
        recent_matches = client.scraper.get_recent_matches(clan_url)
        embed = embeds.create_recent_matches_embed(recent_matches)
        await interaction.followup.send(embed=embed)
        logger.debug('Dados das partidas recentes capturados e enviados.')
    except Exception as e:
        logger.error(f'Erro ao capturar dados: {e}')
        await interaction.followup.send(f"Erro ao capturar dados: {e}")

@client.tree.command(name="top_clans", description="Captura os melhores clãs do dia da página do clã do Crossfire.")
async def top_clans(interaction: discord.Interaction):
    await interaction.response.send_message("Capturando dados dos melhores clãs do dia, por favor espere. ⏳ ")
    logger.debug(f'Comando /top_clans recebido de {interaction.user}')
    clan_url = "http://br.crossfire.z8games.com/clan/home"
    
    try:
        top_clans = client.scraper.get_top_clans(clan_url)
        embed = embeds.create_top_clans_embed(top_clans)
        await interaction.followup.send(embed=embed)
        logger.debug('Dados dos melhores clãs do dia capturados e enviados.')
    except Exception as e:
        logger.error(f'Erro ao capturar dados: {e}')
        await interaction.followup.send(f"Erro ao capturar dados: {e}")

@client.tree.command(name="ranking", description="Captura o ranking de clãs da página de leaderboard do Crossfire.")
async def ranking(interaction: discord.Interaction):
    await interaction.response.send_message("Capturando dados do ranking de clãs, por favor espere. ⏳ ")
    logger.debug(f'Comando /ranking recebido de {interaction.user}')
    leaderboard_url = "https://br.crossfire.z8games.com/clan/leaderboard"
    
    try:
        ranking = client.scraper.get_ranking_from_leaderboard(leaderboard_url)
        embed = embeds.create_ranking_embed(ranking)
        await interaction.followup.send(embed=embed)
        logger.debug('Dados do ranking de clãs capturados e enviados.')
    except Exception as e:
        logger.error(f'Erro ao capturar dados: {e}')
        await interaction.followup.send(f"Erro ao capturar dados: {e}")

@client.tree.command(name="buscar_clan", description="Busca informações detalhadas de um clã pelo nome.")
async def buscar_clan(interaction: discord.Interaction, nome: str):
    await interaction.response.send_message(f"Buscando informações do clã: {nome}...")
    logger.debug(f'Comando /buscar_clan recebido de {interaction.user}')

    try:
        clan_results = client.scraper.search_clan_by_name(nome)
        if not clan_results:
            await interaction.followup.send(f"Clã {nome} não encontrado.")
            return

        view = View()
        for idx, clan in enumerate(clan_results):
            button = ClanButton(label=clan['name'], clan_url=clan['profile_url'])
            view.add_item(button)

        await interaction.followup.send(content="Selecione um clã:", view=view)
        logger.debug('Botões de seleção de clãs enviados.')

    except Exception as e:
        logger.error(f'Erro ao buscar informações do clã: {e}')
        await interaction.followup.send(f"Erro ao buscar informações do clã: {e}")

@client.tree.command(name="sobre", description="Informações sobre o desenvolvedor.")
async def sobre(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Sobre o Desenvolvedor",
        description=(
            "Olá! Eu sou Marcos, o desenvolvedor deste bot. "
            "Sinta-se à vontade para contribuir ou doar para apoiar meu trabalho.\n\n"
            "[Doações](https://livepix.gg/bigpapa567)\n"
            "[GitHub](https://github.com/msouza10)"
        ),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)
    logger.debug('Comando /sobre executado')

@client.event
async def on_connect():
    logger.debug("Bot conectado ao servidor de Discord")

@client.event
async def on_disconnect():
    logger.debug("Bot desconectado do servidor de Discord")

# Rodando o bot
try:
    logger.debug("Tentando iniciar o bot")
    client.run(TOKEN)
except Exception as e:
    logger.error(f'Erro ao iniciar o bot: {e}')