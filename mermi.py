from ursina import *

class Ball(Entity):
    ball_list = []
    def __init__(self, pos = Vec3(0), speed = 23, dir = Vec3(0), rot=Vec3(0)):
        super().__init__(model='mermi', scale=0.2, position=pos, collider='sphere')
        self.direction = dir
        self.speed = speed
        Ball.ball_list.append(self)
        self.rotation = rot
        self.rotation_x = -10
        return

    def update(self):
        self.position += self.direction * self.speed * time.dt
        self.direction.y += -0.3 * time.dt
        # print(self.position)

        if self.position.y < -20:
            Ball.ball_list.remove(self)
            destroy(self)

if __name__ == "__main__":
    app = Ursina()

    Sky()

    EditorCamera()


    def input(key):
        if key == "space":
            ball = Ball(pos=Vec3(0, -5, 0), speed=15, dir=Vec3(1, 0.5, 0))

    app.run()
