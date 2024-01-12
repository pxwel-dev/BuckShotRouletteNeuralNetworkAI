import random


class Player:
    def __init__(self, name):
        self.name = name
        self.opponent = None
        self.health = 6
        self.is_cuffed = False
        self.cuff_count = 0
        self.items = []
        self.liveShells = None
        self.blankShells = None
        self.shotgunDamage = None
        self.nextShell = None

    def get_item(self, items: list):
        random.seed()
        item = random.choice(items)
        self.items.append(item)
        # print('Player {0} collects {1} item!'.format(self.name, item.name))

    def use_item(self, item):
        self.items.remove(item)
        # print('Player {0} uses {1} item!'.format(self.name, item.name))
        return item

    def regen_health(self):
        if self.health < 6:
            self.health += 1
        #     print('Player {0} regens 1 HP! HP Left: {1}'.format(self.name, self.health))
        # else:
        #     print('Player {0} Already has max HP!'.format(self.name))

    def take_damage(self, damage: int):
        self.health -= damage
        # print('Player {0} takes {1} damage! HP Left: {2}'.format(self.name, damage, self.health))

    def view_current_shell(self, shell: int):
        self.nextShell = shell

    def get_cuffed(self, cuffed: bool):
        if cuffed:
            pass
            # print('Player {0} gets handcuffed for 1 turn!'.format(self.name))
        elif not cuffed:
            self.cuff_count = 0
            # print("Player {0}'s handcuffs come off'!".format(self.name))
        self.is_cuffed = cuffed

    def has_lost(self):
        if self.health <= 0:
            return True
        else:
            return False

    def make_move(self):
        pass

    def reset_player(self):
        self.health = 6
        self.is_cuffed = False
        self.items = []
        self.nextShell = None


class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def view_current_shell(self, shell: int):
        self.nextShell = shell
        if self.nextShell == 1:
            print("Current shell: LIVE")
        elif self.nextShell == 0:
            print("Current shell: BLANK")

    def make_move(self):
        while True:
            move = int(input(
                """
Make your move:
1) Shoot Opponent
2) Shoot Self
3) Use Item
"""))
            if move == 1 or move == 2:
                return move
            elif move == 3:
                break
            else:
                print("Please choose a valid option!")

        while True:
            item_list = [item.name for item in self.items]
            chosen_item_name = input(
                """
Which item:
{0}
""".format(item_list))
            for item in self.items:
                if item.name == chosen_item_name:
                    return self.use_item(item)
            print("Please choose a valid option!")


class NEATPlayer(Player):
    def __init__(self, name, neuralNet):
        Player.__init__(self, name)
        self.neuralNetwork = neuralNet

    def check_item(self, item_name, b: bool):
        for item in self.items:
            if item.name == item_name and b is True:
                return self.use_item(item)
            elif item.name == item_name and b is False:
                return True
        return None

    def format_inputs(self):
        live_shell_chance = 0
        if self.liveShells > 0:
            live_shell_chance = self.liveShells / self.liveShells + self.blankShells
        if self.nextShell is not None:
            live_shell_chance = self.nextShell
        inputs = [live_shell_chance,
                  self.shotgunDamage - 1,
                  self.health / 6,
                  self.opponent.health / 6,
                  1 if self.check_item('Cigs', False) else 0,
                  1 if self.check_item('Soda', False) else 0,
                  1 if self.check_item('Cuffs', False) else 0,
                  1 if self.check_item('Saw', False) else 0,
                  1 if self.check_item('Glass', False) else 0]
        return self.neuralNetwork.activate([*inputs])

    def select_move(self, outputs):
        while True:
            decision = outputs.index(max(outputs))
            if decision == 0:
                return 1
            elif decision == 1:
                return 2
            elif decision == 2:
                use_item = None
                if self.health < 6:
                    use_item = self.check_item('Cigs', True)
                if use_item is None:
                    outputs[2] = -1
                else:
                    return use_item
            elif decision == 3:
                use_item = self.check_item('Soda', True)
                if use_item is None:
                    outputs[3] = -1
                else:
                    return use_item
            elif decision == 4:
                use_item = None
                if not self.opponent.is_cuffed:
                    use_item = self.check_item('Cuffs', True)
                if use_item is None:
                    outputs[4] = -1
                else:
                    return use_item
            elif decision == 5:
                use_item = None
                if self.shotgunDamage != 2:
                    use_item = self.check_item('Saw', True)
                if use_item is None:
                    outputs[5] = -1
                else:
                    return use_item
            elif decision == 6:
                use_item = None
                if self.nextShell is None:
                    use_item = self.check_item('Glass', True)
                if use_item is None:
                    outputs[6] = -1
                else:
                    return use_item
            else:
                print("ISSUE: ", decision, outputs)

    def make_move(self):
        return self.select_move(self.format_inputs())


# class AlgorithmicPlayer(Player):
#     def __init__(self, name):
#         Player.__init__(self, name)
