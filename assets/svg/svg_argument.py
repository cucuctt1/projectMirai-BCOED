import assets.block.block_data
from assets.utils.text_size import measure_text_skia as ctw


class Text():
    def __init__(self,value="",color="#000000",top=0,left=0,font_size=16):

        self.value = value
        self.text_color = color
        self.top = top
        self.left = left
        self.font_size = font_size
        self.width ,self.height = 0,0

        self.data = ""
        self.update()

    def update(self):
        self.width, self.height = ctw(self.value, self.font_size)
        self.data = f"""<text x="{self.left}" y="{self.top}" fill="{self.text_color}" font-family="Arial"> {self.value}</text> \n"""

    def __str__(self):
        return str(self.data)

    def __add__(self, other):
        return str(self.data) + other


class gap():
    def __init__(self,width=20):
        self.width = width
        self.height = 1
        self.top = 0
        self.left = 0

    def __str__(self):
        return ""
    def __add__(self,other):
        return other
    def update(self):
        pass

from assets.svg import svg_type
class argument():
    def __init__(self,width=0,height=0,top=0,left=0,color="#ffffff"):

        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.color = color

        self._argument_data = None # block data only
        self.data = {False:svg_type.svg_type(width=self.width,height=self.height,color=self.color,type=2,top=self.top,left=self.left)
        ,True:self._argument_data}
        self.update()

    def update(self):


        self.data = {
            False: svg_type.svg_type(width=30, height=20, color=self.color, type=2, top=self.top,
                                     left=self.left)
            , True: self._argument_data}
        if self._argument_data is not None:
            self.width = self._argument_data.width
            self.height = self._argument_data.height
            self._argument_data.top = self.top
            self._argument_data.left =self.left
            self.color = self._argument_data.color


    @property
    def argument_data(self):
        self.update()
        return self._argument_data

    @argument_data.setter
    def argument_data(self,value:assets.block.block_data.block_data):
        value.type = 2
        value.top = self.top
        value.left = self.left
        value.update()
        #print("value",value.height,value.data.connect_height)
        self._argument_data = value
        self.update()

    def __str__(self):
        return str(self.data[self._argument_data is not None])

    def __add__(self,other):
        return str(self.data[self._argument_data is not None]) + other