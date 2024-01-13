from math import sin, cos
from  glslf  import *
from sdff import *

def circle(t, p):
    r = p[0]
    r0 = 0.2# p[1]
    d = vec3(r0*cos(t), r0*sin(t), 0)
    t = t % TAU
    if t>=0 and t < PI/2:
        d = d + vec3(r, r, 0)

    if t >= PI/2 and t < PI:
        d = d + vec3(-r, r, 0)    
    
    if t >= PI and t < PI*1.5:
        d = d + vec3(-r, -r, 0)        

    if t >= PI*1.5 and t < TAU:
        d = d + vec3(r, -r, 0)            
    return d    

def circle_map(u, v, p):
    r = 3
    r0 = 1.2
    d = curve_norm2(u, v, r0, circle, r, r0)
    d[0].z = d[0].z + p[0]
    return d

def circle_map_side(u, v, p):
    r = 3
    r0 = 1.2
    d = curve_norm2(u, 0, r0, circle, r, r0)
    d[0].z = v
    return d

def circle_map_top(u, v, p):
    h = p[0]
    nor = normalize(vec3(0, 0, h))
    if v == 0:
        d = circle(u, (3, 1.2))
        d.z = h
    else:
        d = vec3(0, 0, h)    
    return (d, nor)    

t = '''
def circle_h(u, v):
    h = 1.5
    d = curve_norm2(u, 0, 0, circle)
    z = h*clamp(v, 0, 1)
    if v >= 0 and v <= 1:
        x = d[0].x
        y = d[0].y
        nor = d[2] #normalize(vec3(x, y, 0))
    else:
        x, y = 0, 0
        if v > 1:
            nor = vec3(0, 0, 1)    
        else:    
            nor = vec3(0, 0, -1)
    return (vec3(x, y, z), nor)
'''
hh = 4
r0 = 1.2
nvert = param_surf(circle_map, "cube9.obj", 100, 25, 0., TAU, 0., PI/2, None, 0, hh)    
nvert = param_surf(circle_map, "", 100, 25, 0., TAU, PI*1.5, TAU, None, nvert, 0.)    
nvert = param_surf(circle_map_side, "", 100, 5, 0., TAU, 0, hh, None, nvert, hh)    
nvert = param_surf(circle_map_top, "", 100, 2, 0., TAU, 0, 1, None, nvert, hh+r0)
nvert = param_surf(circle_map_top, "", 100, 2, TAU, 0, 0, 1, None, nvert, -r0)    
#param_surf(circle_h, "cube3.obj", 100, 24, 0., TAU, -0.1, 1.1)    