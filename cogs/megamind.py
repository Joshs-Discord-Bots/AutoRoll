import nextcord
from nextcord.ext import commands
from PIL import Image, ImageDraw, ImageFont

def generate(text, output='cogs/resources/meme.jpg'):
    text = f'No {text}?' # format text
    text_length = len(text) # max is 20
    font_size = int(70-(text_length)) # calculate font size
    min_font_size = 20
    if font_size < min_font_size: font_size = min_font_size # minimum font size
    text_color = (255, 255, 255)
    stroke_color = (0, 0, 0)
    stroke_width = font_size//15
    font = ImageFont.truetype(font="impact.ttf", size=font_size, encoding="unic")
    # --------------------------------------------------
    file = Image.open('cogs\\resources\\base.jpg') # open image
    image = ImageDraw.Draw(file) # create a layer to draw text on
    textPos = (file.width/2, image.textbbox(text=text, xy=(0, 0), font=font)[3])
    image.text(textPos, text, font=font, fill=text_color, stroke_width=stroke_width, stroke_fill=stroke_color, anchor="ms")

    file.save(output)



class Megamind(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @nextcord.slash_command(description='Creates a "No __?" meme.', guild_ids=[330974948870848512])
    @nextcord.slash_command(description='Creates a "No __?" meme.')
    async def no(self, interaction: nextcord.Interaction, text: str):
        generate(text)
        await interaction.send("", files=[nextcord.File('cogs/resources/meme.jpg')])

def setup(client):
    client.add_cog(Megamind(client))