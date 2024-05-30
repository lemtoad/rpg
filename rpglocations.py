

class Location:
    def __init__(self, name, description, encounters=None):
        self.name = name
        self.description = description
        self.encounters = encounters if encounters else []


# Location instances
goblin_cave = Location("Goblin Cave", "A dark cave infested with goblins.")
forest = Location("Forest", "A dense forest with towering trees.")
town_square = Location("Town Square", "The bustling center of the town.")


# Function to initialize player's current location
def initialize_player_location(player):
    player.current_location = town_square  # Set the starting location


# Function to update player's current location
def update_player_location(player, new_location):
    player.current_location = new_location


def move_to_goblin_cave(player):
    # Update the player's current location to the Goblin Cave
    player.current_location = goblin_cave


def move_to_town(ctx, player):
    # Update the player's current location to the Town
    player.current_location = town_square
