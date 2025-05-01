
#return true if impact
#recusion to search for deepest
#early return

def interact_check(posx,posy,dict_data,cur_layer = 0,layer = []):

    #bfs
    #check if inside bouding box
    x,x2 = dict_data["x"],dict_data["x"]+dict_data["width"]
    y,y2 = dict_data["y"],dict_data["y"]+dict_data["height"]
    layer = layer
    layer.append(cur_layer)
    self_impact = False
    child_impact = False
    if x <= posx <= x2 and y <= posy <= y2:
        self_impact = True

        for z_dept,child in enumerate(dict_data["child"]):
            if child_impact is not True:
                child_impact,layer = interact_check(posx,posy,child,z_dept,layer)
            else:
                return child_impact ,layer

    return self_impact or child_impact,layer


example = {
    'x': 20,
    'y': 40,
    'width': 25,
    'height': 12,
    'child': [
        {
            'x': 30,
            'y': 60,
            'width': 12,
            'height': 6,
            'child': []
        },
        {
            'x': 30,
            'y': 60,
            'width': 12,
            'height': 6,
            'child': []
        }
    ]
}

pointx,pointy = 30,50

print(interact_check(pointx,pointy,example))