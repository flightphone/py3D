from math import sin, cos
from  glslf  import *
from sdff import *

r0 = 2.
r1 = 0.8

def map(x, y):
    r = r0 + r1*cos(y)
    val = vec3(r*cos(x), r*sin(x), r1*sin(y))
    nor = vec3(cos(y)*cos(x), cos(y)*sin(x), sin(y))
    return (val, nor)


def cosn2(x, y):
    #r=cos(2.*f)
    a = 2.0
    r = a*cos(2.*y)
    z0 = r*cos(y)
    h = r*sin(y)
    x0 = h*cos(x)
    y0 = h*sin(x)
    return vec3(x0, y0, z0)

def cosn(u, v):
    val = cosn2(u, v)
    nor = normal_surf(u, v, cosn2)
    return (val, nor)




    


def trefoil_knot(t):
    return vec3(sin(t) + 2*sin(2*t), cos(t) - 2*cos(2*t), -0.5*sin(3*t))

def trefoil(t, f):
    return curve_norm(t, f, 0.3, trefoil_knot)

def eight_knot(t):
    return vec3((2 + cos(2*t))*cos(3*t), (2 + cos(2*t))*sin(3*t), 0.5*sin(4*t))

def eight(t, f):
    return curve_norm(t, f, 0.3, eight_knot)

def sinwave(t):
    a = 3.
    b = 1.5
    m = 3.5
    n = 9
    return vec3(a*cos(t), a*sin(t), b*sin(n/m*t))

def sinwave_map(t, f):
    return curve_norm(t, f, 0.1, sinwave)

def rose(t):
    a = 3.
    n = 2.2
    b = 3.
    r = a*cos(n*t)
    return vec3(r*cos(t), r*sin(t), b*cos(n*t)*cos(n*t))

def rose_map(t, f):
    return curve_norm(t, f, 0.1, rose)

def clelia(t):
    r = 3
    n = 2
    a = r*cos(n*t)
    return vec3(a*cos(t), a*sin(t), r*sin(n*t))

def clelia_map(t, f):
    return curve_norm(t, f, 0.2, clelia)


#https://mathcurve.com/courbes3d.gb/lissajous3d/lissajous3d.shtml

def liss(t):
    a = 3
    b = 3
    c = 1.5
    n = 1.5
    m = 2.5
    f = PI/2.
    e = .0
    return vec3(a*sin(t), b*sin(n*t + f), c*sin(m*t + e))

def liss_deriv(t):
    a = 3
    b = 3
    c = 1.5
    n = 1.5
    m = 2.5
    f = PI/2.
    e = .0
    r1 = normalize(vec3(a*cos(t), n*b*cos(n*t + f), m*c*cos(m*t + e)))
    r2 = normalize(vec3(-a*sin(t), -n*n*b*sin(n*t + f), -m*m*c*sin(m*t + e)))
    return r1, r2

def liss_map(t, f):
    #return curve_norm(t, f, 0.25, liss, liss_deriv)
    return curve_norm(t, f, 0.2, liss)

#param_surf(map, "torp1.obj", 100, 100, 0., TAU , 0., TAU)
#param_surf(cosn, "cosn2.obj", 100, 100, 0., TAU , 0., PI/4)
#param_surf(trefoil, "trfoil.obj", 100, 100, 0., TAU , 0., TAU)
#param_surf(eight, "eight_knot.obj", 200, 100, 0., TAU , 0., TAU)
#param_surf(sinwave_map, "sinwave.obj", 700, 50, 0., 7.*TAU , 0., TAU)
#param_surf(rose_map, "rose3.obj", 500, 50, 0., 5.*TAU , 0., TAU)
#param_surf(clelia_map, "clelia1.obj", 100, 100, 0., TAU , 0., TAU)
#param_surf(liss_map, "liss.obj", 700, 100, 0., 7.*TAU , 0., TAU)


def scale5(x, y):
    r = (1.-math.asin(clamp(abs((x - 0.5)*2.), 0., 1.))*2./PI)*0.6 + 0.4 -y
    #float r = (1.-asin(abs((x - 0.5)*2.))*2./PI)*0.6 + 0.4 -y;
    f = smoothstep(-0.05, 0.05, r)
    f *= y*y*0.5
    f *= (1. + 6.0*math.cos((x-0.5)*PI)*math.cos((y-0.5)*PI))
    dl = f*0.1
    return dl   



def toorow(x, y, step):
    x1 = x
    y1 = y*0.5 + 0.5
    x2 = x + step % 1.0
    y2 = y*0.5
    dl1 = scale5(x1, y1)
    dl2 = scale5(x2, y2)
    return max(dl1, dl2)

def pine(u, v):
    a = 2.0
    p, nor = cosn(u, v)
    l = length(p.xy())
    h = p.z 
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
    p = p - nor*dl
    return p

def pine_map(u, v):
    val = pine(u, v)
    nor = normal_surf(u, v, pine)
    return (val, nor)


param_surf(pine_map, "pine2.obj", 100, 300, 0., TAU , 0., PI/4)