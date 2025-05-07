from assets.setting import block_setting as bs
from assets.svg import svg_type as st
class block_data:

    def __init__(self,width=0,height=0,top=0,left=0,color="#FFFFFF",type=1,child=[]):

        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.color = color
        self.type = type

        self.data =  st.svg_type(width=self.width,height=self.height,color=self.color,type=self.type)#svg type

        self.child_data = child
        self.update()

    def update(self):
        width = 0
        height = 0
        self.data.update()
        for child in self.child_data:

            child.update()
            width += child.width

            height = max(child.height+ bs.content_top*2,height)
        height += self.data.connect_height*2 + self.data.border_width*2

        self.width = width +self.data.border_width*2+bs.content_pad*2

        self.height = max(height,50) if self.type == 1 else max(height,40)
        #print("data connect heiht", self.data.connect_height,self.height)
        self.data = st.svg_type(width=self.width, height=self.height, color=self.color, type=self.type,top=self.top,left=self.left)


    def __str__(self):
        return str(self.data)
    def __add__(self, other):
        return str(self.data) + other


