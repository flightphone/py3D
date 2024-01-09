import math
from  glslf  import *
from sdff import *

def sdEggBox(p, a, b):
    x = clamp(p.x, a, b)
    y = clamp(p.y, a, b)
    k = 15.
    f =  0.1*(math.sin(k*x) + math.sin(k*y))
    val = vec3(x, y, f)
    d = length(p - val)/4. - 0.01
    return d

def sdSphere(p, r):
    d = (length(p) - r)/4. - 0.01
    return d

def map(pos):
    return sdEggBox(pos, -1., 1.)
    #return sdSphere(pos, 1.0)

def map1(pos):
    return sdSphere(pos, 2.0)

def map2(p):
    z = clamp(p.z, -1., 1)
    v = vec3(0., 0., z)
    d = length(p - v)*0.5 - 0.2
    return d


def sdRoundBox(p,  b,  r ):
  q = vec3(abs(p.x), abs(p.y), abs(p.z)) - b
  return (length(vec3(max(q.x,0.0), max(q.y,0.0), max(q.z,0.0))) + min(max(q.x,max(q.y,q.z)),0.0))*0.5 - r

def map3 (p):
    return sdRoundBox(p, vec3(0.5, 0.3, 0.4), 0.1)

def aafi(p):
    fi = math.atan2(p[1], p[0])
    if p[1] < 0:
        fi += TAU
    return fi    

def lonlat (p):
    lon = aafi((p.x, p.y))/TAU
    lat = aafi((p.z, length(vec3(p.x, p.y, 0.))))/PI
    return (lon, lat)



def sign(n):
    if n < 0:
        return 1.
    else:
        return -1.
    
def sdfClei(p):
    n = 2.
    l = length(vec3(p.x, p.y, 0.))
    L = ((math.atan2(p.y, p.x)/PI) % 2.) * n 
    d = length(vec3( length(p)/2.-.5, l * math.sin( ( (L%1.-.5)*PI + math.atan2(p.z,l)/sign((L % 2.)-1.)) *.5/n ), 0.0))*0.5 -.03
    return d


def sdTor(p):
    l = length(vec3(p.x, p.y, 0.)) - 2.
    d = length(vec3(l, p.z, 0.))
    d = d - 1.4
    return d


def larme2(p, a):
    k = 0.3
    p.x += a*(k - 0.95)/2.0
    zoom = 1.5
    x = clamp(p.x, -a*0.95, a*k)
    f = math.acos(x/a)
    y = a*math.sin(f)*math.sin(f/2.)*math.sin(f/2.)*zoom
    d = length(p - vec2(x, y))
    f = math.acos(k)
    y = a*math.sin(f)*math.sin(f/2.)*math.sin(f/2.)*zoom
    y2 = clamp(p.y, -y, y)
    d2 = length(p - vec2(k*a, y2))
    d = min(d, d2)
    return d

def larme(p, a):
    l = length(vec2(p.x, p.y))
    d = larme2(vec2(p.z, l), a)
    return d*0.3 - 0.02

def map5(p):
    return larme(p, 2.)


#cart_projection(map, "eggbox1.obj", 100, 100, -1.5, 1.5, -1.5, 1.5, 2.0)
#sphere_projection(map1, "ball.obj", nx = 100, ny = 50, r = dist_infin)
#cart_projection(sdTor, "tor1.obj", 100, 100, -2.5, 2.5, -2.5, 2.5, 2.0)

#sphere_projection(sdfClei, "clelie.obj", nx = 400, ny = 200, r = dist_infin, osd = 2)    
#sphere_projection(sdTor, "tor.obj", nx = 100, ny = 100, r = dist_infin, osd = 2)    


sphere_projection(map5, "larme3.obj", nx = 100, ny = 100, r = dist_infin, osd = 2)    
