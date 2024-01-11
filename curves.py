from math import sin, cos, exp
from  glslf  import *
from sdff import *

h = 3
axis_x = vec3(1, 0, 0)
axis_y = vec3(0, 1, 0)
axis_z = vec3(0, 0, 1)
shift = vec3(0, 0, 0)

def heir(t):
    fi = 0.8
    z = t
    x = sin(z * TAU  + fi) * h * 0.6 * z * (h - z) / h / h 
    y = sin(z * TAU  - fi) * h * 0.6 * z * (h - z) / h / h
    return axis_x*x + axis_y*y + axis_z*z + shift

def heir_map(t, f):
    
    r1 = 0.08
    r0 = 0.02
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

def sphere(u, v):
    r = 2
    nor = -vec3(sin(v)*cos(u), sin(v)*sin(u), cos(v))
    val = nor*r
    return(val, nor)

#param_surf(heir_map, "heir.obj", 100, 40, -1., h+1, 0., TAU, texture1)
nvert = param_surf(sphere, "virus.obj", 100, 100, 0., TAU, 0., PI, texture0)
n = 5
for i in range(n):
    fi = TAU*i/n
    a = vec3(sin(5*PI/6)*cos(fi), sin(5*PI/6)*sin(fi), cos(5*PI/6))
    axis_x, axis_y, axis_z = getAxis(a)
    shift = a*2
    nvert = param_surf(heir_map, "", 200, 100, -1., h+1, 0., TAU, texture1, nvert)
'''
float heirw(vec3 p, float h, float r, float r0, float fi) {
    h = h * (1.0 + 0.05 * cos(iTime * 4. + fi));
    float z = clamp(p.z, 0., h), // radius pimple 
    x = sin(z * PI * 2.0 + iTime * 4. + fi) * h * 0.3 * z * (h - z) / h / h, y = sin(z * PI * 2.0 - iTime * 4. + fi) * h * 0.3 * z * (h - z) / h / h;

    vec3 p2 = vec3(x, y, z);
    //Color
    sdfColor = mix(col1, col2, pow(vec3(p.z / h), vec3(3.)));
    return length(p - p2) * 0.5 - r * (h - z) / h - r0;
}
'''