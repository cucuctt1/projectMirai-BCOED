
#return true if impact
#recusion to search for deepest
#early return

def interact_check(posx,posy,dict_data,cur_layer = 0,inlayer = []):
    #bfs
    #check if inside bouding box
    x,x2 = dict_data["x"],dict_data["x"]+dict_data["width"]
    y,y2 = dict_data["y"],dict_data["y"]+dict_data["height"]
    layer = inlayer
    self_impact = False
    child_impact = False
    if x <= posx <= x2 and y <= posy <= y2:
        self_impact = True
        layer.append(cur_layer)
        for z_dept,child in enumerate(dict_data["child"]):
            if not child_impact:
                child_impact,layer = interact_check(posx,posy,child,z_dept,layer)
            else:
                return child_impact ,layer

    return self_impact or child_impact,layer


example = {
    'x': 20,
    'y': 40,
    'width': 100,
    'height': 100,
    'child': [
        {
            'x': 30,
            'y': 60,
            'width': 30,
            'height': 30,
            'child': []
        },
        {
            'x': 90,
            'y': 60,
            'width': 30,
            'height': 30,
                    'child': [        {
                    'x': 100,
                    'y': 70,
                    'width': 10,
                    'height': 10,
                    'child': []
                }
            ]
        }
    ]
}

pointx,pointy = 110,71

print(interact_check(pointx,pointy,example))