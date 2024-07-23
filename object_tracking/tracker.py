import math 

class EuclideanDistTracker:
    id = 0
    def __init__( self, max_speed = 50 ):
        self.snap = []
        self.max_speed_squared = max_speed * max_speed

    def update( self, detections ):
        snap = []
        for x, y, _w, _h in detections :
            closest = None
            for px, py, id, speed in self.snap :
                dist = self.dist_squared( x, y, px, py )
                if dist > self.max_speed_squared : continue
                if not closest : closest = ( x, y, id, dist )

                cx, cy, cid, cdist = closest
                if dist < cdist :
                    closest = ( x, y, id, dist )     

            if not closest :
                EuclideanDistTracker.id += 1
                closest = ( x, y, EuclideanDistTracker.id, 0 )

            snap.append( closest )
        self.snap = snap
        return self.snap
    
    def dist_squared( self, x1, y1, x2, y2 ):
        dx = x1 - x2
        dy = y1 - y2
        return dx*dx + dy*dy 
