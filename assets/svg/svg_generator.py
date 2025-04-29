'''
take block data in
extract 2 data:
    - main block data
    -child data
child data is argument data (text,gap,argument,..)
block use group move to minimize the edit of svg
dict update
'''

from assets.setting import block_setting as bs
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
            temp_data , temp_dict_data = create_child(data.argument_data,x,y,block_data.left+offsetx,max(bs.content_top*2,(h-mh)/2)+offsety,id=random_str.random_string())
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
        "child": children
    }


    return hgw + datas + child_data + "\n" +tgw,dict_data



def z(block_data, x=0, y=0, parent_offset_x=0, parent_offset_y=0):
    if block_data is None:
        return "", None

    block_data.update()

    # Calculate local transform
    hgw = f"""<g transform="translate({x}, {y})">\n"""
    datas = str(block_data) + "\n"

    w = bs.content_pad
    h = block_data.height - block_data.data.connect_height * 2

    mh = max((item.height for item in block_data.child_data), default=0)
    child_group_y = max(bs.content_top * 2, (h - mh) / 2)
    child_svg = f"""<g transform="translate({block_data.left}, {child_group_y})">\n"""

    dict_children = []

    for data in block_data.child_data:
        data.left = w
        data.top = (mh - data.height) / 2
        data.update()

        # Absolute position = all parent offsets + local position
        abs_x = parent_offset_x + x + block_data.left + data.left
        abs_y = parent_offset_y + y + child_group_y + data.top

        if isinstance(data, svg_argument.argument):
            # Recursively get nested argument dictionary
            if data.argument_data is not None:
                child_svg_str, child_dict = z(
                    data.argument_data,
                    x, y,
                    parent_offset_x=abs_x,
                    parent_offset_y=abs_y
                )
                child_svg += child_svg_str
            else:
                child_dict = None

            # Add argument to dictionary
            dict_entry = {
                "type": "argument",
                "x": abs_x,
                "y": abs_y,
                "width": data.width,
                "height": data.height,
                "color": data.color
            }
            if child_dict:
                dict_entry["children"] = [child_dict]

            dict_children.append(dict_entry)

        # Add SVG element
        child_svg += str(data)
        w += data.width

    child_svg += "</g>\n"
    tgw = "</g>"

    svg_output = hgw + datas + child_svg + tgw

    dict_output = None
    if dict_children:
        dict_output = {
            "type": "block",
            "x": parent_offset_x + x,
            "y": parent_offset_y + y,
            "width": block_data.width,
            "height": block_data.height,
            "children": dict_children
        }

    return svg_output, dict_output



def multiblock(block_datas,x=0,y=0):
    x= x
    y= y
    for block_data in block_datas:
        create_child(block_data,x,y)
        y += block_data.height


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


print(create_child(l)[1])
