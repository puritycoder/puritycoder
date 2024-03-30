import os
import random
import string
import discord
from discord.ext import commands
from discord.ui import Button, View

TOKEN = os.getenv('TOKEN')
WEB_URL = 'https://blendprive.netlify.app/'

# Comprobar si el token está configurado
if TOKEN is None:
    print(
        'No se ha configurado un token para el bot. Por favor, configura una variable de entorno llamada "TOKEN" con el token de tu bot.'
    )
    exit()

# Configurar el bot
intents = discord.Intents.default()
intents.messages = True  # Habilitar el intent de mensajes
intents.guilds = True
intents.dm_messages = True
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)


# Función para generar una licencia aleatoria
def generar_licencia():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(16))


# Clase para el botón "Generar Licencia"
class GenerarLicenciaButton(Button):

    def __init__(self):
        super().__init__(style=discord.ButtonStyle.success,
                         label="Generar Licencia")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # Generar una licencia
        licencia = generar_licencia()

        # Obtener la URL del avatar del autor
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url

        # Crear un embed bonito para enviar la licencia
        embed = discord.Embed(
            title="Licencia Generada",
            description=
            f"Aquí está tu licencia generada: {licencia}\n\n[Activar Licencia Automáticamente]({WEB_URL}?licencia={licencia})",
            color=0x00ff00)
        embed.set_author(name=interaction.user.display_name, icon_url=avatar_url)

        # Enviar el embed como mensaje privado
        await interaction.user.send(embed=embed)


# Evento para enviar el mensaje con el botón cuando el bot se conecta
@bot.event
async def on_ready():
    # Obtener el canal deseado por su ID
    canal_deseado_id = 1223438466574975096  # Reemplaza 'ID_del_Canal' con el ID del canal deseado
    canal = bot.get_channel(canal_deseado_id)

    # Crear un view con el botón "Generar Licencia"
    view = View()
    view.add_item(GenerarLicenciaButton())

    # Enviar el mensaje con el botón al canal deseado
    await canal.send("Pulsa el botón para generar una licencia:", view=view)


# Ejecutar el bot con el token proporcionado
bot.run(TOKEN)
