import asyncio
import random

import rpg.rpglocations
from rpg.combathandler import CombatHandler
from rpg.rpgcore import Player, db, players
from rpg.rpgevents import EVENTS
from rpg.rpgmonsters import Monster


async def start_adventure(ctx):
    # Start or resume the player's adventure
    print(f"Starting adventure for user {ctx.author.id}")  # Debug statement
    player = Player.load_from_db(db, ctx.author.id)
    if player:
        await ctx.send(f"{ctx.author.mention}, welcome back to your adventure!")
    else:
        player = Player(ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, your adventure starts now!")
    players[ctx.author.id] = player


async def show_stats(ctx):
    player = players.get(ctx.author.id)
    if not player:
        await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~start`.")
        return

    # Calculate player stats
    attack = player.calculate_attack()
    defense = player.calculate_defense()
    equipped_armor = player.equipment.get('armor', "None")
    equipped_weapon = player.equipment.get('weapon', "None")

    stats_text = f"""
    **Your Stats**
    Level: {player.level}
    EXP: {player.exp}
    Gold: {player.gold}
    Max Health: {player.max_health}
    Current Health: {player.current_health}
    Base Attack: {player.base_attack}
    Base Defense: {player.base_defense}
    Attack: {attack}
    Defense: {defense}
    Health Potions: {player.inventory.get('health_potion', 0)}
    Stat Points: {player.stat_points}
    Equipped Armor: {equipped_armor}
    Equipped Weapon: {equipped_weapon}
    """

    await ctx.send(stats_text)


async def update_loop():
    while True:
        print("Updating game state...")
        await asyncio.sleep(60)


async def explore(ctx, player):
    current_location = player.current_location  # Get the player's current location

    # Check if the current location is "town_square"
    if current_location == rpg.rpglocations.town_square:
        # Simulate an exploration event
        event_name = random.choice(list(EVENTS.keys()))
        event_function = EVENTS.get(event_name)

        if event_function:
            result = await event_function(player, ctx)  # Call the function asynchronously
            if result:  # Check if the result is not empty
                await ctx.send(result)
        else:
            await ctx.send(f"{ctx.author.mention}, an unknown event occurred.")

    if current_location.encounters:
        encounter = random.choice(current_location.encounters)
        if callable(encounter):  # Check if the encounter is a callable function
            await encounter(player, ctx)  # Trigger the encounter function
        else:
            await ctx.send(f"{ctx.author.mention}, an unknown encounter occurred in {current_location.name}.")

    # Check if there is a location encounter and the current location is not "town_square"
    if current_location != rpg.rpglocations.town_square and current_location.encounters:
        encounter = random.choice(current_location.encounters)
        if isinstance(encounter, Monster):  # Check if the encounter is a monster
            combat_handler = CombatHandler(player, encounter, ctx)
            await combat_handler.start_combat()


async def show_inventory(ctx):
    player = players.get(ctx.author.id)
    if player:
        inventory_text = f"{ctx.author.mention}, your inventory:\n"

        # Display equipped armor and weapon
        equipped_armor = player.equipment['armor']
        equipped_weapon = player.equipment['weapon']

        if equipped_armor:
            inventory_text += f"Equipped Armor: {equipped_armor}\n"

        if equipped_weapon:
            inventory_text += f"Equipped Weapon: {equipped_weapon}\n"

        # Display inventory items
        if player.inventory:
            for item, count in player.inventory.items():
                inventory_text += f"{item}: {count}\n"
        else:
            inventory_text += "Your inventory is empty."

        await ctx.send(inventory_text)
    else:
        await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~start`.")


async def use_health_potion(ctx):
    # Use a health potion to restore health
    player = players.get(ctx.author.id)
    if player:
        if 'Health Potion' in player.inventory and player.inventory['Health Potion'] > 0:
            player.use_health_potion()
            await ctx.send(
                f"{ctx.author.mention}, you used a health potion. Your health is now {player.current_health}/{player.max_health}.")
        else:
            await ctx.send(f"{ctx.author.mention}, you don't have any health potions.")
    else:
        await ctx.send(f"{ctx.author.mention}, you haven't started your adventure yet. Use `~start`.")
