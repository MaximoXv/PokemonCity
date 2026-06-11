class Pokemon:

    HATCHING = "hatching"
    IDLE = "idle"
    DEAD = "dead"

    def __init__(self, name, pokemon_type):

        self.name = name
        self.type = pokemon_type

        self.level = 1

        self.max_hp = 100
        self.hp = self.max_hp

        self.food = 0

        self.state = Pokemon.HATCHING

        self.hatch_timer = 30

        self.habitat = None

    def food_required(self):

        return 10 ** self.level

    def feed(self, amount):

        if self.state == Pokemon.DEAD:
            return

        self.food += amount

        while self.food >= self.food_required():

            self.food -= self.food_required()

            self.level += 1

    def take_damage(self, damage):

        if self.state == Pokemon.DEAD:
            return

        self.hp -= damage

        if self.hp <= 0:

            self.hp = 0

            self.state = Pokemon.DEAD

            if self.habitat:
                self.habitat.remove_pokemon(self)

    def heal(self, amount):

        if self.state == Pokemon.DEAD:
            return

        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def update(self, dt):

        if self.state == Pokemon.HATCHING:

            self.hatch_timer -= dt

            if self.hatch_timer <= 0:

                self.state = Pokemon.IDLE