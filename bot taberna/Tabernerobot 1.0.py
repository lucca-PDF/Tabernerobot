import discord
from discord.ext import commands
import secreto  # el token
from datos import razas_info, trasfondos_info

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Función para buscar coincidencias parciales
def buscar_coincidencias(texto, opciones):
    texto = texto.lower()
    return [opcion for opcion in opciones if texto in opcion.lower()]

@bot.command(name="pj")
async def pj(ctx, *, argumento: str = None):
    if argumento is None:
        await ctx.send("Por favor, escribe una raza y un trasfondo separados por `/`.\nEjemplo: `$pj alto elfo/marinero`.")
        return

    # Dividir la entrada del usuario usando "/"
    partes = argumento.split("/")
    if len(partes) != 2:
        await ctx.send("Formato incorrecto. Asegúrate de usar `/` para separar raza y trasfondo.\nEjemplo: `$pj alto elfo/marinero`.")
        return

    raza_entrada = partes[0].strip()
    trasfondo_entrada = partes[1].strip()

    # Buscar coincidencias en razas y trasfondos
    razas_coincidencias = buscar_coincidencias(raza_entrada, razas_info.keys())
    trasfondos_coincidencias = buscar_coincidencias(trasfondo_entrada, trasfondos_info.keys())

    # Validar coincidencias únicas
    if len(razas_coincidencias) == 1 and len(trasfondos_coincidencias) == 1:
        raza_seleccionada = razas_coincidencias[0]
        trasfondo_seleccionado = trasfondos_coincidencias[0]

        raza_data = razas_info[raza_seleccionada]
        trasfondo_data = trasfondos_info[trasfondo_seleccionado]

        # Construir el mensaje con la información detallada
        mensaje = f"**Raza:** {raza_seleccionada.capitalize()}\n"
        mensaje += f"Idiomas: {', '.join(raza_data['idiomas']) if raza_data['idiomas'] else 'Ninguno'}\n"
        mensaje += f"Competencias: {', '.join(raza_data['competencias']) if raza_data['competencias'] else 'Ninguno'}\n"
        mensaje += f"Extra: {', '.join(raza_data['extra']) if raza_data['extra'] else 'Ninguno'}\n"
        mensaje += f"Link: {', '.join(raza_data['link']) if raza_data['link'] else 'Ninguno'}\n\n"
        mensaje += f"**Trasfondo:** {trasfondo_seleccionado.capitalize()}\n"
        mensaje += f"Idiomas: {', '.join(trasfondo_data.get('idiomas', ['Ninguno']))}\n"
        mensaje += f"Competencias: {', '.join(trasfondo_data['competencias']) if trasfondo_data['competencias'] else 'Ninguno'}\n"
        mensaje += f"Extra: {', '.join(trasfondo_data['extra']) if trasfondo_data['extra'] else 'Ninguno'}\n"
        mensaje += "** esto es una descricion general se recomieda leer la ficha oficial**"
        await ctx.send(mensaje)
        return

    # Sugerencias para coincidencias parciales
    respuesta = ""
    if not razas_coincidencias:
        respuesta += f"No se encontraron razas que coincidan con '{raza_entrada}'.\n"
    elif len(razas_coincidencias) > 1:
        respuesta += f"**Razas sugeridas:** {', '.join(razas_coincidencias).capitalize()}\n"

    if not trasfondos_coincidencias:
        respuesta += f"No se encontraron trasfondos que coincidan con '{trasfondo_entrada}'.\n"
    elif len(trasfondos_coincidencias) > 1:
        respuesta += f"**Trasfondos sugeridos:** {', '.join(trasfondos_coincidencias).capitalize()}\n"

    if respuesta:
        await ctx.send(respuesta)
    else:
        await ctx.send("No se encontraron coincidencias únicas. Por favor, revisa la ortografía o especifica más palabras.")

bot.run(secreto.TOKEN)
