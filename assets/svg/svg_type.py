from assets.setting import svg_setting as ss
from assets.setting.block_setting import *
from assets.setting.svg_setting import connect_width
from assets.utils import saturation_scale,remove_newline
from assets.debug import svg_debug as sdb

class svg_type():

    def __init__(self,width=default_block_width,height=default_block_height,color="#FFFFFF",border_width = ss.border_width,border_radius=ss.border_radius,connect_width = ss.connect_width,connect_height = ss.connect_height,
                 connect_length = ss.connect_len,head_length = ss.head_len,type=1,top=0,left=0):
        self.type = type
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.color = color
        self.border_color = saturation_scale.adjust_saturation(self.color,scale_factor=0.8,brightness_factor=0.8)
        self.border_width = border_width[self.type]
        self.border_radius = border_radius[self.type]
        self.connect_height = connect_height[self.type]
        self.connect_width = connect_width[self.type]
        self.connect_length = connect_length[self.type]
        self.head_length = head_length[self.type]

        self.type_dict ={1:self.default(),2:self.no_connect()}
    def update(self):
        self.type_dict = {1: self.default(),2:self.no_connect()}
    def default(self)->str:
        #pre-calculate box
        base_height = self.height-self.connect_height-self.border_radius*2-self.border_width
        tail_width2 = self.width-self.head_length-self.border_radius*2-(self.border_radius-2)*2-self.connect_length
        tail_width = self.width-self.head_length-self.border_radius*2-self.connect_length-(self.border_radius-2)*2-self.connect_width*2-10

        print("tail width",tail_width,tail_width2)

        svg = f"""<path fill="{self.color}" d="
        M{self.left} {self.top}
        v{base_height}
        a{self.border_radius} {self.border_radius} 0 0 0 {self.border_radius} {self.border_radius} 
        h{self.head_length}
        l{self.connect_width} -{self.connect_height}
        a{self.border_radius} {self.border_radius} 0 0 1 {self.border_radius} -{self.border_radius-2}
        h{self.connect_length}
        a{self.border_radius} {self.border_radius} 0 0 1 {self.border_radius} {self.border_radius-2}
        l{self.connect_width} {self.connect_height}
        h{tail_width}
        a{self.border_radius} {self.border_radius} 0 0 0 {self.border_radius} -{self.border_radius}
        v-{base_height}
        a{self.border_radius} {self.border_radius} 0 0 0 -{self.border_radius} -{self.border_radius}
        h-{tail_width}
        l-{self.connect_width} -{self.connect_height}
        a{self.border_radius} {self.border_radius} 0 0 0 -{self.border_radius} -{self.border_radius-2}
        h-{self.connect_length}
        a{self.border_radius} {self.border_radius} 0 0 0 -{self.border_radius} {self.border_radius-2}
        l-{self.connect_width} {self.connect_height}
        h-{self.head_length}
        a{self.border_radius} {self.border_radius} 0 0 0 -{self.border_radius} {self.border_radius}"
        stroke="{self.border_color}" stroke-width="{self.border_width}"
        />"""

        return remove_newline.clean_text(svg)+"\n"
    def no_connect(self)->str:
        self.height -= self.border_width*2
        self.width -= self.border_width*2
        print("noconnect",self.border_radius,self.width,self.height,self.width-self.border_radius*2)
        svg  = f"""<path fill="{self.color}" d="
            M{self.left}
            {self.top}
            v{self.height-self.border_radius*2}
            a{self.border_radius}
            {self.border_radius}
            0
            0
            0
            {self.border_radius}
            {self.border_radius}
            h{self.width-self.border_radius*2}
            a{self.border_radius}
            {self.border_radius}
            0
            0
            0
            {self.border_radius}
            -{self.border_radius}
            v -{self.height-self.border_radius*2}
            a{self.border_radius}
            {self.border_radius}
            0
            0
            0
            -{self.border_radius}
            -{self.border_radius}
            h -{self.width-self.border_radius*2}
            a{ss.argument_border_radius}
            {ss.argument_border_radius}
            0
            0
            0
            -{self.border_radius}
            {self.border_radius}
            "
            stroke="{self.border_color}" stroke-width="{self.border_width}"
            />"""

        #stupid ass code
        self.height += self.border_width*2
        self.width += self.border_width*2
        return remove_newline.clean_text(svg)+"\n"

    def __str__(self):
        print(self.width,self.height)
        return self.type_dict[self.type]

    def __add__(self, other):
        return self.__str__() + other


# print(b)
