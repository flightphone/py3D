from glslf import *
from math import sin, cos

TAU = math.pi * 2.
PI = math.pi


kxyy = vec3(1, -1, -1)
kyyx = vec3(-1, -1, 1)
kyxy = vec3(-1, 1, -1)
kxxx = vec3(1, 1, 1)

def calcNormal(pos, map):
    h = 0.0001
    return normalize(kxyy * map(pos + kxyy * h) + kyyx * map(pos + kyyx * h) +  kyxy * map(pos + kyxy * h) + kxxx * map(pos + kxxx * h))
    


nn = 128
eps = 0.001
dist_infin = 4.0

def dist(ro, rd, map):
    t = 0.
    pos = ro
    for _ in range(nn):
        pos = ro + rd*t
        h = map(pos)
        if (h < eps):
            break
        t += h;  
        if (t >= dist_infin):
            break
    return (t, pos)    

def sphere_projection(map, fname, nx = 100, ny = 100, r = 2., osd = 1):
    sys.stdout = open(fname, "w")
    nvert = 0
    for sd in range(osd):
        ro = vec3(0., 0., 0.)
        vert = [0]*(nx*ny + 1)
        for i in range(nx):
            for j in range(ny):
                x = math.pi * 2.0 * i/(nx - 1)
                y = math.pi*j/(ny - 1)
                rd = vec3(math.sin(y)*math.cos(x), math.sin(y)*math.sin(x), math.cos(y))
                if sd == 0:
                    ro = -rd*r

                d = dist(ro, rd, map)
                if d[0] < dist_infin and d[0] > eps:
                    nor = calcNormal(d[1], map)
                    print(d[1])
                    print(nor.vn())
                    nvert += 1
                    vert[i*ny + 1 + j] = nvert
                



        for i in range(nx-1):
            for j in range(ny-1):
                a = i*ny + 1 + j
                b = a + 1
                c = a+ny
                d = b + ny
                
                a = vert[a]
                b = vert[b]
                c = vert[c]
                d = vert[d]

                if (a *c * b > 0):
                    print(f'f {a}//{a} {c}//{c} {b}//{b}')
                if (b *c * d):
                    print(f'f {b}//{b} {c}//{c} {d}//{d}')
                
                # if (a *c * b > 0):
                #     print(f'f {a} {c} {b}')
                # if (b *c * d):
                #     print(f'f {b} {c} {d}')

            

    


def param_surf(map, fname, nx, ny, x0, x1 ,y0 , y1, txr = None, nvert = 0):
    if fname!="":
        sys.stdout = open(fname, "w")
    
    vert = [0]*(nx*ny + 1)
    for i in range(nx):
        for j in range(ny):
            x = x0 + (x1-x0)*i/(nx-1)
            y = y0 + (y1-y0)*j/(ny-1)
            d = map(x, y)
            if d:
                print(d[0])
                print(d[1].vn())
                if (txr):
                    print(txr(x, y))
                nvert += 1
                vert[i*ny + 1 + j] = nvert

    for i in range(nx-1):
        for j in range(ny-1):
            a = i*ny + 1 + j
            b = a + 1
            c = a+ny
            d = b + ny
            
            a = vert[a]
            b = vert[b]
            c = vert[c]
            d = vert[d]

            if (not txr):
                if (a *c * b > 0):
                    print(f'f {a}//{a} {c}//{c} {b}//{b}')
                if (b *c * d):
                    print(f'f {b}//{b} {c}//{c} {d}//{d}')
            else:
                if (a *c * b > 0):
                    print(f'f {a}/{a}/{a} {c}/{c}/{c} {b}/{b}/{b}')
                if (b *c * d):
                    print(f'f {b}/{b}/{b} {c}/{c}/{c} {d}/{d}/{d}')        
                #print(f'f {a} {c} {b}')
                #print(f'f {b} {c} {d}')
    return nvert


#calculte normal and points on curve
def curve_norm(t, f, r, curve, deriv = None):
    h = 0.0001
    if (deriv!=None):
        r1, r2 = deriv(t)
    else:
        vt = curve(t)
        vth = curve(t+h)
        r1 = normalize(vth - vt)
        r2 = normalize(curve(t+2*h) - vth*2. + vt)
    
    x = normalize(cross(r1, r2))
    y = normalize(cross(x, r1))
    nor = x*cos(f) + y*sin(f)
    val = curve(t) + nor*r
    return (val, nor, x, y, r1)


#calculte normal and points on curve
def curve_norm2(t, f, r, curve):
    h = 0.0001
    vt = curve(t)
    vth = curve(t+h)
    r1 = normalize(vth - vt)
    x = normalize(cross(r1, vec3(0, 0, 1)))
    if length(x) == 0:
        x = vec3(1, 0, 0)
        y = vec3(0, 1, 0)
    else:
        y = normalize(cross(x, r1))    
    
    nor = x*cos(f) + y*sin(f)
    val = curve(t) + nor*r
    return (val, nor, x, y, r1)

#calculate normal to surface
def normal_surf(u, v, surf):
    h = 0.0001
    du = surf(u+h, v) - surf(u-h, v)
    dv = surf(u, v+h) - surf(u, v-h)
    return normalize(cross(du, dv))

