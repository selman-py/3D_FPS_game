from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint
from mermi import *
from direct.actor.Actor import Actor
from ursina.shaders import basic_lighting_shader as bls, colored_lights_shader as cls
from collider_setup import *

Entity.default_shader = bls

class CustomSky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture="sunset.hdr",
            double_sided=True,
            scale=3000,
            shader=cls
        )


class Enemy(Entity):
    enemy_list = []
    def __init__(self,  move_speed=0.1, collider_speed=1, **kwargs):
        super().__init__(model=None, scale=.7, y=0, collider="box", **kwargs)
        self.actor = Actor("assets/guardian.glb")
        self.actor.reparentTo(self)
        self.actor.loop('Walk')
        self.actor.setPlayRate(0.71, 'Walk')  # Set the animation speed
        self.collider = BoxCollider(self, size=(1, 3, 1))
        self.shader = cls
        self.speed = move_speed  # Movement speed
        self.collider_speed = collider_speed  # Collider speed
        print(self.actor.get_anim_names())
        # self.collider.visible = True
        self.speed = 4

        Enemy.enemy_list.append(self)

    def update(self):
        dist = distance_xz(self, player)

        if dist < 20:
            print_on_screen("BUSTED")
            self.actor.play("attack")
        if dist > 50:
            return

        self.look_at_2d(player, axis="y")
        self.position += self.forward * time.dt * self.speed  # Movement speed multiplier

        for enemy in Enemy.enemy_list:
            if enemy == self: continue
            if distance_xz(self, enemy) < 1:
                self.position -= self.forward * time.dt * self.collider_speed  # Collider speed multiplier

        for b in Ball.ball_list:
            if distance(b, self) < 1:
                self.hit_enemy()

        self.rotation_y += 180

    def hit_enemy(self):
        self.z -= 25


class PhysicsEntity(Entity):
    def __init__(self, model='bomba', collider='box', **kwargs):
        super().__init__(model=model, collider=collider, **kwargs)
        self.velocity = Vec3(0, 0, 0)

    def update(self):
        if self.intersects():
            self.stop()
            return

        self.velocity = lerp(self.velocity, Vec3(0), time.dt)
        self.velocity += Vec3(0, -1, 0) * time.dt * 5
        self.position += (self.velocity + Vec3(0, -4, 0)) * time.dt

    def stop(self):
        self.velocity = Vec3(0, 0, 0)

    def throw(self, direction, force):
        self.velocity = direction * force


def input(key):
    if key == 'left mouse down':
        dir = camera.forward + Vec3(0, 0.01, 0)
        pos = player.position + player.forward + Vec3(0, 1.6, 0)
        ball = Ball(pos=pos, speed=15, dir=dir, rot=player.rotation)
        ball.shader = bls
    elif key == '3':
        bomba_Shoot()


def bomba_Shoot():
    bomb = PhysicsEntity(model='bomba', scale=1, position=player.position + Vec3(0, 1.5, 0) + player.forward, collider='sphere')
    bomb.throw(camera.forward + Vec3(0, 0.5, 0), 10)


app = Ursina(borderless=False)

sky = CustomSky()

arena = Entity(model="map6", scale=350, y=-34.5) #harita14

ground = Entity(model="plane", scale=300, y=0, texture="grass", color=color.lime)
ground_box = Entity(model="plane", scale=300, y=-1.5, collider="box")

player = FirstPersonController(x=-10, origin_y=-.5, speed=3)
player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))

# Gun setup with model 'gun3'
gun = Entity(model='gun3', parent=camera, position=(.5, -.25, .25), scale=(.3, .2, 1), origin_z=-.5, on_cooldown=False)
gun.muzzle_flash = Entity(parent=gun, z=8, y=1, x=5, world_scale=.5, model='quad', color=color.yellow, enabled=False)

shootables_parent = Entity()
mouse.traverse_target = shootables_parent

def update():
    if held_keys['left mouse']:
        shoot()
    for enemy in Enemy.enemy_list:
        if not enemy.actor.getCurrentAnim():
            enemy.actor.loop("Walk")


def shoot():
    if not gun.on_cooldown:
        gun.on_cooldown = True
        gun.muzzle_flash.enabled = True
        from ursina.prefabs.ursfx import ursfx
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise',
              pitch=random.uniform(-13, -12), pitch_change=-12, speed=3.0)
        invoke(gun.muzzle_flash.disable, delay=.05)
        invoke(setattr, gun, 'on_cooldown', False, delay=.15)
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            mouse.hovered_entity.hp -= 10
            mouse.hovered_entity.blink(color.red)


enemies = [Enemy(x=x * 20, anim_speed=0.5, move_speed=0.1, collider_speed=0.05) for x in range(5)]  # Düşmanların animasyon, hareket ve collider hızlarını azaltmak için değerler eklendi

setup_scene("assets\colliders.json", 350)

#EditorCamera()

app.run()
