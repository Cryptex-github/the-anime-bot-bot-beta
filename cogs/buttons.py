import discord
from discord.ext import commands
import random

from discord import ui

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                assert isinstance(child, discord.ui.Button) # just to shut up the linter
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

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
        finally:
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
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def ttt(self, ctx):
        await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())
    
    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def click(self, ctx):
        colors = ["blurple", "grey", "green", "red"]
        random.shuffle(colors)
        color = random.choice(colors)
        v = SpeedClickView(color)
        for i in colors:
            v.add_item(SpeedClickButton(style=getattr(discord.ButtonStyle, i), label=i, custom_id=i))
        await ctx.send(f"Click the button that is {color}", view=v)

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def roo(self, ctx):
        r = RooView()
        e = [str(i) for i in self.bot.emojis if i.name.startswith("roo")][:25]
        for i in e:
            r.add_item(RooButton(emoji=i, style=discord.ButtonStyle.primary, label="\u200b"))
        m = await ctx.send(content="get your roo", view=r)

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def bobo(self, ctx):
        b = BoboView()
        b.add_item(BoboButton(style=discord.ButtonStyle.primary, custom_id="bobo", label="bobo"))
        b.add_item(BoboButton(style=discord.ButtonStyle.success, custom_id="big bobo", label="big bobo"))
        b.add_item(BoboButton(style=discord.ButtonStyle.secondary, custom_id="big big bobo", label="big big bobo"))
        b.add_item(BoboButton(style=discord.ButtonStyle.danger, custom_id="huge bobo", label="huge bobo"))
        m = await ctx.send(content="get your bobo", view=b)

def setup(bot):
    bot.add_cog(Buttons(bot))
