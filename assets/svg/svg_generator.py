'''
take block data in
extract 2 data:
    - main block data
    -child data
child data is argument data (text,gap,argument,..)
block use group move to minimize the edit of svg
dict update
'''

from assets.setting import block_setting as bs , svg_setting as ss
from assets.block import block_data as bd
from assets.svg import svg_type,svg_argument
from assets.utils import random_str


def create_child(block_data,x=0,y=0,offsetx=0,offsety=0,id=None):
    if block_data is None:
        return ""
    hgw = f"""<g transform="translate({x}, {y})"> {"\n"}"""
    block_data.update()
    datas = str(block_data)+"\n"
    w = bs.content_pad
    h = block_data.height-block_data.data.connect_height*2
    print(f"in id {id}" if id is not None else "")
    mh = 0
    for item in block_data.child_data:
        mh = max(mh,item.height)
    child_data = f"""<g transform="translate({block_data.left}, {max(bs.content_top*2,(h-mh)/2)})"> {"\n"}"""
    children = []
    for data in block_data.child_data:
        data.left = w
        data.top = (mh-data.height)/2
        data.update()
        dx = x+data.left+block_data.left+offsetx
        dy = y+data.top+max(bs.content_top*2,(h-mh)/2)+offsety
        if hasattr(data,"_argument_data") and data.argument_data is not None:
            print("skibidi",dx, dy)
            temp_data , temp_dict_data = create_child(data.argument_data,0,0,block_data.left+offsetx,max(bs.content_top*2,(h-mh)/2)+offsety,id=random_str.random_string())
            child_data += temp_data
            children.append(temp_dict_data)
        elif hasattr(data,"_argument_data") and data.argument_data is None:
            print("skibidi2", dx, dy,x,data.left,block_data.left,offsetx,w,f"out id {id}" if id is not None else "")
            temp_dict_data = {
                "x": dx,
                "y": dy,
                "width": block_data.width,
                "height": block_data.height,
                "child": children
            }
            children.append(temp_dict_data)
            child_data += str(data)
        else:
            child_data += str(data)
        w += data.width
    child_data += "</g>"
    tgw = "</g>"
    dict_data = {
        "x":x+offsetx+block_data.left,
        "y":y+offsety+block_data.top,
        "width":block_data.width,
        "height":block_data.height,
        #add type to create interact
        "child": children
    }

    return hgw + datas + child_data + "\n" +tgw,dict_data


def complete_svg(svg,svg_width,svg_height,connect_height,border_width):
    svg_head = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{47.7109375}" height="{svg_height}" viewBox="-{border_width} -{connect_height} {svg_width} {svg_height}" fill="none">"""

    svg_tail = "</svg>"

    return svg_head + svg + svg_tail


def multiblock(block_datas,x=0,y=0):
    x= x
    y= y
    mx = 0
    bouding_list = []
    svg_body = ""
    for block_data in block_datas:

        temp_svg,temp_bb = create_child(block_data,x,y)
        bouding_list.append(temp_bb)
        svg_body += temp_svg +"\n"

        y += block_data.height - ss.connect_height[block_data.type] - ss.border_width[block_data.type]*2
        mx = max(mx,block_data.width)

    # post process
    y += ss.border_width[1]*2
    svg = complete_svg(svg_body,mx,y,ss.connect_height[1]*2+ss.border_width[1]*2,ss.border_width[1])
    return svg , bouding_list , mx, y

a = svg_argument.argument(30,20)
p = svg_argument.argument(30,20)

h = svg_argument.argument(30,20)
h.argument_data=bd.block_data(width=150,height=30,child=[svg_argument.Text("test2"),
                                             svg_argument.gap(20),svg_argument.argument(30,20)])
p.argument_data = bd.block_data(width=150,height=30,child=[svg_argument.Text("test2"),
                                             svg_argument.gap(20),h])

a.argument_data=bd.block_data(width=150,height=30,child=[svg_argument.Text("test2"),
                                             svg_argument.gap(20),p])
l = bd.block_data(width=150,height=50,child=[svg_argument.Text("test"),
                                             svg_argument.gap(20),a
                                             ,
                                             svg_argument.gap(20),
                                             svg_argument.argument(30,20)])
l.update()

import copy
ds = [copy.deepcopy(l),copy.deepcopy(l),copy.deepcopy(l)]

print(multiblock(ds,0,0)[0])
