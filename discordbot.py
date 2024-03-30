import os
import random
import string

import discord
from discord.ext import commands

TOKEN = os.getenv('TOKEN')

# Comprobar si el token está configurado
if TOKEN is None:
  print(
      'No se ha configurado un token para el bot. Por favor, configura una variable de entorno llamada "TOKEN" con el token de tu bot.'
  )
  exit()

# Rest of the code remains the same
# Crear una instancia del cliente de Discord con los intents requeridos
intents = discord.Intents.default()
intents.messages = True  # Habilitar el intent de mensajes
intents.guilds = True
intents.dm_messages = True
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)


# Definir una función para generar una licencia aleatoria
def generar_licencia():
  caracteres = string.ascii_letters + string.digits + string.punctuation
  return ''.join(random.choice(caracteres) for _ in range(16))


# Manejar el evento 'on_message'
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # Verificar si el mensaje se envió desde el canal deseado
  canal_deseado_id = '1223438466574975096'  # Reemplaza 'ID_del_Canal' con el ID del canal deseado
  if str(message.channel.id) != canal_deseado_id:
    return

  # Verificar si el mensaje comienza con el comando '/gen'
  if message.content.startswith('/gen'):
    # Verificar si el autor del mensaje tiene el rol específico
    if discord.utils.get(message.author.roles, name='Cliente'):
      # Generar una licencia
      licencia = generar_licencia()
      # Enviar la licencia como mensaje privado
      await message.author.send(f'Aquí está tu licencia generada: {licencia}')
    else:
      await message.channel.send('No tienes permiso para generar licencias.')


# Ejecutar el bot con el token proporcionado
client.run(TOKEN)
