from ursina import *
from main import *
from mermi import *

physics_entities = []
class PhysicsEntity(Entity):
    def __init__(self, model='bomba', collider='box', **kwargs):
        super().__init__(model=model, collider=collider, **kwargs)
        physics_entities.append(self)

    def update(self):
        if self.intersects():
            self.stop()
            return

        self.velocity = lerp(self.velocity, Vec3(0), time.dt)
        self.velocity += Vec3(0,-1,0) * time.dt * 5
        self.position += (self.velocity + Vec3(0,-4,0)) * time.dt


    def stop(self):
        self.velocity = Vec3(0,0,0)
        if self in physics_entities:
            physics_entities.remove(self)

    def on_destroy(self):
        self.stop()


    def throw(self, direction, force):
        pass

from ursina.shaders import lit_with_shadows_shader
Entity.default_shader = lit_with_shadows_shader
DirectionalLight().look_at(Vec3(1,-1,-1))

#ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=Vec2(32), collider='box')

if __name__ == "__main__":
    app = Ursina()

    Sky()

def input(key):
    if key == 'right mouse down':
        e = PhysicsEntity(model='bomba', velocity=Vec3(0), scale =1 ,position=player.position+Vec3(0,1.5,0)+player.forward, collider='sphere')
        e.velocity = (camera.forward + Vec3(0,.5,0)) * 10
        # physics_entities.append(e)

app.run()