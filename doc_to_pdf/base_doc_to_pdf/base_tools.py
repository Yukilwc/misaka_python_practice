class BaseDocToPdf(object):
    def __init__(self,**kv):
        print(' BaseDocToPdf init')
        self.menu_url = kv['menu_url']

def hello():
    print('hello')