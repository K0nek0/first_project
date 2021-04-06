import interaction as i
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button


class Object(Widget):
    def __init__(self, **kw):
        super(Object, self).__init__()

        self.step = kw['step']
        self.color = kw['color']
        self.pos = kw['pos']
        self.vel = kw['vel']
        self.size = kw['size']
        self.COORDS_small = []

        self.interect_small = i.Interaction_small(x0=self.pos[0],
                                                  vx0=self.vel[0],
                                                  y0=self.pos[1],
                                                  vy0=self.vel[1])

        for j in range(self.step):
            self.COORDS_small.append(
                (float(self.interect_small.solve_func()[0][j]) * 100 + 250,
                 float(self.interect_small.solve_func()[1][j]) * 100 + 250))


    def draw_small(self):
        self.canvas.add(self.color)
        self.ellipse = Ellipse(pos=self.pos, size=self.size)
        self.ellipse_c = Ellipse(pos=(250, 250), size=(20, 20))
        self.canvas.add(self.ellipse)
        self.canvas.add(self.ellipse_c)

    def move_small(self, k):
        self.pos = Vector(self.COORDS_small[k])
        self.ellipse.pos = self.pos


class Move(Widget):
    def __init__(self):
        super(Move, self).__init__()
        self.counter = 0
        self.n = i.T

    def update_small(self, dt):
        if self.counter == self.n - 1:
            self.counter = 0
        self.counter += 1
        self.object.move_small(self.counter)

    def create_small(self, color, pos, size, vel):
        self.object = Object(step=self.n,
                             color=color,
                             pos=pos,
                             vel=vel,
                             size=size)
        self.object.draw_small()
        self.add_widget(self.object)


class PlanetApp(App):
    def create_small_object(self, instance):
        self.object = Move()
        self.object.create_small(color=Color(1, 0, 0),
                                 pos=(0, 1 * 149 * 10**9),
                                 vel=(-30000, 0),
                                 size=(8, 8))
        Clock.schedule_interval(self.object.update_small, .04)
        self.parent.add_widget(self.object)

    def build(self):
        self.parent = Widget()
        self.btn_1 = Button(text='Create small object',
                            on_press=self.create_small_object)
        self.parent.add_widget(self.btn_1)

        return self.parent


PlanetApp().run()
