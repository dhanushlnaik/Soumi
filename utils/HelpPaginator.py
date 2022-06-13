import disnake
from disnake.ext import commands
from disnake.ui import View ,Button, Select

options = [
    disnake.SelectOption(label="Actions", description="Includes Roleplay/Action Commands.", emoji=disnake.PartialEmoji(name="EmotesCategory", id=943427911027925082)),
    disnake.SelectOption(label="Anime", description="Includes Anime Related Commands.", emoji=disnake.PartialEmoji(name="EmiPuck", id=943366309775835247,animated=True)),
    disnake.SelectOption(label="General", description="Includes General Commands.", emoji=disnake.PartialEmoji(name="GeneralCategory", id=943427909752856577)),
    disnake.SelectOption(label="Fun", description="Includes Fun Related Commands.", emoji=disnake.PartialEmoji(name="FunCategory", id=943427905931857961)),
    disnake.SelectOption(label="Meme", description="Includes Meme Related Commands.", emoji=disnake.PartialEmoji(name="MemeCategory", id=943427907877994507)),
    disnake.SelectOption(label="Info", description="Includes Info Related Commands.", emoji=disnake.PartialEmoji(name="InformationCategory", id=943427908691701771)),
    disnake.SelectOption(label="Utility", description="Includes Utility Related Commands.", emoji=disnake.PartialEmoji(name="AEmiThinkC", id=943366254243233822)),
    disnake.SelectOption(label="Moderation", description="Includes Moderation Related Commands.", emoji=disnake.PartialEmoji(name="ModerationCategory", id=943428021212307476, animated=True)),
    disnake.SelectOption(label="Family", description="Includes Family Related Commands.", emoji=disnake.PartialEmoji(name="FamilyCategory", id=943427906674253865))
]
def get_options(ctx):
    options = []
    bot = ctx.bot
    for cogn in bot.cogs:
            
        if not cogn: pass
        cog = bot.get_cog(cogn)
            
        options.append(disnake.SelectOption(label=cogn, description=cog.description, emoji=cog.emoji))
        return options


class Simple(disnake.ui.View):
    """
    Embed Paginator.
    Parameters:
    ----------
    timeout: int
        How long the Paginator should timeout in, after the last interaction. (In seconds) (Overrides default of 60)
    PreviousButton: disnake.ui.Button
        Overrides default previous button.
    NextButton: disnake.ui.Button
        Overrides default next button.
    PageCounterStyle: disnake.ButtonStyle
        Overrides default page counter style.
    InitialPage: int
        Page to start the pagination on.
    """

    def __init__(self, *,
                 timeout: int = 60,
                 sPrevButton : disnake.ui.Button = disnake.ui.Button(emoji="⏮️", row=2),
                 sNextButton : disnake.ui.Button = disnake.ui.Button(emoji="⏭️", row=2),
                 PreviousButton: disnake.ui.Button = disnake.ui.Button(emoji=disnake.PartialEmoji(name="\U000025c0"), row=2),
                 NextButton: disnake.ui.Button = disnake.ui.Button(emoji=disnake.PartialEmoji(name="\U000025b6"), row=2),
                 PageCounterStyle: disnake.ButtonStyle = disnake.ButtonStyle.grey,
                 InitialPage: int = 0
                 ) -> None:
        self.PreviousButton = PreviousButton
        self.NextButton = NextButton
        self.sPrevButton = sPrevButton
        self.sNextButton = sNextButton
        self.PageCounterStyle = PageCounterStyle
        self.InitialPage = InitialPage

        self.message = None
        self.pages = None
        self.ctx = None
        self.message = None
        self.current_page = None
        self.page_counter = None
        self.total_page_count = None

        super().__init__(timeout=timeout)

    async def start(self, ctx: commands.Context, pages: list[disnake.Embed], message):
        self.pages = pages
        self.total_page_count = len(pages)
        self.ctx = ctx
        self.current_page = self.InitialPage
        self.message = message

        self.PreviousButton.callback = self.previous_button_callback
        self.NextButton.callback = self.next_button_callback
        self.sPrevButton.callback = self.sprevious_button_callback
        self.sNextButton.callback = self.snext_button_callback

        self.page_counter = SimplePaginatorPageCounter(style=self.PageCounterStyle,
                                                       TotalPages=self.total_page_count,
                                                       InitialPage=self.InitialPage)

        btn1 = Button(label="Invite", style=disnake.ButtonStyle.url,row=0, url="https://disnake.com/api/oauth2/authorize?client_id=850243448724127754&permissions=140076435526&scope=bot", emoji=disnake.PartialEmoji(name="invite", id=939483316367802418))
        btn3 = Button(label="Support Server", style=disnake.ButtonStyle.url,row=0, url="https://disnake.gg/eZFKMmS6vz", emoji=disnake.PartialEmoji(name="head", id=939483469426360400))
        btn2 = Button(label="Vote Me", style=disnake.ButtonStyle.url,row=0, url="https://top.gg/bot/850243448724127754/vote", emoji=disnake.PartialEmoji(name="head", id=939483469426360400))
        menu = Select(placeholder="Select any Category",min_values=1, max_values=1,options=options,row=1)
        
        self.add_item(btn1)
        self.add_item(btn3)
        self.add_item(btn2)
        # self.add_item(menu)
        self.add_item(self.sPrevButton)
        self.add_item(self.PreviousButton)
        self.add_item(self.page_counter)
        self.add_item(self.NextButton)
        self.add_item(self.sNextButton)

        await self.message.edit(embed=self.pages[self.InitialPage], view=self)

    async def previous(self):
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)
    
    async def first(self):
        if self.current_page == 0:
            return
        else:
            self.current_page =0

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def last(self):
        if self.current_page == self.total_page_count - 1:
            return
        else:
            self.current_page = self.total_page_count - 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def next(self):
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def next_button_callback(self, interaction: disnake.Interaction):
        if interaction.user != self.ctx.author:
            embed = disnake.Embed(description="You cannot control this pagination because you did not execute it.",
                                  color=disnake.Colour.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.next()

    async def previous_button_callback(self, interaction: disnake.Interaction):
        if interaction.user != self.ctx.author:
            embed = disnake.Embed(description="You cannot control this pagination because you did not execute it.",
                                  color=disnake.Colour.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.previous()

    async def snext_button_callback(self, interaction: disnake.Interaction):
        if interaction.user != self.ctx.author:
            embed = disnake.Embed(description="You cannot control this pagination because you did not execute it.",
                                  color=disnake.Colour.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.last()

    async def sprevious_button_callback(self, interaction: disnake.Interaction):
        if interaction.user != self.ctx.author:
            embed = disnake.Embed(description="You cannot control this pagination because you did not execute it.",
                                  color=disnake.Colour.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.first()


class SimplePaginatorPageCounter(disnake.ui.Button):
    def __init__(self, style: disnake.ButtonStyle, TotalPages, InitialPage):
        super().__init__(label=f"{InitialPage + 1}/{TotalPages}", style=style, disabled=True, row=2)