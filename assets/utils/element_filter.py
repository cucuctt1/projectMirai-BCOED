

def filter(block_data,element_type):
    temp = []
    for data in block_data:

        if type(data) == element_type:
            temp.append(data)

    return temp