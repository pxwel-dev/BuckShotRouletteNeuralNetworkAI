import random

from overrides import overrides

from SimPlayers import Player


class Item:
    def __init__(self, name):
        self.name = name

    def use_item(self):
        pass
        # Use the item.


class Shotgun:
    def __init__(self):
        self.chamber_size = 8
        self.chamber = []
        self.damage = 1
        self.live_shells = 0
        self.blank_shells = 0

    def load_chamber(self):
        random.seed()
        self.chamber_size = random.randint(2, 8)
        while len(self.chamber) != self.chamber_size:
            self.chamber.append(random.randint(0, 1))
        self.live_shells = self.chamber.count(1)
        self.blank_shells = self.chamber.count(0)

    def pop_current_shell(self):
        shell = self.chamber.pop(0)
        if shell == 1:
            self.live_shells -= 1
        elif shell == 0:
            self.blank_shells -= 1
        else:
            Exception("You've Successfully Broken The Game!! Congrats Dickhead!!")
        return shell

    def fire_gun(self, target: Player):
        shell = self.pop_current_shell()
        if shell == 1:
            # print("LIVE BULLET IS FIRED")
            target.take_damage(self.damage)
            return True
        elif shell == 0:
            # print("BLANK BULLET IS FIRED")
            return False
        else:
            Exception("You've Successfully Broken The Game!! Congrats Dickhead!!")

    def reset_damage(self):
        self.damage = 1

    def reset_gun(self):
        self.chamber.clear()
        self.reset_damage()
        self.live_shells = 0
        self.blank_shells = 0


class Soda(Item):
    def __init__(self, name):
        Item.__init__(self, name)

    @overrides(check_signature=False)
    def use_item(self, gun: Shotgun):
        shell = gun.pop_current_shell()
        # if shell == 1:
        #     print("A live shell pops out!")
        # elif shell == 0:
        #     print("A blank shell pops out!")
        # Cocks the shotgun to reveal shell


class MagnifyingGlass(Item):
    def __init__(self, name):
        Item.__init__(self, name)

    @overrides(check_signature=False)
    def use_item(self, player: Player, gun: Shotgun):
        player.view_current_shell(gun.chamber[0])
        # print("Player {0} views the current shell!".format(player.name))
        # Reveals current shell in shotgun


class HandSaw(Item):
    def __init__(self, name):
        Item.__init__(self, name)

    @overrides(check_signature=False)
    def use_item(self, gun: Shotgun):
        gun.damage = 2
        # print("Shotgun does twice the damage now!")
        # Shotgun does double the damage


class Cigarette(Item):
    def __init__(self, name):
        Item.__init__(self, name)

    @overrides(check_signature=False)
    def use_item(self, player: Player):
        player.regen_health()
        # Takes the edge off - player heals 1 hp


class HandCuffs(Item):
    def __init__(self, name):
        Item.__init__(self, name)

    @overrides(check_signature=False)
    def use_item(self, opponent: Player):
        opponent.get_cuffed(True)
        # Opponent has to skip a turn
