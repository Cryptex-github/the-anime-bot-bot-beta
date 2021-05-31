import discord
from discord.ext import commands
import random

from discord import ui

class SpeedClickView(ui.View):
    def __init__(self, color, *args, **kwargs):
        self.color = color
        self.clicked = False
        super().__init__(*args, **kwargs)

class SpeedClickButton(ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def callback(self, interaction):
        e = discord.utils.utcnow()
        if self.view.clicked:
            return
        self.view.clicked = True
        try:
            if self.custom_id != self.view.color:
                return await interaction.response.send_message(content=f"Wrong color", ephemeral=True)
            f = e - interaction.message.created_at
            for button in self.view.children:
                button.disabled = True
            await interaction.response.edit_message(content=f"{interaction.user} won. They clicked the {self.view.color} button within {f.total_seconds()} seconds", view=self.view)
            self.view.stop()
        except:
            self.view.clicked = False


class RooView(ui.View):
    def __init__(self, *args, **kwargs):
        self.counter = 0
        super().__init__(*args, **kwargs)

class RooButton(ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def callback(self, interaction):
        self.view.counter += 1
        await interaction.response.edit_message(content=f"get your roo: total roo collected: {self.view.counter}")
        await interaction.response.send_message(content=f"{interaction.user} got a {str(self.emoji)}", ephemeral=True)

class BoboView(ui.View):
    def __init__(self, *args, **kwargs):
        self.counter = 0
        super().__init__(*args, **kwargs)

class BoboButton(ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def callback(self, interaction):
        self.view.counter += 1
        await interaction.response.edit_message(content=f"get your bobo: total bobo collected: {self.view.counter}")
        await interaction.response.send_message(content=f"{interaction.user} got a {self.custom_id}", ephemeral=True)


class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def click(self, ctx):
        colors = ["blurple", "grey", "green", "red"]
        random.shuffle(colors)
        color = random.choice(colors)
        v = SpeedClickView(color)
        for i in colors:
            v.add_item(SpeedClickButton(style=getattr(discord.ButtonStyle, i), label=i, custom_id=i))
        await ctx.send(f"Click the button that is {color}", view=v)

    @commands.command()
    async def roo(self, ctx):
        r = RooView()
        e = [str(i) for i in self.bot.emojis if i.name.startswith("roo")][:25]
        for i in e:
            r.add_item(RooButton(emoji=i, style=discord.ButtonStyle.primary, label="\u200b"))
        m = await ctx.send(content="get your roo", view=r)

    @commands.command()
    async def bobo(self, ctx):
        b = BoboView()
        b.add_item(BoboButton(style=discord.ButtonStyle.primary, custom_id="bobo", label="bobo"))
        b.add_item(BoboButton(style=discord.ButtonStyle.success, custom_id="big bobo", label="big bobo"))
        b.add_item(BoboButton(style=discord.ButtonStyle.secondary, custom_id="big big bobo", label="big big bobo"))
        b.add_item(BoboButton(style=discord.ButtonStyle.danger, custom_id="huge bobo", label="huge bobo"))
        m = await ctx.send(content="get your bobo", view=b)

def setup(bot):
    bot.add_cog(Buttons(bot))