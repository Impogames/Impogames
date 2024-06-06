import discord
from discord import app_commands
import os

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user.name} ({self.user.id})')
        await self.tree.sync()

client = MyClient()

@client.tree.command(name="meme", description="Wyślij załącznik na kanał oczekiwanie-na-mema")
async def meme(interaction: discord.Interaction, attachment: discord.Attachment):
    # Znalezienie kanału "oczekiwanie-na-mema"
    channel = discord.utils.get(interaction.guild.channels, name='oczekiwanie-na-mema')
    if not channel:
        await interaction.response.send_message("Kanał 'oczekiwanie-na-mema' nie został znaleziony.", ephemeral=True)
        return
    
    # Zapisanie załącznika lokalnie
    file_path = f'./{attachment.filename}'
    await attachment.save(file_path)
    
    # Wysłanie załącznika na kanał "oczekiwanie-na-mema" z informacją o użytkowniku
    await channel.send(content=f'Załącznik od {interaction.user.mention}', file=discord.File(file_path))
    
    # Usunięcie załącznika z lokalnego systemu plików po wysłaniu
    os.remove(file_path)
    
    # Wysłanie odpowiedzi do użytkownika
    await interaction.response.send_message(f'Załącznik {attachment.filename} został wysłany na kanał {channel.mention} przez {interaction.user.mention}', ephemeral=True)

client.run('MTE2Nzc2MDU4MzExOTA5NzkzOA.GUFhBq.hpv_ZVW3UCkLcEIN2A_fpxMVvF2hZuNjlm5EUQ')
