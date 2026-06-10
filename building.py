class Building:

    def __init__(self, build_time):

        self.state = "building"

        self.build_timer = build_time

    def update(self, dt):

        if self.state == "building":

            self.build_timer -= dt

            if self.build_timer <= 0:

                self.state = "idle"