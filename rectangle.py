class rect:
    def __init__ (self, pict):
        '''
        pict should be a zelle graphics.image file
        '''
        self.pict = pict
        pass

    def right(self):
        return self.pict.getAnchor().getX() + self.pict.getWidth()/2
    def left(self):
        return self.pict.getAnchor().getX() - self.pict.getWidth()/2
    def top(self):
        return self.pict.getAnchor().getY() - self.pict.getHeight()/2
    def bottom(self):
        return self.pict.getAnchor().getY() + self.pict.getHeight()/2
