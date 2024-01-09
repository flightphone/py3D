import math
from  glslf  import *
from sdff import *

def sdCosNp(p:vec2, a):
    fi = math.atan2(p.y, p.x)
    L = length(p)
    d = dist_infin
    r = a * math.cos(2. * fi)
    if(p.x < 0.):
        r = -.5
    d = min(abs(L - r), d)
    f = math.acos(clamp(L / a, -1., 1.)) / 2.
    d = min(2.0 * abs(math.sin((fi - f) / 2.0)) * L, d)
    d = min(2.0 * abs(math.sin((fi + f) / 2.0)) * L, d)
    return d


def scale5(x, y):
    r = (1.-math.asin(clamp(abs((x - 0.5)*2.), 0., 1.))*2./PI)*0.6 + 0.4 -y
    #float r = (1.-asin(abs((x - 0.5)*2.))*2./PI)*0.6 + 0.4 -y;
    f = smoothstep(-0.05, 0.05, r)
    f *= y*y*0.5
    f *= (1. + 6.0*math.cos((x-0.5)*PI)*math.cos((y-0.5)*PI))
    dl = f*0.01
    return dl   



def toorow(x, y, step):
    x1 = x
    y1 = y*0.5 + 0.5
    x2 = x + step % 1.0
    y2 = y*0.5
    dl1 = scale5(x1, y1)
    dl2 = scale5(x2, y2)
    return max(dl1, dl2)


def sdConePine(p:vec3, a):
    l = length(p.xy())
    h = -p.z + a/2.
    d = sdCosNp(vec2(h, l), a)
    n = 10.
    m = 8.
    step = 0.5
    y = 1.0 - h/a
    x = (math.atan2(p.y, p.x) % TAU)/TAU
    row = math.floor(y*n)
    y = y*n - row
    shift = step*row % 1.0
    x = x - shift/m % 1.0
    x = x*m % 1.0
    dl = toorow(x, y, step)
    d*=0.3
    d -= dl
    return d



def map(pos):
    return sdConePine(pos, 2.0)


sphere_projection(map, "pine.obj", nx = 300, ny = 150, r = 2., osd = 1)  
