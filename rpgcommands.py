from discord.ext import commands

import rpg.rpgcore
from database import DatabaseConnection
import rpg.rpgactions
import rpg.rpglocations
from rpg.disgameleader import get_level_leaderboard
from rpg.rpgblacksmnith import buy_from_blacksmith, sell_to_blacksmith

# Establishing the database connection
db = DatabaseConnection("rpg.db.db")


class RPGCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def rpg(self, ctx):
        """Starts or interacts with the RPG adventure."""
        if ctx.invoked_subcommand is None:
            await rpg.rpgactions.start_adventure(ctx)
            help_text = (
                "🛡️ **RPG Adventure Commands** 🛡️\n"
                "Use the following commands to manage your adventure:\n"
                "`~rpg stats` - Displays your character's stats.\n"
                "`~rpg explore` - Explores the current area.\n"
                "`~rpg inventory` - Shows what's in your inventory.\n"
                "`~rpg ll` - Shows the level leaderboard.\n"
                "`~rpg uhp` - Use a health potion.\n"
                "`~rpg save` - Saves your current progress.\n"
                "`~rpg armor [armor_name]` - Equip an armor item.\n"
                "`~rpg weapon [weapon_name]` - Equip a weapon.\n"
                "`~rpg npc [NPC name] [action]` - Interact with NPCs like the Blacksmith.\n"
                "`~rpg allocate [stat] [points]` - Allocate points to a stat.\n"
                "`~rpg move [location_name]` - Move to a new location.\n"
                "Start your adventure with `~rpg` or use the command for more actions."
            )
            await ctx.send(help_text)
        else:
            await ctx.invoke(ctx.invoked_subcommand)

    @rpg.command(name='stats')
    async def stats(self, ctx):
        """Displays the player's stats."""
        await rpg.rpgactions.show_stats(ctx)

    @rpg.command(name='explore')
    async def explore(self, ctx):
        """Explores the current area."""
        player = rpg.rpgcore.players.get(ctx.author.id)
        if player:
            await rpg.rpgactions.explore(ctx, player)
        else:
            await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~rpg`.")

    @rpg.command(name='inventory')
    async def inventory(self, ctx):
        """Shows the player's inventory."""
        await rpg.rpgactions.show_inventory(ctx)

    @rpg.command(name='ll')
    async def level_leaderboard(self, ctx):
        """Displays the level leaderboard."""
        leaderboard_data = get_level_leaderboard()
        if leaderboard_data:
            leaderboard_text = "Level Leaderboard:\n"
            for position, (discord_id, level) in enumerate(leaderboard_data, start=1):
                try:
                    user = await self.bot.fetch_user(discord_id)
                    username = user.name
                except Exception as e:
                    print(f"Error fetching user {discord_id}: {e}")
                    username = "Unknown User"

                leaderboard_text += f"{position}. {username} - Level {level}\n"

            await ctx.send(leaderboard_text)
        else:
            await ctx.send("The leaderboard is empty.")

    @rpg.command(name='save')
    async def save(self, ctx):
        """Saves the player's progress."""
        player = rpg.rpgcore.players.get(ctx.author.id)
        if player:
            player.save_to_db(db)
            await ctx.send(f"{ctx.author.mention}, your progress has been saved.")
        else:
            await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~rpg`.")

    @rpg.command(name='uhp')
    async def use_health_potion(self, ctx):
        """Uses a health potion."""
        player = rpg.rpgcore.players.get(ctx.author.id)
        if player:
            await rpg.rpgactions.use_health_potion( player)
        else:
            await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~rpg`.")
    @rpg.command(name='armor')
    async def equip_armor(self, ctx, *, armor_name):
        """Equips armor."""
        player = rpg.rpgcore.players.get(ctx.author.id)
        if player:
            equipped_item = player.equip_item(armor_name, 'armor')
            if equipped_item:
                await ctx.send(f"{ctx.author.mention}, you have equipped {equipped_item}.")
            else:
                await ctx.send(f"{ctx.author.mention}, you don't have {armor_name} in your inventory.")
        else:
            await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~rpg`.")

    @rpg.command(name='weapon')
    async def equip_weapon(self, ctx, *, weapon_name):
        """Equips a weapon."""
        player = rpg.rpgcore.players.get(ctx.author.id)
        if player:
            equipped_item = player.equip_item(weapon_name, 'weapon')
            if equipped_item:
                await ctx.send(f"{ctx.author.mention}, you have equipped {equipped_item}.")
            else:
                await ctx.send(f"{ctx.author.mention}, you don't have {weapon_name} in your inventory.")
        else:
            await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~rpg`.")

    @rpg.command(name='npc')
    async def interact_with_npc(self, ctx, npc_name, action=None):
        """Interacts with an NPC."""
        player = rpg.rpgcore.players.get(ctx.author.id)
        if player:
            if npc_name == 'Blacksmith':
                if action == 'buy':
                    await buy_from_blacksmith(player, ctx, self.bot)
                elif action == 'sell':
                    await sell_to_blacksmith(player, ctx, self.bot)
                else:
                    await ctx.send(f"{ctx.author.mention}, please specify 'buy' or 'sell' as the action.")
            else:
                await ctx.send(f"{ctx.author.mention}, there is no NPC named '{npc_name}' here.")
        else:
            await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~rpg`.")

    @rpg.command(name='allocate')
    async def allocate(self, ctx, stat: str, points: int):
        """Allocates stat points."""
        player = rpg.rpgcore.players.get(ctx.author.id)
        if player:
            valid_stats = ['attack', 'defense', 'health']
            if stat.lower() in valid_stats:
                if player.allocate_stat_points(stat.lower(), points):
                    await ctx.send(f"{ctx.author.mention}, you've allocated {points} points to {stat.capitalize()}.")
                    await rpg.rpgactions.show_stats(ctx)
                else:
                    await ctx.send(f"{ctx.author.mention}, you don't have enough unallocated stat points.")
            else:
                await ctx.send(f"{ctx.author.mention}, please specify a valid stat ({', '.join(valid_stats)}).")
        else:
            await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~start`.")

    @rpg.command(name='move')
    async def move(self, ctx, location_name: str):
        """Moves the player to a new location."""
        player = rpg.rpgcore.players.get(ctx.author.id)
        if player:
            if location_name.lower() == 'goblin_cave':
                rpg.rpglocations.move_to_goblin_cave(player)
                await ctx.send(f"{ctx.author.mention}, you have moved to the Goblin Cave.")
            elif location_name.lower() == 'forest':
                rpg.rpglocations.update_player_location(player, rpg.rpglocations.forest)
                await ctx.send(f"{ctx.author.mention}, you have moved to the Forest.")
            elif location_name.lower() == 'town':
                rpg.rpglocations.update_player_location(player, rpg.rpglocations.town_square)
                await ctx.send(f"{ctx.author.mention}, you have moved to the Town Square.")
            else:
                await ctx.send(f"{ctx.author.mention}, that location doesn't exist.")
        else:
            await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~rpg`.")


async def setup(bot):
    await bot.add_cog(RPGCommands(bot))
