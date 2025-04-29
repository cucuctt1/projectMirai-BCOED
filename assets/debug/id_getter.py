
def id_debug(func):

    def wraper(*args,**kwargs):
        func(*args,**kwargs)

    return wraper()