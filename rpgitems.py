class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class RareHerb:
    def __init__(self, name, description):
        self.name = name
        self.description = description

items = {'Leather Armor': {
    'type': 'armor',
    'defense': 5,
    'sell_price': 10,  # Add a sell price for the item
}, 'Iron Sword': {
    'type': 'weapon',
    'damage': 15,
    'sell_price': 20,  # Add a sell price for the item
}, 'Wooden Shield': {
    'type': 'armor',
    'defense': 8,
    'sell_price': 15,  # Add a sell price for the item
}, 'Steel Dagger': {
    'type': 'weapon',
    'damage': 12,
    'sell_price': 18,  # Add a sell price for the item
}, 'Lost Relic': {
    'type': 'artifact',  # You can specify a unique type for artifacts
    'description': 'The legendary Lost Relic of the Lymian Empire. Its power is shrouded in mystery.',
    'power': 'Mysterious Power',  # Add any special attributes or powers here
    'sell_price': None,  # Set the sell price to None if it's not available yet
}, 'Health Potion': {
    'type': 'potion',
    'sell_price': 5  # The price at which this item can be sold (5 gold by default)
}}
# Add the "Lost Relic" item
