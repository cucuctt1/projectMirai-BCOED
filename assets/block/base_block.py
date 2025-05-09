import flet as ft


from assets.block import drag_module as dm
from assets.debug.id_getter import *
from assets.utils.random_str import *
from assets.svg import svg_generator as sg
from assets.control import interact_check as ic
from assets.utils import element_filter as ele_fil
from assets.svg import svg_argument as sa

class Base(dm.drag_module):
    def __init__(self,width=150,height=50,left = 0,top =10,stack = None):
        super().__init__()
        self.width = width
        self.height = height
        self.top = top
        self.left =left
        self.block_dict = []
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
        #string to svg
        svg = ft.Image(src=content,width=self.width,height=self.height)
        self.content = svg



    def add_data(self,block_data):
        self.block_data = block_data
        content ,boudingbox,maxwidth,maxheight = sg.multiblock(block_data,0,0)

        self.width = maxwidth
        self.height = maxheight
        self.add(content)
        self.block_dict = boudingbox

    def update_content(self):
        content, boudingbox, maxwidth, maxheight = sg.multiblock(self.block_data, 0, 0)
        self.width = maxwidth
        self.height = maxheight
        self.add(content)
        self.block_dict = boudingbox

    def updateWNH(self):
        self.width = self.content.width
        self.height = self.content.height


    def update_dict(self):
        pass

    def start_drag(self ,e):

        px,py = e.global_x-self.left,e.global_y-self.top-5
        impact = None
        pos = (None,None)
        #print(self.block_dict[0]["child"][0]["child"][0]["child"][0]["child"][0]["child"])
        if self.child is None:
            indice = 0
            for data in self.block_dict:
                impact,layer = ic.interact_check(px,py,data,0,[])
                if impact:
                    data = self.block_data[layer[0]]
                    if len(layer) >= 2:
                        for index in layer[1:]:
                            data = data.child_data
                            filterd_ele = ele_fil.filter(data,sa.argument)
                            if filterd_ele[index].argument_data:
                                data = filterd_ele[index].argument_data
                            else:
                                pass
                    break


            #impact,pos = impact_check(self.block_dict,point)

        if indice == 0:
            indice = None
        if impact is not None and pos[0] is not None:

            #get data

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
                    # impact,pos = impact_check(item.block_dict,((self.left+10)-item.left,(self.top-15)-item.top))
                    # if impact is not None:
                    #     block_data = item.block_data
                    #     block_data[impact+1:impact+1] = self.block_data
                    #     item.add_data(block_data)
                    #     self.add_data([])
                    #
                    #     break
                    pass

            super().end_drag(e)
        elif self.child is not None:
            self.child.end_drag(e)

        self.child = None
        self.selected = False
        if not self.block_data:
            self.stack.remove(self)
            del self



