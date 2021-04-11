import interaction as i
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from random import randint


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
        self.canvas.add(self.ellipse)

    def draw_massive(self):
        self.canvas.add(Color(1, randint(0,1), randint(0,1), 1))
        self.ellipse_c = Ellipse(pos=self.pos, size=self.size)
        self.canvas.add(self.ellipse_c)

    def move_small(self, k):
        self.pos = Vector(self.COORDS_small[k])
        self.ellipse.pos = self.pos


class Move(Widget):
    def __init__(self):
        super(Move, self).__init__()
        self.counter = 0
        self.n = i.T

    def update_small(self, u):
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

    def create_central(self, color, pos, size, vel):
        self.c_object = Object(step=self.n,
                             color=color,
                             pos=pos,
                             vel=vel,
                             size=size)
        self.c_object.draw_massive()
        self.add_widget(self.c_object)


class PlanetApp(App):
    def create_small_object(self, instance):
        self.move = Move()
        self.move.create_small(color=Color(1, randint(0,1), randint(0,1), 1),
                                 pos=(0, 1 * 149 * 10**9),
                                 vel=(randint(-30000,-10000), 0),
                                 size=(8, 8))
        Clock.schedule_interval(self.move.update_small, .04)
        self.main_layout.add_widget(self.move)

    def create_massive_object(self, instance):
        self.c_move = Move()
        self.c_move.create_central(color=Color(1, randint(0,1), randint(0,1), 1),
                                 pos=(i.x_c/i.ae*100+250, i.y_c/i.ae*100+250),
                                 vel=(0, 0),
                                 size=(20, 20))
        self.main_layout.add_widget(self.c_move)

    def build(self):
        self.layout = GridLayout(cols=2, size_hint_y=None)

        self.btn_1 = Button(text='Create small object',
                            on_press=self.create_small_object)
        self.btn_2 = Button(text='Create massive object',
                            on_press=self.create_massive_object)
        self.layout.add_widget(self.btn_1)
        self.layout.add_widget(self.btn_2)

        self.main_layout = GridLayout(rows=2, size_hint_y=None)
        self.main_layout.add_widget(self.layout)
        
        return self.main_layout


PlanetApp().run()
