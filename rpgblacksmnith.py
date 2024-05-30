import asyncio

import discord

from rpg.rpgitems import items

# Define a mapping of numbered emojis to items
emoji_to_item = {
    '1️⃣': 'Leather Armor',
    '2️⃣': 'Iron Sword',
    '3️⃣': 'Wooden Shield',
    '4️⃣': 'Steel Dagger',
    '5️⃣': 'Health Potion',
    # Add more emojis and items as needed
}

# Define the maximum number of items to display on each page
items_per_page = 4

async def buy_from_blacksmith(player, ctx, bot):
    # Create an embedded message for buying items
    embed = discord.Embed(
        title="Blacksmith's Shop",
        description="Here are the items available for purchase. React with the corresponding emoji to buy an item.",
        color=discord.Color.blue()
    )

    # Add items with emojis and prices to the embedded message
    for emoji, item in emoji_to_item.items():
        item_price = items[item]['sell_price']
        embed.add_field(
            name=f"{emoji} {item}",
            value=f"Price: {item_price} gold",
            inline=False
        )

    # Display the embedded message
    message = await ctx.send(embed=embed)

    # Add emojis as reactions
    for emoji in emoji_to_item.keys():
        await message.add_reaction(emoji)

    def reaction_check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in emoji_to_item.keys()

    try:
        reaction, _ = await bot.wait_for('reaction_add', timeout=30, check=reaction_check)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to make a choice.")
        return

    selected_item = emoji_to_item.get(str(reaction.emoji))
    if selected_item:
        item_price = items[selected_item]['sell_price']  # Get the item's price from the dictionary
        if player.gold >= item_price:
            player.gold -= item_price
            player.add_to_inventory(selected_item)
            await ctx.send(f"You bought a {selected_item} for {item_price} gold!")
        else:
            await ctx.send("You don't have enough gold to purchase this item.")
    else:
        await ctx.send("Invalid choice. Please select an available item.")

async def sell_to_blacksmith(player, ctx, bot):
    items_list = list(emoji_to_item.keys())  # Get the list of emojis
    num_pages = (len(items_list) + items_per_page - 1) // items_per_page  # Calculate the number of pages

    current_page = 0  # Start with the first page

    while True:
        # Calculate the start and end indices for the current page
        start_index = current_page * items_per_page
        end_index = start_index + items_per_page

        # Create an embedded message for selling items on the current page
        embed = discord.Embed(
            title="Blacksmith's Shop",
            description=f"Page {current_page + 1}/{num_pages}\nReact with the corresponding emoji to sell an item.",
            color=discord.Color.orange()
        )

        # Add sellable items with numbered emojis and sell prices to the embedded message for the current page
        for emoji, item in list(emoji_to_item.items())[start_index:end_index]:
            if item in player.inventory:
                item_price = items[item]['sell_price']
                embed.add_field(
                    name=f"{emoji} {item}",
                    value=f"Sell Price: {item_price} gold",
                    inline=False
                )

        # Display the embedded message
        message = await ctx.send(embed=embed)

        # Add numbered emojis as reactions
        for emoji in emoji_to_item.keys():
            await message.add_reaction(emoji)

        def reaction_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emoji_to_item.keys()

        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=30, check=reaction_check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to make a choice.")
            break  # Exit the loop on timeout

        selected_item = emoji_to_item.get(str(reaction.emoji))
        if selected_item and selected_item in player.inventory:
            item_price = items[selected_item]['sell_price']  # Get the item's sell price from the dictionary
            player.gold += item_price
            player.inventory[selected_item] -= 1
            await ctx.send(f"You sold a {selected_item} for {item_price} gold!")
        else:
            await ctx.send("Invalid choice or you don't have that item to sell.")

        # Check if there are more pages
        if num_pages > 1:
            next_page_emoji = '➡️'
            previous_page_emoji = '⬅️'

            if current_page < num_pages - 1:
                await message.add_reaction(next_page_emoji)
            if current_page > 0:
                await message.add_reaction(previous_page_emoji)

            def page_reaction_check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in [next_page_emoji, previous_page_emoji]

            try:
                reaction, _ = await bot.wait_for('reaction_add', timeout=30, check=page_reaction_check)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to navigate pages.")
                break  # Exit the loop on timeout

            if str(reaction.emoji) == next_page_emoji:
                current_page = min(current_page + 1, num_pages - 1)
            elif str(reaction.emoji) == previous_page_emoji:
                current_page = max(current_page - 1, 0)