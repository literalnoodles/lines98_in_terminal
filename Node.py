class Node:
    def __init__(self,ntype,color):
        self.color = color
        self.ntype = ntype
    
    @classmethod
    def parse(cls,str):
        ntype,color = str.split('/')
        return cls(ntype,color)

