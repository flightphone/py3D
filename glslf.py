
import math
import sys

class vec3:
    def __init__(self, x = 0.0, y = 0.0, z = 0.0) -> None:
        self.x = x 
        self.y = y
        self.z = z

    def __str__  (self): 
         return f'v {self.x} {self.y} {self.z}'   
    
    def vn (self): 
         return f'vn {self.x} {self.y} {self.z}'   

    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)
    
    def __add__(self, v):  
        if type(v) == vec3:      
            return vec3(self.x + v.x, self.y + v.y, self.z + v.z)    
        else:
            return vec3(self.x + v, self.y + v, self.z + v)    
            
        
    def __sub__(self, v):  
        if type(v) == vec3:      
            return vec3(self.x - v.x, self.y - v.y, self.z - v.z)        
        else:
            return vec3(self.x - v, self.y - v, self.z - v)    
            
    
    def __mul__(self, v):  
        if type(v) == vec3:      
            return vec3(self.x * v.x, self.y * v.y, self.z * v.z)            
        else:
            return vec3(self.x * v, self.y * v, self.z * v)    
        
    def __truediv__(self, v):  
        if type(v) == vec3:      
            return vec3(self.x / v.x, self.y / v.y, self.z / v.z)            
        else:
            return vec3(self.x / v, self.y / v, self.z / v)
    
    def xy(self):
        return vec2(self.x, self.y)            
            


class vec2:
    def __init__(self, x = 0.0, y = 0.0) -> None:
        self.x = x 
        self.y = y

    def __str__  (self): 
         return f'{self.x} {self.y}'   
    
    
    def __neg__(self):
        return vec2(-self.x, -self.y)
    
    def __add__(self, v):  
        if type(v) == vec2:      
            return vec2(self.x + v.x, self.y + v.y)    
        else:
            return vec2(self.x + v, self.y + v)    
            
        
    def __sub__(self, v):  
        if type(v) == vec2:      
            return vec2(self.x - v.x, self.y - v.y)        
        else:
            return vec2(self.x - v, self.y - v)    
            
    
    def __mul__(self, v):  
        if type(v) == vec2:      
            return vec2(self.x * v.x, self.y * v.y)            
        else:
            return vec2(self.x * v, self.y * v)    
        
    def __truediv__(self, v):  
        if type(v) == vec2:      
            return vec2(self.x / v.x, self.y / v.y)            
        else:
            return vec2(self.x / v, self.y / v)
    



def length(a):
    if type(a) == vec3:
        return math.sqrt(a.x*a.x + a.y*a.y + a.z*a.z)
    else:
        return math.sqrt(a.x*a.x + a.y*a.y)


def dot(a, b):
    if type(a) == vec3:
        return (a.x*b.x + a.y*b.y + a.z*b.z)
    else:
        return (a.x*b.x + a.y*b.y)


def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

def normalize(a):
    if (length(a) == 0):
        return a
    return a/length(a)


def cross(a, b):
    return vec3(a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x)

def smoothstep(edge0, edge1, x):
    x = clamp((x - edge0) / (edge1 - edge0), 0., 1.)
    return x * x * (3. - 2. * x)

def getAxis(a):
    a = normalize(a)
    z = a
    x  = vec3(1, 0, 0)
    if a.x != 0.0: 
        x = normalize(vec3(a.y, -a.x, 0))
    y = normalize(cross(x, a))   
    return (x, y, z)
