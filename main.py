"""
The MIT License (MIT)
Copyright (c) 2015-2019 Rapptz
Copyright (c) 2019 DantasB
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import random
import time
import discord
import datetime
import aiohttp
import json

from discord.ext import commands
from forex_python.converter import CurrencyRates
from dhooks import Webhook
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions


startup_extensions = ['Music', 'Diversão', 'Interação', 'Cobrança', 'Administração', 'Error']
prefix = 'prefixo de interesse'
client = commands.Bot(command_prefix=prefix)
TOKEN = 'Seu discord bot token'
client.remove_command('help')

# Musica
players = {}

# tretas
lista = ['[nome] saiu de casa novo']#Deve ser escrito como: '[nome] fez algo'

# afk
with open('afks.json', 'r') as file:
    try:
        afklist = json.load(file)
    except ValueError:
        afklist = {}



@client.event
async def on_ready():
    print('--------------BD--------------')
    print('BOT ONLINE')
    print('Nome do Bot: ' + client.user.name)
    print('ID do Bot: ' + str(client.user.id))
    print('Versao do Discord: ' + discord.__version__)
    print('--------------BD--------------')
    game = discord.Game("$ajuda")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_member_join(member):
    guild = member.guild.get_channel() #logs channel
    fmt = 'Bem vindo ao servidor {1.name}, {0.mention}, aproveita e segue o baile.'
    await guild.send(fmt.format(member, member.guild), delete_after=15)
    role = discord.utils.get(member.guild.roles, name='Iniciados')
    await member.add_roles(role)


@client.event
async def on_member_remove(member):
    guild = member.guild.get_channel() #logs channel
    fmt = '{0.mention} ficou bolado e saiu do servidor'
    await guild.send(fmt.format(member), delete_after=15)


@client.event
async def on_guild_join(guild):
    for membro in guild.members:
        if membro.guild_permissions.administrator and membro != client.user:
            embed = discord.Embed(title="Bem vindo ao meu Suporte", colour=discord.Colour(0x370c5e),
                                  description="Olá, eu sou a Betina: \n esse suporte está aqui para te ajudar e "
                                              "ajudar ao meu criador ```\nSim, eu sou um bot e não vou roubar seus "
                                              "dados...```")
            embed.set_image(
                url=betina_icon)
            embed.set_thumbnail(
                url=betina_icon)
            embed.set_author(name="Betina")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)

            embed.add_field(name="Precisa de ajuda?🤔", value="para usar meus comandos utilize o $help")
            embed.add_field(name="Teve alguma ideia boa ? 😱: ",
                            value="fale com o meu criador, ele poderá implementar!")
            embed.add_field(name="Teve algum problema com o bot ?🙄",
                            value="não se preocupe, alguns problemas são comuns"
                                  " considerando o fato do bot estar em construção,"
                                  " mas, de qualquer forma,  fale com o meu criador.")
            embed.add_field(name="Criador do bot:", value="DantasB#7096", inline=True)
            embed.add_field(name="Maiores informações:", value="github.com/DantasB", inline=True)

            await membro.send(embed=embed)


@client.event
async def on_message(message):
    print('Logs:\n', message.author, message.content)
    if message.content.lower().startswith('$treta'):
        i = random.randrange(len(lista))
        listas = lista[i]
        x = random.randrange(len(message.guild.members))
        user = list(message.guild.members)[x]
        fquote = listas.replace('[nome]', user.name)
        await message.channel.send(fquote)

    guild_id = str(message.guild.id)
    author_id = str(message.author.id)
    afk_users = []

    if len(message.mentions) > 0:

        if guild_id in afklist:
            if author_id in afklist[guild_id]:
                del afklist[guild_id][author_id]
                embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                      description=f" Bem vindo de volta {message.author}")
                await message.channel.send(embed=embed, delete_after=10)
            else:
                mentions = message.mentions
                for member in mentions:
                    if guild_id in afklist:
                        if str(member.id) in afklist[guild_id]:
                            embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                              description=f"{member.name} está **AFK**: *{afklist[str(guild_id)][str(member.id)]}*")
                            await message.channel.send(embed=embed, delete_after=10)
                        else:
                            if member.id == client.user.id:
                                if message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                                    avi = message.author.avatar_url.rsplit("?", 1)[0]
                                else:
                                    avi = message.author.avatar_url_as(static_format='png')

                                embed = discord.Embed(
                                    title="Olá, meu nome é Betina. Caso queira saber mais sobre minhas funções, utilize o comando $help",
                                    colour=discord.Colour(0x370c5e))

                                embed.set_author(name=f"{message.author.name}", icon_url=avi)
                                embed.set_footer(text="Betina Brazilian Bot ",
                                         icon_url=betina_icon)
                                await message.channel.send(embed=embed)
        else:
            mentions = message.mentions
            for member in mentions:
                if member.id == client.user.id:
                    if message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                        avi = message.author.avatar_url.rsplit("?", 1)[0]
                    else:
                        avi = message.author.avatar_url_as(static_format='png')

                    embed = discord.Embed(
                        title="Olá, meu nome é Betina. Caso queira saber mais sobre minhas funções, utilize o comando $help",
                        colour=discord.Colour(0x370c5e))

                    embed.set_author(name=f"{message.author.name}", icon_url=avi)
                    embed.set_footer(text="Betina Brazilian Bot ",
                                 icon_url=betina_icon)
                    await message.channel.send(embed=embed)
    else:
        if guild_id in afklist:
            if author_id in afklist[guild_id]:
                del afklist[guild_id][author_id]
                embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                  description=f" Bem vindo de volta {message.author}")
                await message.channel.send(embed=embed, delete_after=10)


    with open('afks.json', 'w') as file:
        json.dump(afklist, file)


    await client.process_commands(message)


@client.event
async def on_raw_reaction_add(payload):
    if not payload.guild_id:
        return
    if payload.message_id != #messageid:
        return
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if client.user.id == member.id:
        return

    if str(payload.emoji) == '✅':
        role = discord.utils.get(guild.roles, name="Usuários")

    else:
        return

    await member.add_roles(role)
    await member.remove_roles(get(guild.roles, name='Iniciados'))


@commands.guild_only()
@client.command()
async def help(ctx):
    """Manda mensagem privada pro usuario!"""
    author = ctx.author
    embed = discord.Embed(title="Escolha uma categoria", colour=discord.Colour(0x370c5e),
                          description="```Bem vindo ao"
                                      " meu suporte, escolha abaixo uma das categorias"
                                      " para obter mais informações sobre minhas utilidades ```")
    embed.set_footer(text="Betina Brazilian Bot",
                     icon_url=betina_icon)

    embed.add_field(name="😂 **Diversão**", value="``$moeda, $ppt, $rola ...``", inline=False)
    embed.add_field(name="💰 **Cobrança**", value="``$devemais, $devemenos, $deve...``", inline=False)
    embed.add_field(name="🎵 **Música**", value="``$play, $resume, $stop, $fila...``", inline=False)
    embed.add_field(name="🗣 **Interação**", value="``$bate, $abraça, $treta...``", inline=False)
    embed.add_field(name="👮 **Administração**", value="``$apaga, $ping, $pong...``", inline=False)

    message = await author.send(embed=embed, delete_after=60)

    reaction_list = ["😂", "💰", "🎵", "🗣", "👮"]

    for reaction in reaction_list:
        await message.add_reaction(reaction)

    def check(reaction, user):
        return user == author and str(reaction.emoji) in reaction_list

    try:
        reaction, user = await client.wait_for('reaction_add', check=check)
    except:
        return

    if str(reaction.emoji) == "💰":
        await message.delete()
        embed = discord.Embed(title="Cobrança", colour=discord.Colour(0x370c5e),
                              description="*Bem vindo a categoria Cobrança:\nAqui você encontrará"
                                          " comandos que ajudará você a ter noção de finanças.*")
        embed.set_thumbnail(
            url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
        embed.add_field(name="**$devemais <usuário> <quantidade>**", value="``Você aumentará o quanto um"
                                                                           " usuário te deve!``", inline=False)
        embed.add_field(name="**$devemenos**", value="``Você diminuirá o quanto um usuário te deve!``",
                        inline=False)
        embed.add_field(name="**$deve**", value="``Mostra uma lista de todas as pessoas que um usuário"
                                                " deve!``", inline=False)
        embed.add_field(name="**$conversor <moeda1> <moeda2>"
                             " <quantidade>**", value="``Diz a cotação da moeda 1 em relação a moeda 2,"
                                                      " a quantidade é a quantidade vezes o valor da cotação``",
                        inline=False)
        msg = await author.send(embed=embed, delete_after=40)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == author and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(client.get_command("help"))


    elif str(reaction.emoji) == "😂":
        await message.delete()
        embed = discord.Embed(title="Diversão", colour=discord.Colour(0x370c5e),
                              description="*Bem vindo a categoria diversão:\n"
                                          "Aqui você encontrará comandos que trará alegria a todos no servidor.*")
        embed.set_thumbnail(
            url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)

        embed.add_field(name="**$moeda**", value="``Jogarei uma moeda. Poderá cair cara ou coroa!``",
                        inline=False)
        embed.add_field(name="**$rola**", value="``Rolarei um dado de até 20 lados!``", inline=False)
        embed.add_field(name="**$ppt <Pedra, Papel ou Tesoura>**", value="``Começarei um jogo de pedra, papel"
                                                                         " ou tesoura contra você!``",
                        inline=False)
        embed.add_field(name="**$bolsonaro**", value="``O Bolsonaro aparece?``",
                        inline=False)
        embed.add_field(name="**$faustao**", value="``O Faustão aparece!!``", inline=False)
        embed.add_field(name="**$miranha**", value="``O Miranha aparece!``", inline=False)

        msg = await author.send(embed=embed, delete_after=40)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == author and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(client.get_command("help"))


    elif str(reaction.emoji) == "🎵":
        await message.delete()
        embed = discord.Embed(title="Música", colour=discord.Colour(0x370c5e),
                              description="*Bem vindo a categoria Música:\nAqui você encontrará"
                                          " comandos que ajudará você a ouvir música enquanto faz suas atividades"
                                          " no discord.*")
        embed.set_thumbnail(
            url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)

        embed.add_field(name="**$play <música>**",
                        value="``Busco pela música ou toco a música de link específico!``",
                        inline=False)
        embed.add_field(name="**$pause**", value="``Pauso a música que está tocando atualmente!``",
                        inline=False)
        embed.add_field(name="**$stop**", value="``Paro de tocar a música e saio do canal de voz!``",
                        inline=False)
        embed.add_field(name="**$skip **", value="``Pularei a música que está tocando atualmente!``",
                        inline=False)
        embed.add_field(name="**$volume <quantidade>**",
                        value="``Mudarei o volume que está tocando a música!``",
                        inline=False)
        embed.add_field(name="**$fila **", value="``Mostrarei todas as músicas que estão na fila!``",
                        inline=False)
        embed.add_field(name="**$tocando**", value="``Direi a música que está tocando a música atualmente``",
                        inline=False)
        embed.add_field(name="**$sai**", value="``Sairei do canal de voz!``", inline=False)
        msg = await author.send(embed=embed, delete_after=40)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == author and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(client.get_command("help"))


    elif str(reaction.emoji) == "🗣":
        await message.delete()
        embed = discord.Embed(title="Interação", colour=discord.Colour(0x370c5e),
                              description="*Bem vindo a categoria Interação:\nAqui você encontrará"
                                          " comandos que ajudará você a interagir com outros membros do seu servidor*")
        embed.set_thumbnail(
            url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)

        embed.add_field(name="**$treta **", value="``Diz coisas assustadoras sobre as pessoas do servidor!``",
                        inline=False)
        embed.add_field(name="**$abraça <usuário>**", value="``Abraça o usuário!``",
                        inline=False)
        embed.add_field(name="**$beija <usuário>**", value="``Beija o usuário!``", inline=False)
        embed.add_field(name="**$bate <usuário> **", value="``Bate no usuário!``", inline=False)
        embed.add_field(name="**$dança <usuário> **", value="``Dança com o usuário!``", inline=False)
        embed.add_field(name="**$ataca <usuário> **", value="``Dá um ataque no usuário!``", inline=False)
        embed.add_field(name="**$emputece <usuário> **", value="``Deixa o usuário puto!``", inline=False)
        embed.add_field(name="**$voltapracaverna <usuário> **", value="``Manda o usuário voltar "
                                                                      "pro seu lugar de origem!``", inline=False)
        embed.add_field(name="**$ship <usuário1> <usuário2> (opcional)**", value="``Forma um novo casal!``", inline=False)
        embed.add_field(name="**$tnc **", value="``Manda alguem do servidor tomar no você sabe onde!``",
                        inline=False)
        embed.add_field(name="**$highfive <usuário>**", value="``Bate na mão do usuário!``",
                        inline=False)
        embed.add_field(name="**$roletarussa**", value="``Brincarei de roleta russa com você "
                                                       "e mais 4 pessoas!``", inline=False)

        msg = await author.send(embed=embed, delete_after=40)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == author and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(client.get_command("help"))


    elif str(reaction.emoji) == "👮":
        await message.delete()
        embed = discord.Embed(title="Administração", colour=discord.Colour(0x370c5e),
                              description="*Bem vindo a categoria Administração:\nAqui você encontrará"
                                          " comandos que ajudará você a ajudar a controlar seu servidor.*")
        embed.set_thumbnail(
            url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
        embed.add_field(name="**$apaga <quantidade>**", value="``Eu apagarei uma"
                                                              " quantidade de mensagens!``", inline=False)
        embed.add_field(name="**$ping**", value="``Retornarei o ping do usuário``", inline=False)
        embed.add_field(name="**$pong**", value="``oiráusu od gnip o ieranroter``", inline=False)
        embed.add_field(name="**$userinfo**", value="``Retorna informações sobre o usuário!``", inline=False)
        embed.add_field(name="**$serverinfo**", value="``Retorna informações sobre o servidor!``", inline=False)
        embed.add_field(name="**$afk <motivo> (opcional)**", value="``Define o usuário como afk!``", inline=False)
        embed.add_field(name="**$warn**", value="``Dá um Warn no usuário!``", inline=False)
        embed.add_field(name="**$mute**", value="``Em breve!``", inline=False)
        embed.add_field(name="**$ban <motivo> (opcional)**", value="``Bane o usuário do servidor!``", inline=False)

        msg = await author.send(embed=embed, delete_after=40)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == author and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(client.get_command("help"))


@commands.guild_only()
@client.command(name='afk', aliases=['away', 'ausente'])
@has_permissions(manage_messages=True)
async def afk(ctx, *, arg: str = None):
    if arg == None:
        reason = 'Sem motivos específicados!'
    else:
        reason = arg
    guild_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    if guild_id in afklist:
        afklist[guild_id][user_id] = reason
        embed = discord.Embed(colour=discord.Colour(0x370c5e), description=f"{ctx.author.mention} Está como afk agora! | {reason}")
        await ctx.send(embed=embed)
    else:
        afklist[guild_id] = {}
        afklist[guild_id][user_id] = reason
        embed = discord.Embed(colour=discord.Colour(0x370c5e), description=f"{ctx.author.mention} Está como afk agora! | {reason}")
        await ctx.send(embed=embed)

    with open("afks.json", "w") as file:
        json.dump(afklist, file)


@afk.error
async def afk_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="Comando $afk:", colour=discord.Colour(0x370c5e),
                                description="Dá o status de afk ao usuário"
                                              "\n \n**Como usar: $afk <motivo> (opcional)**")

        embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Gerenciar as mensagens`` *para utilizar este comando!*",
                            inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$afk fui a praia\n$afk ", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$away, $ausente.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")


@commands.guild_only()
@client.command(pass_context=True, name='addtreta', aliases=['maistreta', 'adiciona'])
@has_permissions(administrator=True)
async def addtreta(ctx, *, arg: str):
    lista.append(arg)



@addtreta.error
async def addtreta_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="Comando $addtreta:", colour=discord.Colour(0x370c5e),
                                description="Adiciona uma treta a lista de tretas"
                                              "\n \n**Como usar: $addtreta <treta> Obs: dentro da treta em vez "
                                            "do nome do usuário, deve-se colocar [nome]!**")

        embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$addtreta [nome] é vacilão\n$addtreta [nome] só faz besteira"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$maistreta, $adiciona.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'arg':
            embed = discord.Embed(title="Comando $addtreta:", colour=discord.Colour(0x370c5e),
                                  description="Adiciona uma treta a lista de tretas"
                                              "\n \n**Como usar: $addtreta <treta> Obs: dentro da treta em vez "
                                              "do nome do usuário, deve-se colocar [nome]!**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$addtreta [nome] é vacilão\n$addtreta [nome] só faz besteira"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$maistreta, $adiciona.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(TOKEN)
