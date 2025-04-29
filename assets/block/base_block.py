import flet as ft
from assets.block import drag_module as dm
from assets.debug.id_getter import *
from assets.utils.random_str import *

def impact_check(position_dict,point):
    px, py = point
    for key, (x, y, x2, y2) in position_dict.items():
        if x <= px <= x2 and y <= py <= y2:
            return key,(x,y)
    return None,(None,None)

class Base(dm.drag_module):
    def __init__(self,width=150,height=50,left = 0,top =10,stack = None):
        super().__init__()
        self.width = width
        self.height = height
        self.top = top
        self.left =left
        self.block_dict = {}
        self.block_data = []
        #self.block_data = sg.d
        self.id = random_string()
        self.stack = stack
        self.child = None
        self.selected = False
        if stack:
            self.mainstack = stack.main_stack
            self.topstack = stack.top_stack
            self.mainstack.controls.append(self)

        #self.test()

    def add(self,content):
        self.content = content
        self.update_dict()
        self.updateWNH()


    def add_data(self,block_data):
        pass

    def updateWNH(self):
        self.width = self.content.width
        self.height = self.content.height


    def update_dict(self):
        pass

    def start_drag(self ,e):

        point = e.global_x-self.left,e.global_y-self.top-15
        impact = None
        pos = (None,None)

        if self.child is None:
            impact,pos = impact_check(self.block_dict,point)

        if impact ==0:
            impact = None
        if impact is not None and pos[0] is not None:
            splited_data = self.block_data[impact:]
            self.add_data(self.block_data[:impact])
            new_block = Base(width = self.width,height = self.height,left=self.left,top=pos[1]+self.top,stack=self.stack)
            new_block.add_data(splited_data)
            new_block.selected = True
            self.child = new_block
            self.child.start_drag(e)

        else:
            self.selected = True

        if self.selected and self.child is None:
            super().start_drag(e)

    def drag(self ,e):
        
        if self.child is None:
            super().drag(e)
        else:
            self.child.drag(e)


    def end_drag(self ,e):
        if self.child is None:
            for item in self.stack.main_stack.controls:
                if item != self:
                    #normalize the pos
                    impact,pos = impact_check(item.block_dict,((self.left+10)-item.left,(self.top-15)-item.top))
                    if impact is not None:
                        block_data = item.block_data
                        block_data[impact+1:impact+1] = self.block_data
                        item.add_data(block_data)
                        self.add_data([])

                        break

            super().end_drag(e)
        elif self.child is not None:
            self.child.end_drag(e)

        self.child = None
        self.selected = False
        if not self.block_data:
            self.stack.remove(self)
            del self



