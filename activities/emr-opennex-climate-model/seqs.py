# -*- coding: utf-8 -*-
import math

# This library calculates sequence numbers for quadrangles of a given size in degrees.

# Example: 5° quadrangle sequence number
# s = sequenceNumber(5,49.5,-126.0)
#
def sequenceNumber(size,lat,lon):
   latMax = int(180 / size)
   lonMax = int(360 / size)
   nlat = 90 - lat
   nlon = 360 + lon if lon < 0 else lon
   s = int(math.floor(nlat/size)) * int(lonMax) + int(nlon / size) + 1
   return s
   
# Example: 5° quandrangle sequence numbers for a large rectangular region
# quad = sequencesFromQuadrangle(5,[40,-125,35,-120])
# 
def sequencesFromQuadrangle(size,quad):
   quadBounds = [ sequenceNumber(size,quad[0],quad[1]), sequenceNumber(size,quad[0],quad[3]),
                  sequenceNumber(size,quad[2],quad[3])]
   width = int(quadBounds[1] - quadBounds[0] + 1)
   lonMax = int(360 / size)
   
   s = quadBounds[0]
   while s<quadBounds[2]:
      for seq in range(s,s+width):
          yield seq
      s += lonMax
             
             

