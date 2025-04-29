
'''the drag part of the program'''

import flet as ft
from assets.utils import cloner ,random_color

class tempblock(ft.GestureDetector):
    def __init__(self ,width ,height ,top ,left ,content):
        super().__init__()
        self.width = width
        self.left = left
        self.content = content
        self.top = top
        self.height = height
        self.on_pan_start = self.dummy


    def dummy(self ,e):
        pass

class drag_module(ft.GestureDetector):
    def __init__(self ,width=0 ,height=0 ,left = 0 ,top = 0 ,stack = None):
        super().__init__()
        self.width = width
        self.height = height
        self.left = left
        self.top = top


        if stack:
            self.mainstack = stack.main_stack
            self.topstack = stack.top_stack
            self.mainstack.controls.append(self)

        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.end_drag
        

        self.tempo = None


    def start_drag(self ,e):
        tempo = cloner.clone_widget(self.content)
        self.tempo = tempblock(self.width ,self.height ,top = self.top ,left=self.left ,content=tempo)
        # debug
        self.topstack.controls.append(self.tempo)
        # create tempo

        pass

    def drag(self ,e):
        delta_x ,delta_y = e.delta_x ,e.delta_y

        self.top += delta_y
        self.left += delta_x

        # update tempo
        if self.tempo != None:
            self.tempo.top = self.top
            self.tempo.left = self.left



    def end_drag(self ,e):
        if self.tempo != None:
            self.topstack.controls.remove(self.tempo)
        # delete tempo

        pass

    def assign_content(self ,content):
        self.content = content

    def installize(self ,updater = None ,sector = None):
        if updater:
            updater.add_to_sector(sector ,self)

    def update_status(self):
        if self.content != None:
            self.height = self.content.height
            self.width = self.content.width