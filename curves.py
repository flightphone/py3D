from math import sin, cos, exp
from  glslf  import *
from sdff import *

h = 5
axis_x = vec3(1, 0, 0)
axis_y = vec3(0, 1, 0)
axis_z = vec3(0, 0, 1)
shift = vec3(0, 0, 0)

def heir(t):
    fi = 0.8#dot(axis_x, vec3(1.12, 3, 6))
    z = t
    x = sin(z * TAU  + fi) * h * 0.3 * z * (h - z) / h / h 
    y = sin(z * TAU  - fi) * h * 0.3 * z * (h - z) / h / h
    return axis_x*x + axis_y*y + axis_z*z + shift

def heir_map(t, f):
    
    r1 = 0.1
    r0 = 0.04
    if t <= h and t >= 0:
        res =  curve_norm(t, f, 0., heir)   
        r = r1 * (h - t) / h + r0 
        return (res[0] + res[1]*r, res[1])
    else:
        t0 = clamp(t, 0, h)
        fi = clamp((t-t0)*PI/2., -PI/2., PI/2.)
        res =  curve_norm(t0, f, 0, heir)   
        r = r1 * (h - t0) / h + r0
        x = res[2]
        y = res[3]
        z = res[4]
        nor = x*cos(f)*cos(fi) + y*sin(f)*cos(fi) + z*sin(fi)
        val = res[0] + nor*r
        return (val, nor)

def texture1(u, v):    
    u = clamp(u, 0, h) / h
    s = f'vt {u} 0.5'
    return s

def texture0(u, v):
    u, v = u/TAU, v/PI
    return f'vt {u} {v}'     

def texture4(u, v):
    u, v = u/TAU/4, v/TAU
    return f'vt {u} {v}'

def sphere(u, v):
    r = 2
    nor = -vec3(sin(v)*cos(u), sin(v)*sin(u), cos(v))
    val = nor*r
    return(val, nor)

#param_surf(heir_map, "heir.obj", 100, 40, -1., h+1, 0., TAU, texture1)
def render_sprut():
    nvert = param_surf(sphere, "sprut.obj", 100, 100, 0., TAU, 0., PI, texture0)
    n = 5
    global axis_x, axis_y, axis_z, shift
    for i in range(n):
        fi = TAU*i/n
        a = vec3(sin(5*PI/6)*cos(fi), sin(5*PI/6)*sin(fi), cos(5*PI/6))
        axis_x, axis_y, axis_z = getAxis(a)
        shift = a*2
        nvert = param_surf(heir_map, "", 100, 50, -1., h+1, 0., TAU, texture1, nvert)

#render_sprut()
#https://mathcurve.com/courbes3d.gb/solenoidtoric/solenoidtoric.shtml
def solenoid(t):
    n = 1.25
    R = 3
    r = 1
    return vec3((R + r*cos(n*t))*cos(t), (R + r*cos(n*t))*sin(t), r*sin(n*t))

def solenoid_map(t, f):
    return(curve_norm(t, f, 1, solenoid))



def larme(u, v):
    a = 2
    zoom = 1.5
    l = a*sin(v)*sin(v/2)*sin(v/2)*zoom
    z = a*cos(v)
    x = l*cos(u)
    y = l*sin(u)
    return vec3(x, y, z)

def larme_map(u, v):
    h = PI/3
    if v > h:
        val = larme(u, v)
        nor = normal_surf(u, v, larme)
    else:
        a = 2
        zoom = 1.5
        l = a*sin(h)*sin(h/2)*sin(h/2)*zoom
        z = a*cos(h)
        l = l*v/h
        x = l*cos(u)
        y = l*sin(u)
        val = vec3(x, y, z)
        nor = vec3(0, 0, -1)

    return (val, nor)

def larme_map2(u, v):
    val, nor = larme_map(u, v)
    val = val + nor*0.2
    return (val, nor)

#param_surf(solenoid_map, "solenoid.obj", 500, 100, 0., 4*TAU, 0., TAU, texture4)
#param_surf(heir_map, "heir.obj", 400, 40, -1., h+1, 0., TAU, texture1)
nvert = param_surf(larme_map, "larme9.obj", 100, 100, 0, TAU, 0, 0.9*PI, texture0)
#param_surf(larme_map2, "", 100, 100, 0, TAU, 0, 0.9*PI, texture0, nvert)