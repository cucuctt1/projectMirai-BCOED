

'''custom stack '''


import flet as ft


class block_display:
    def __init__(self,width,height,left = 0,top = 0):
        self.width = width
        self.height = height
        self.top = top
        self.left = left



        self.main_stack = ft.Stack(width = self.width,height= self.height,left = 0,top = 0)
        self.top_stack = ft.Stack(width = self.width,height= self.height,left = 0,top = 0)

        self.substorestack = ft.Stack(width = self.width,height= self.height,controls=[self.main_stack,self.top_stack])
        self.store_stack = ft.Container(width=self.width, height=self.height, content=self.substorestack)

    def installize(self,page,updater=None,sector = None):
        page.add(self.store_stack)

        if updater:
            updater.add_to_sector(sector,self.store_stack)
            updater.add_to_sector(sector,self.main_stack)
            updater.add_to_sector(sector, self.top_stack)

    def remove(self,item):
        if item in self.main_stack.controls:
            self.main_stack.controls.remove(item)
        else:
            print("no item in stack")



