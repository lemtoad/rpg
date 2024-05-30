import random
import asyncio
from discord import Embed  # Import only Embed for Discord interactions

from rpg.rpgitems import items  # Assuming this module properly handles RPG items


class CombatHandler:
    def __init__(self, player, monster, ctx):
        self.player = player
        self.monster = monster
        self.ctx = ctx
        self.combat_log = []

    async def start_combat(self):
        await self.announce_combat_start()
        await self.execute_combat_rounds()

    async def execute_combat_rounds(self):
        round_counter = 0
        while self.monster.is_alive() and self.player.current_health > 0:
            await self.execute_round()
            round_counter += 1
            if round_counter % 5 == 0 or not self.monster.is_alive() or self.player.current_health <= 0:
                await self.flush_combat_log()

    async def execute_round(self):
        await self.player_turn()
        await asyncio.sleep(2)
        if self.monster.is_alive():
            await self.monster_turn()
            await asyncio.sleep(2)

    async def flush_combat_log(self):
        if self.combat_log:
            embed = Embed(title="Combat Log", description="\n".join(self.combat_log), color=0x00ff00)
            await self.ctx.send(embed=embed)
            self.combat_log = []

    async def announce_combat_start(self):
        message = f"{self.ctx.author.mention}, you encountered a {self.monster.name} with {self.monster.health} health!"
        self.combat_log.append(message)

    async def player_turn(self):
        attack_damage = self.calculate_attack_damage(self.player)
        self.monster.health -= attack_damage
        self.combat_log.append(
            f"You attacked {self.monster.name} for {attack_damage} damage. Remaining health: {self.monster.health}")

    async def monster_turn(self):
        if not self.monster.is_alive():
            return
        special_ability_result = self.monster.special_ability()
        self.combat_log.append(f"The {self.monster.name} {special_ability_result}")

        if "damage" in special_ability_result:
            # Extract damage from the ability result if applicable
            damage = int(special_ability_result.split()[-2])  # Assumes the second last word is the damage
            self.player.current_health -= damage
        else:
            attack_damage = self.calculate_attack_damage(self.monster)
            self.player.current_health -= attack_damage
            self.combat_log.append(
                f"The {self.monster.name} attacked you for {attack_damage} damage. Your remaining health: {self.player.current_health}")

    def calculate_attack_damage(self, attacker):
        if hasattr(attacker, 'attack'):
            attack_range = range(attacker.attack - 5, attacker.attack + 5)
            if hasattr(attacker, 'equipment') and attacker.equipment.get('weapon'):
                weapon_damage = items[attacker.equipment['weapon']]['damage']
                attack_range = range(weapon_damage - 5, weapon_damage + 5)
        else:
            # Fallback if no specific attack value is defined
            attack_range = range(1, 11)  # Default attack range for entities without attack attribute

        attack_damage = random.choice(list(attack_range))
        return attack_damage

    async def end_combat(self):
        winner = "player" if self.monster.current_health <= 0 else "monster"
        if winner == "monster":
            self.player.reset_stats()  # Reset the player's stats if they lost the combat
            xp_gain = 0  # Player gains no experience if they die
            combat_message = "You were defeated and your stats have been reset."
        else:
            xp_gain = self.calculate_exp_gain(winner)  # Calculate experience gain for winning
            combat_message = f"You defeated the {self.monster.name} and gained {xp_gain} EXP!"
            self.player.gain_exp(xp_gain)  # Player gains experience if they won

        # Send an embed with the combat results
        embed = Embed(title="Combat Results", description=combat_message,
                      color=0xff0000 if winner == "monster" else 0x00ff00)
        await self.ctx.send(embed=embed)

    def calculate_exp_gain(self, winner):
        return self.monster.experience_value if winner == "player" else 0
