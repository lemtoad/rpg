import json
import random

import rpg.rpglocations  # Import your locations module
from database import DatabaseConnection
from rpg.rpgitems import items
from rpg.rpgquest import LymianEmpire

# Initialize the database connection
db = DatabaseConnection("chat_history.db")


class State:
    def __init__(self):
        self.active_quest = None


# In your Player class' __init__ method

class Player:
    def __init__(self, discord_id):
        # Initialize player attributes
        self.discord_id = discord_id
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.max_health = 100
        self.current_health = self.max_health
        self.base_attack = 10
        self.base_defense = 5
        self.inventory = {'health_potion': 0, 'rare_herb': 0, 'lymian_prism': 0}
        self.equipment = {'armor': None, 'weapon': None}
        self.stat_points = 0  # Add a stat_points attribute
        self.kills_per_monster = {}
        self.attack = self.calculate_attack()
        self.completed_quests = set()  # Store completed quest IDs as a set
        self.goblins_defeated = 0  # Initialize the goblins_defeated attribute
        self.current_location = rpg.rpglocations.town_square
        self.state = State()
        self.state.active_quest = None  # No quest by default
        self.lymian_empire_state = LymianEmpire()

    def add_to_inventory(self, item, quantity=1):
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def add_experience(self, exp_gain):
        self.exp += exp_gain

    def add_gold(self, gold_gain):
        self.gold += gold_gain

    def use_rare_herb(self):
        # Check if the player has a "rare_herb" in their inventory
        if 'rare_herb' in self.inventory and self.inventory['rare_herb'] > 0:
            # Use the rare herb to avoid resetting
            self.inventory['rare_herb'] -= 1
            return True  # The rare herb was used successfully
        return False  # The player doesn't have a rare herb

    def equip_item(self, item_name, item_type):
        # Check if the player has the item in their inventory
        if self.inventory.get(item_name, 0) > 0:
            # Check the item type and equip accordingly
            if item_type == 'armor':
                self.equipment['armor'] = item_name
            elif item_type == 'weapon':
                self.equipment['weapon'] = item_name
            # Remove the item from the inventory
            self.inventory[item_name] -= 1
            return item_name  # Return the name of the equipped item
        else:
            return None  # Item not found in inventory

    @classmethod
    def load_from_db(cls, db, discord_id):
        # Load player data from the database
        query = """
            SELECT level, exp, gold, max_health, current_health, base_attack, base_defense, inventory, equipment, 
            stat_points, lymian_empire_state  
            FROM players
            WHERE discord_id = ?
        """
        result = db.fetchall(query, (discord_id,))
        if result:
            data = result[0]

            player = cls(discord_id)
            player.level = data[0]
            player.exp = data[1]
            player.gold = data[2]
            player.max_health = data[3]
            player.current_health = data[4]
            player.base_attack = data[5]
            player.base_defense = data[6]
            player.stat_points = data[9]  # Load unallocated stat points
            if len(data) > 10:
                le_data = json.loads(data[10]) if data[10] else {}
                player.lymian_empire_state = LymianEmpire()
                player.lymian_empire_state.__dict__.update(le_data)
            else:
                print("Failed to load LymianEmpire state: data tuple does not contain an element at index 10.")

            if len(data) > 7:
                player.inventory = json.loads(data[7]) if data[7] else {}
            else:
                print("Failed to load inventory: data tuple does not contain an element at index 7.")

            if len(data) > 8:
                player.equipment = json.loads(data[8]) if data[8] else {'armor': None, 'weapon': None}
            else:
                print("Failed to load equipment: data tuple does not contain an element at index 8.")

            return player

    def calculate_attack(self):
        # Calculate the player's attack based on their base attack and equipped weapon (if any)
        if self.equipment and self.equipment.get('weapon'):
            weapon_data = items.get(self.equipment['weapon'])
            if weapon_data:
                return self.base_attack + weapon_data.get('damage', 0)
        # If the player doesn't have a weapon or equipment, use their base attack as the default
        return self.base_attack

    def calculate_defense(self):
        # Calculate the player's defense based on their base defense and equipped armor (if any)
        if self.equipment and self.equipment.get('armor'):
            armor_data = items.get(self.equipment['armor'])
            if armor_data:
                return self.base_defense + armor_data.get('defense', 0)
        # If the player doesn't have equipped armor or equipment, use their base defense as the default
        return self.base_defense

    def reset_stats(self):
        # Reset the player's stats as before
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.max_health = 100
        self.current_health = self.max_health
        self.base_attack = 10
        self.base_defense = 5
        self.stat_points = 5  # Reset unallocated stat points
        self.inventory = {'health_potion': 0}

    def calculate_exp_required(self):
        # Define an exponential growth curve for EXP required
        base_exp = 10  # Adjust this as needed
        exponent = 1.5  # Adjust this as needed for the desired curve

        return int(base_exp * (self.level ** exponent))

    def level_up(self):
        # Calculate EXP required for the next level
        exp_required = self.calculate_exp_required()

        # Check if the player's current EXP surpasses the required EXP
        if self.exp >= exp_required:
            # Level up logic here (e.g., increase stats, reset EXP, etc.)
            self.level += 1
            self.exp = 0
            self.max_health += random.randint(5, 15)
            self.current_health = self.max_health
            self.base_attack += random.randint(1, 5)
            self.base_defense += random.randint(1, 3)
            self.stat_points += 3

    def allocate_stat_points(self, stat, points):
        # Allocate stat points to player's stats
        if self.stat_points >= points:
            if stat == 'attack':
                self.base_attack += points
            elif stat == 'defense':
                self.base_defense += points
            elif stat == 'health':
                self.max_health += points * 10  # Each point increases max health by 10
                self.current_health = min(self.current_health + points * 10, self.max_health)  # Restore health
            self.stat_points -= points
            return True
        return False

    def gain_exp(self, amount):
        # Gain experience points and check for level up
        self.exp += amount
        if self.exp >= self.level * 10:  # Level up condition
            self.level_up()

    def calculate_damage(self, enemy_defense):
        # Calculate damage to deal to an enemy
        damage = max(0, self.calculate_attack() - enemy_defense)
        return damage

    def save_to_db(self, db):
        query = """
        REPLACE INTO players (
            discord_id, level, exp, gold, max_health, current_health, 
            base_attack, base_defense, inventory, equipment, stat_points, 
            lymian_empire_state
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        serialized_lymian_empire_state = json.dumps(self.lymian_empire_state.__dict__)
        db.execute(query, (
            self.discord_id,
            self.level,
            self.exp,
            self.gold,
            self.max_health,
            self.current_health,
            self.base_attack,
            self.base_defense,
            json.dumps(self.inventory),
            json.dumps(self.equipment),
            self.stat_points,
            serialized_lymian_empire_state  # Save the serialized Lymian Empire state
        ))

    def use_health_potion(self):
        # Use a health potion to restore health
        if 'health_potion' in self.inventory and self.inventory['health_potion'] > 0:
            health_to_restore = 10  # Adjust the amount as needed
            self.current_health += health_to_restore
            self.inventory['health_potion'] -= 1
            if self.current_health > self.max_health:
                self.current_health = self.max_health

    def take_damage(self, damage):
        # Calculate damage after considering player's defense
        actual_damage = max(0, damage - self.calculate_defense())
        self.current_health -= actual_damage


class NPC:
    def __init__(self, name):
        self.name = name


# Define an interaction function for the Blacksmith NPC


# Dictionary to store Player objects, using Discord IDs as keys
players = {}



