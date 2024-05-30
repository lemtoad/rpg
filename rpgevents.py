import asyncio

from rpg.combathandler import CombatHandler
from rpg.rpgitems import RareHerb
from rpg.rpgmonsters import *
from rpg.rpgquest import event_lost_relic

# Constants for event outcomes and values
GOLD_MIN = 5
GOLD_MAX = 20
EXP_MIN = 10
EXP_MAX = 30
POTION_MIN = 1
POTION_MAX = 2
HERB_MIN = 1
HERB_MAX = 2

# Constants for event outcomes
EVENT_OUTCOMES = {
    "gold": "You went hunting in the forest and found a hidden treasure chest filled with gold!",
    "experience": "During your hunt, you encountered a pack of wolves. You bravely fought them off and gained "
                  "experience.",
    "herb": "While hunting, you stumbled upon a rare herb with magical properties. You collected it for later use.",
    "default": "Unfortunately, your hunt didn't yield much, but you still had an adventure in the wilderness.",
}


# Class for a rare herb



# Event handler for generic outcomes (gold, experience, herb)
async def event_generic(player, ctx, outcome, min_value, max_value, gain_message):
    value_gain = random.randint(min_value, max_value)
    if outcome == "gold":
        player.gold += value_gain
    elif outcome == "experience":
        player.gain_exp(value_gain)
    elif outcome == "herb":
        rare_herb = RareHerb("Mystic Herb", "A rare herb with magical properties.")
        player.add_to_inventory('rare_herb', 1)

    await ctx.send(f"{ctx.author.mention}, {gain_message} You gained {value_gain} {outcome.capitalize()}!")


# Event function for finding gold
async def event_gold(player, ctx):
    await event_generic(player, ctx, "gold", GOLD_MIN, GOLD_MAX, "You found a hidden treasure chest filled with gold!")


# Event function for encountering monsters
async def event_monster(player, ctx):
    monster_classes = [Goblin, Orc, Dragon, Troll, Wolf, Skeleton, GiantSpider, Wraith, Bunny, Bandit]
    random_monster_class = random.choice(monster_classes)
    monster = random_monster_class()
    combat_handler = CombatHandler(player, monster, ctx)

    winner = await combat_handler.start_combat()
    if winner:
        await combat_handler.end_combat()


# Event function for making choices
async def event_choice(player, ctx):
    choices = {
        "A": "Open the mysterious door",
        "B": "Talk to the stranger",
        "C": "Ignore and move on"
    }

    await ctx.send(f"{ctx.author.mention}, you encounter a fork in the road. What will you do?\n" +
                   "\n".join([f"{key}: {value}" for key, value in choices.items()]))

    def check(msg):
        return msg.author == ctx.author and msg.content.upper() in choices.keys()

    try:
        response = await ctx.bot.wait_for("message", check=check, timeout=30.0)  # Wait for 30 seconds
        print(f"Response received: {response.content}")  # Debug statement
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, you took too long to decide.")
        return

    choice = response.content.upper()
    if choice == "A":
        await event_generic(player, ctx, "gold", GOLD_MIN, GOLD_MAX, "")
    elif choice == "B":
        await event_generic(player, ctx, "experience", EXP_MIN, EXP_MAX, "")
    elif choice == "C":
        await ctx.send(f"{ctx.author.mention}, you decided to move on.")


# Event function for finding potions
async def event_potion(player, ctx):
    potion_count = random.randint(1, 2)  # Generate 1 or 2 potions
    player.inventory['health_potion'] += potion_count
    await ctx.send(f"{ctx.author.mention}, you found {potion_count} health potions!")


# Event function for hunting with various outcomes
async def event_hunt(player, ctx):
    outcome = random.choice(list(EVENT_OUTCOMES.keys()))
    result_message = EVENT_OUTCOMES[outcome]

    if outcome in ["gold", "experience", "herb"]:
        if outcome == "herb":
            await event_generic(player, ctx, outcome, HERB_MIN, HERB_MAX, result_message)
        else:
            await event_generic(player, ctx, outcome, GOLD_MIN, GOLD_MAX, result_message)


# Event function for interacting with a merchant
async def event_merchant(player, ctx):
    choices = {
        "A": "Buy a Health Potion for 5 gold",
        "B": "Upgrade Attack for 10 gold",
        "C": "Upgrade Defense for 8 gold",
        "D": "Leave the merchant"
    }

    await ctx.send(f"{ctx.author.mention}, you meet a wandering merchant. What will you do?\n" +
                   "\n".join([f"{key}: {value}" for key, value in choices.items()]))

    def check(msg):
        return msg.author == ctx.author and msg.content.upper() in choices.keys()

    try:
        response = await ctx.bot.wait_for("message", check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, you took too long to decide.")
        return

    choice = response.content.upper()

    if choice == "A":
        if player.gold >= 5:
            player.gold -= 5
            player.inventory['health_potion'] += 1
            await ctx.send(f"{ctx.author.mention}, you bought a Health Potion.")
        else:
            await ctx.send(f"{ctx.author.mention}, you don't have enough gold.")

    elif choice == "B":
        if player.gold >= 10:
            player.gold -= 10
            player.attack += 2
            await ctx.send(f"{ctx.author.mention}, your attack power has been increased.")
        else:
            await ctx.send(f"{ctx.author.mention}, you don't have enough gold.")

    elif choice == "C":
        if player.gold >= 8:
            player.gold -= 8
            player.defense += 1
            await ctx.send(f"{ctx.author.mention}, your defense has been increased.")
        else:
            await ctx.send(f"{ctx.author.mention}, you don't have enough gold.")

    elif choice == "D":
        await ctx.send(f"{ctx.author.mention}, you decided to leave the merchant.")


# Define a dictionary that maps event names to their corresponding functions
EVENTS = {
    "gold": event_gold,
    "monster": event_monster,
    "potion": event_potion,
    "choice_event": event_choice,
    "hunt": event_hunt,
    "merchant": event_merchant,
    "lost_relic": event_lost_relic,

}
