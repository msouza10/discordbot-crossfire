import discord
from bs4 import BeautifulSoup

def create_featured_clans_embed(clans):
    embed = discord.Embed(
        title="🌟 Clãs em Destaque 🌟", 
        color=discord.Color.blue(),
        description="Aqui estão os clãs que mais se destacaram recentemente!"
    )
    for clan in clans:
        embed.add_field(
            name=clan['name'], 
            value=f"**Pontos**: {clan['points']}", 
            inline=False
        )
    embed.set_footer(text="Atualizado diariamente")
    embed.timestamp = discord.utils.utcnow()
    return embed

def create_recent_matches_embed(matches):
    embed = discord.Embed(
        title="⚔️ Partidas Recentes ⚔️", 
        color=discord.Color.green(),
        description="Confira os resultados das últimas batalhas!"
    )
    for match in matches:
        embed.add_field(
            name=match['date'], 
            value=f"{match['clan1']['name']} {match['clan1']['score']} VS {match['clan2']['score']} {match['clan2']['name']}", 
            inline=False
        )
    embed.set_footer(text="Resultados atualizados em tempo real")
    embed.timestamp = discord.utils.utcnow()
    return embed

def create_top_clans_embed(clans):
    embed = discord.Embed(
        title="🏆 Melhores Clãs do Dia 🏆", 
        color=discord.Color.purple(),
        description="Veja os clãs que lideram o ranking hoje!"
    )
    for clan in clans:
        embed.add_field(
            name=clan['name'], 
            value=f"**Pontos**: {clan['points']}", 
            inline=False
        )
    embed.set_footer(text="Atualizado diariamente")
    embed.timestamp = discord.utils.utcnow()
    return embed

def create_ranking_embed(ranking):
    embed = discord.Embed(
        title="📊 Ranking de Clãs 📊", 
        color=discord.Color.gold(),
        description="Acompanhe a posição dos clãs no ranking!"
    )
    for clan in ranking:
        embed.add_field(
            name=f"{clan['position']} - {clan['name']}",
            value=(
                f"**Líder**: {clan['leader']}\\n"
                f"**Pontos**: {clan['points']}\\n"
                f"[Perfil do Clã]({clan.get('profile_url', '#')})"
            ),
            inline=False
        )
    embed.set_footer(text="Atualizado semanalmente")
    embed.timestamp = discord.utils.utcnow()
    return embed

def create_clan_details_embed(clan_details):
    embed = discord.Embed(
        title=f"Detalhes do Clã: {clan_details['name']}",
        description=clan_details['description'],
        color=discord.Color.blue()
    )
    embed.add_field(name="Líder", value=clan_details['leader'], inline=True)
    embed.add_field(name="Data de Criação", value=clan_details['creation_date'], inline=True)
    embed.add_field(name="Pontos", value=clan_details['points'], inline=True)
    embed.add_field(name="Rank", value=clan_details['rank'], inline=True)
    embed.add_field(name="Taxa de Vitórias", value=clan_details['win_rate'], inline=True)
    embed.add_field(name="Vitórias", value=clan_details['win_count'], inline=True)
    embed.add_field(name="Derrotas", value=clan_details['loss_count'], inline=True)
    embed.add_field(name="Empates", value=clan_details['draw_count'], inline=True)
    embed.add_field(name="URL do Perfil", value=f"[Link]({clan_details['profile_url']})", inline=True)

    if clan_details['recent_matches']:
        matches_description = "\\n".join([
            f"{match['date']} - {match['result']} - {clan_details['name']} vs {match['opponent_clan']} ({match['score'].replace('\\n', '')}) - no Mapa {match['map_name']}"
            for match in clan_details['recent_matches']
        ])
        embed.add_field(name="Partidas Recentes", value=matches_description, inline=False)

    embed.set_footer(text="Informações detalhadas do clã")
    embed.timestamp = discord.utils.utcnow()
    return embed