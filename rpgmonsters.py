import random

# Health and Attack Ranges for existing monsters
GOBLIN_HEALTH_RANGE = (20, 30)
GOBLIN_ATTACK_RANGE = (5, 10)

ORC_HEALTH_RANGE = (30, 40)
ORC_ATTACK_RANGE = (10, 15)

DRAGON_HEALTH_RANGE = (50, 80)
DRAGON_ATTACK_RANGE = (15, 20)

TROLL_HEALTH_RANGE = (60, 80)
TROLL_ATTACK_RANGE = (20, 30)

WOLF_HEALTH_RANGE = (15, 25)
WOLF_ATTACK_RANGE = (8, 12)

BANDIT_HEALTH_RANGE = (25, 35)
BANDIT_ATTACK_RANGE = (10, 20)

# Health and Attack Ranges for new monsters
SKELETON_HEALTH_RANGE = (20, 25)
SKELETON_ATTACK_RANGE = (7, 12)

WRAITH_HEALTH_RANGE = (40, 50)
WRAITH_ATTACK_RANGE = (12, 18)

SPIDER_HEALTH_RANGE = (25, 30)
SPIDER_ATTACK_RANGE = (9, 15)

BUNNY_HEALTH_RANGE = (15, 15)
BUNNY_ATTACK_RANGE = (5, 5)


class Monster:
    """
    Represents a generic monster in the game.

    Attributes:
        name (str): The name of the monster.
        health (int): The current health points of the monster.
        attack (int): The damage the monster can inflict in an attack.
    """

    def __init__(self, name, health, attack, experience_value):
        """
        Initializes a new Monster instance.

        Args:
            name (str): The name of the monster.
            health (int): The initial health points of the monster.
            attack (int): The initial attack damage of the monster.
        """
        self.name = name
        self.health = health
        self.attack = attack
        self.experience_value = experience_value

    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0

    def special_ability(self):
        """
        Defines the special ability of the monster.

        Returns:
            str: A message describing the special ability.
        """
        return "No special ability."


class Bandit(Monster):
    def __init__(self):
        super().__init__("Bandit", random.randint(*BANDIT_HEALTH_RANGE), random.randint(*BANDIT_ATTACK_RANGE),
                         experience_value=25)

    def special_ability(self):
        # Implement a special ability unique to Bandits
        if random.random() < 0.3:
            # 30% chance of success for the special ability
            return "Threw a smoke bomb and disappeared!"
        else:
            return "Tried to use a smoke bomb, but failed."


class Goblin(Monster):
    def __init__(self):
        super().__init__("Goblin", random.randint(*GOBLIN_HEALTH_RANGE), random.randint(*GOBLIN_ATTACK_RANGE),
                         experience_value=10)

    def special_ability(self):
        # Implement a special ability unique to Goblins
        if random.random() < 0.3:
            # 30% chance of success for the special ability
            return "Used a sneaky trick and stunned you!"
        else:
            return "Tried to use a sneaky trick, but failed."


class Wolf(Monster):
    def __init__(self):
        super().__init__("Wolf", random.randint(*WOLF_HEALTH_RANGE), random.randint(*WOLF_ATTACK_RANGE),
                         experience_value=15)

    def special_ability(self):
        # Implement a special ability unique to Wolves
        if random.random() < 0.2:
            # 20% chance of success for the special ability
            damage_boost = random.randint(5, 10)
            self.attack += damage_boost
            return f"Enraged and gained {damage_boost} attack power!"
        else:
            return "Tried to go into a frenzy, but remained calm."


class Bunny(Monster):
    def __init__(self):
        super().__init__("Bunny", random.randint(*BUNNY_HEALTH_RANGE), random.randint(*BUNNY_ATTACK_RANGE),
                         experience_value=35)

    def special_ability(self):
        # Implement the Bunny's special ability to multiply (duh!)
        multiplicity = random.randint(1, 3)
        self.health += self.health * multiplicity
        return f"Multiplied! The bunny now has {self.health} health"


class Orc(Monster):
    def __init__(self):
        super().__init__("Orc", random.randint(*ORC_HEALTH_RANGE), random.randint(*ORC_ATTACK_RANGE),
                         experience_value=20)

    def special_ability(self):
        # Implement a special ability unique to Orcs
        if random.random() < 0.2:
            # 20% chance of success for the special ability
            damage_boost = random.randint(5, 15)
            self.attack += damage_boost
            return f"Enraged and gained {damage_boost} attack power!"
        else:
            return "Tried to go into a frenzy, but remained calm."


class Dragon(Monster):
    def __init__(self):
        super().__init__("Dragon", random.randint(*DRAGON_HEALTH_RANGE), random.randint(*DRAGON_ATTACK_RANGE),
                         experience_value=50)

    def special_ability(self):
        # Implement a special ability unique to Dragons
        if random.random() < 0.25:
            # 25% chance of success for the special ability
            fire_damage = random.randint(10, 20)
            return f"Breathed fire and dealt {fire_damage} damage to you!"
        else:
            return "Breathed fire but missed."


class Troll(Monster):
    def __init__(self):
        super().__init__("Troll", random.randint(*TROLL_HEALTH_RANGE), random.randint(*TROLL_ATTACK_RANGE),
                         experience_value=30)

    def special_ability(self):
        # Implement the Troll's special ability to regenerate health
        health_regeneration = random.randint(5, 10)
        self.health += health_regeneration
        return f"Regenerated {health_regeneration} health."


class Skeleton(Monster):
    def __init__(self):
        super().__init__("Skeleton", random.randint(*SKELETON_HEALTH_RANGE), random.randint(*SKELETON_ATTACK_RANGE),
                         experience_value=15)

    def special_ability(self):
        # Implement a special ability unique to Skeletons
        if random.random() < 0.2:
            # 20% chance of success for the special ability
            dodge_chance = random.random()
            if dodge_chance < 0.5:
                return "Dodged your attack with its agility!"
            else:
                return "Tried to dodge, but failed."
        else:
            return "Tried to dodge, but failed."


class Wraith(Monster):
    def __init__(self):
        super().__init__("Wraith", random.randint(*WRAITH_HEALTH_RANGE), random.randint(*WRAITH_ATTACK_RANGE),
                         experience_value=35)

    def special_ability(self):
        # Implement a special ability unique to Wraiths
        if random.random() < 0.3:
            # 30% chance of success for the special ability
            return "Turned ethereal and became immune to your attack!"
        else:
            return "Tried to become ethereal, but failed."


class GiantSpider(Monster):
    def __init__(self):
        super().__init__("Giant Spider", random.randint(*SPIDER_HEALTH_RANGE), random.randint(*SPIDER_ATTACK_RANGE),
                         experience_value=25)

    def special_ability(self):
        # Implement a special ability unique to Giant Spiders
        if random.random() < 0.25:
            # 25% chance of success for the special ability
            venom_damage = random.randint(5, 15)
            return f"Injected venom and dealt {venom_damage} poison damage to you!"
        else:
            return "Tried to inject venom, but missed."

# You can create instances of these new monsters as needed.

# Example usage:
# skeleton = Skeleton()
# wraith = Wraith()
# spider = GiantSpider()
