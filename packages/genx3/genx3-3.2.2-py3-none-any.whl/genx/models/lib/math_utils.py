'''
A library for various math utilites that is good to have to calculate
various scattering patterns that do not exist in the standard numpy or
scipy packages.
'''
import numpy as np

def dot2(A, B):
    D=np.zeros(A.shape, dtype=np.complex128)
    D[0, 0]=A[0, 0]*B[0, 0]+A[0, 1]*B[1, 0]
    D[0, 1]=A[0, 0]*B[0, 1]+A[0, 1]*B[1, 1]
    D[1, 0]=A[1, 0]*B[0, 0]+A[1, 1]*B[1, 0]
    D[1, 1]=A[1, 0]*B[0, 1]+A[1, 1]*B[1, 1]
    return D

def dot2_Adiag(A, B):
    D=np.zeros(A.shape, dtype=np.complex128)
    D[0, 0]=A[0, 0]*B[0, 0]
    D[0, 1]=A[0, 0]*B[0, 1]
    D[1, 0]=A[1, 1]*B[1, 0]
    D[1, 1]=A[1, 1]*B[1, 1]
    return D

def inv2(A):
    D=np.zeros(A.shape, dtype=np.complex128)
    det=det2(A)
    D[0, 0]=A[1, 1]
    D[0, 1]=-A[0, 1]
    D[1, 0]=-A[1, 0]
    D[1, 1]=A[0, 0]
    return D/det

def det2(A):
    return A[0, 0]*A[1, 1]-A[0, 1]*A[1, 0]

def dot4(A, B):
    D=np.zeros(A.shape, dtype=np.complex128)
    D[0, 0]=(A[0, 0]*B[0, 0]+A[0, 1]*B[1, 0]+A[0, 2]*B[2, 0]+
             A[0, 3]*B[3, 0])
    D[0, 1]=(A[0, 0]*B[0, 1]+A[0, 1]*B[1, 1]+A[0, 2]*B[2, 1]+
             A[0, 3]*B[3, 1])
    D[0, 2]=(A[0, 0]*B[0, 2]+A[0, 1]*B[1, 2]+A[0, 2]*B[2, 2]+
             A[0, 3]*B[3, 2])
    D[0, 3]=(A[0, 0]*B[0, 3]+A[0, 1]*B[1, 3]+A[0, 2]*B[2, 3]+
             A[0, 3]*B[3, 3])

    D[1, 0]=(A[1, 0]*B[0, 0]+A[1, 1]*B[1, 0]+A[1, 2]*B[2, 0]+
             A[1, 3]*B[3, 0])
    D[1, 1]=(A[1, 0]*B[0, 1]+A[1, 1]*B[1, 1]+A[1, 2]*B[2, 1]+
             A[1, 3]*B[3, 1])
    D[1, 2]=(A[1, 0]*B[0, 2]+A[1, 1]*B[1, 2]+A[1, 2]*B[2, 2]+
             A[1, 3]*B[3, 2])
    D[1, 3]=(A[1, 0]*B[0, 3]+A[1, 1]*B[1, 3]+A[1, 2]*B[2, 3]+
             A[1, 3]*B[3, 3])

    D[2, 0]=(A[2, 0]*B[0, 0]+A[2, 1]*B[1, 0]+A[2, 2]*B[2, 0]+
             A[2, 3]*B[3, 0])
    D[2, 1]=(A[2, 0]*B[0, 1]+A[2, 1]*B[1, 1]+A[2, 2]*B[2, 1]+
             A[2, 3]*B[3, 1])
    D[2, 2]=(A[2, 0]*B[0, 2]+A[2, 1]*B[1, 2]+A[2, 2]*B[2, 2]+
             A[2, 3]*B[3, 2])
    D[2, 3]=(A[2, 0]*B[0, 3]+A[2, 1]*B[1, 3]+A[2, 2]*B[2, 3]+
             A[2, 3]*B[3, 3])

    D[3, 0]=(A[3, 0]*B[0, 0]+A[3, 1]*B[1, 0]+A[3, 2]*B[2, 0]+
             A[3, 3]*B[3, 0])
    D[3, 1]=(A[3, 0]*B[0, 1]+A[3, 1]*B[1, 1]+A[3, 2]*B[2, 1]+
             A[3, 3]*B[3, 1])
    D[3, 2]=(A[3, 0]*B[0, 2]+A[3, 1]*B[1, 2]+A[3, 2]*B[2, 2]+
             A[3, 3]*B[3, 2])
    D[3, 3]=(A[3, 0]*B[0, 3]+A[3, 1]*B[1, 3]+A[3, 2]*B[2, 3]+
             A[3, 3]*B[3, 3])

    return D

def dot4_Adiag(A, B):
    D=np.zeros(A.shape, dtype=np.complex128)
    # D[0,0] = A[0, 0]*B[0, 0]
    # D[0,1] = A[0, 0]*B[0, 1]
    # D[0,2] = A[0, 0]*B[0, 2]
    # D[0,3] = A[0, 0]*B[0, 3]
    D[0]=A[0, 0]*B[0]

    # D[1,0] = A[1, 1]*B[1, 0]
    # D[1,1] = A[1, 1]*B[1, 1]
    # D[1,2] = A[1, 1]*B[1, 2]
    # D[1,3] = A[1, 1]*B[1, 3]
    D[1]=A[1, 1]*B[1]

    # D[2,0] = A[2, 2]*B[2, 0]
    # D[2,1] = A[2, 2]*B[2, 1]
    # D[2,2] = A[2, 2]*B[2, 2]
    # D[2,3] = A[2, 2]*B[2, 3]
    D[2]=A[2, 2]*B[2]

    # D[3,0] = A[3, 3]*B[3, 0]
    # D[3,1] = A[3, 3]*B[3, 1]
    # D[3,2] = A[3, 3]*B[3, 2]
    # D[3,3] = A[3, 3]*B[3, 3]
    D[3]=A[3, 3]*B[3]
    return D

def dot4_Bdiag(A, B):
    '''Assumes that A is a diagonal matrix - will speed up the 
    multiplicaiton
    '''
    D=np.zeros(A.shape, dtype=np.complex128)
    D[0, 0]=A[0, 0]*B[0, 0]
    D[0, 1]=A[0, 1]*B[1, 1]
    D[0, 2]=A[0, 2]*B[2, 2]
    D[0, 3]=A[0, 3]*B[3, 3]

    D[1, 0]=A[1, 0]*B[0, 0]
    D[1, 1]=A[1, 1]*B[1, 1]
    D[1, 2]=A[1, 2]*B[2, 2]
    D[1, 3]=A[1, 3]*B[3, 3]

    D[2, 0]=A[2, 0]*B[0, 0]
    D[2, 1]=A[2, 1]*B[1, 1]
    D[2, 2]=A[2, 2]*B[2, 2]
    D[2, 3]=A[2, 3]*B[3, 3]

    D[3, 0]=A[3, 0]*B[0, 0]
    D[3, 1]=A[3, 1]*B[1, 1]
    D[3, 2]=A[3, 2]*B[2, 2]
    D[3, 3]=A[3, 3]*B[3, 3]

    return D

def inv4(A):
    '''returns the inverse of the 4x4 matrix A
    '''
    D=np.zeros(A.shape, dtype=np.complex128)
    D[0, 0]=(A[1, 2]*A[2, 3]*A[3, 1]-A[1, 3]*A[2, 2]*A[3, 1]
             +A[1, 3]*A[2, 1]*A[3, 2]-A[1, 1]*A[2, 3]*A[3, 2]
             -A[1, 2]*A[2, 1]*A[3, 3]+A[1, 1]*A[2, 2]*A[3, 3])
    D[0, 1]=(A[0, 3]*A[2, 2]*A[3, 1]-A[0, 2]*A[2, 3]*A[3, 1]
             -A[0, 3]*A[2, 1]*A[3, 2]+A[0, 1]*A[2, 3]*A[3, 2]
             +A[0, 2]*A[2, 1]*A[3, 3]-A[0, 1]*A[2, 2]*A[3, 3])
    D[0, 2]=(A[0, 2]*A[1, 3]*A[3, 1]-A[0, 3]*A[1, 2]*A[3, 1]
             +A[0, 3]*A[1, 1]*A[3, 2]-A[0, 1]*A[1, 3]*A[3, 2]
             -A[0, 2]*A[1, 1]*A[3, 3]+A[0, 1]*A[1, 2]*A[3, 3])
    D[0, 3]=(A[0, 3]*A[1, 2]*A[2, 1]-A[0, 2]*A[1, 3]*A[2, 1]
             -A[0, 3]*A[1, 1]*A[2, 2]+A[0, 1]*A[1, 3]*A[2, 2]
             +A[0, 2]*A[1, 1]*A[2, 3]-A[0, 1]*A[1, 2]*A[2, 3])
    D[1, 0]=(A[1, 3]*A[2, 2]*A[3, 0]-A[1, 2]*A[2, 3]*A[3, 0]
             -A[1, 3]*A[2, 0]*A[3, 2]+A[1, 0]*A[2, 3]*A[3, 2]
             +A[1, 2]*A[2, 0]*A[3, 3]-A[1, 0]*A[2, 2]*A[3, 3])
    D[1, 1]=(A[0, 2]*A[2, 3]*A[3, 0]-A[0, 3]*A[2, 2]*A[3, 0]
             +A[0, 3]*A[2, 0]*A[3, 2]-A[0, 0]*A[2, 3]*A[3, 2]
             -A[0, 2]*A[2, 0]*A[3, 3]+A[0, 0]*A[2, 2]*A[3, 3])
    D[1, 2]=(A[0, 3]*A[1, 2]*A[3, 0]-A[0, 2]*A[1, 3]*A[3, 0]
             -A[0, 3]*A[1, 0]*A[3, 2]+A[0, 0]*A[1, 3]*A[3, 2]
             +A[0, 2]*A[1, 0]*A[3, 3]-A[0, 0]*A[1, 2]*A[3, 3])
    D[1, 3]=(A[0, 2]*A[1, 3]*A[2, 0]-A[0, 3]*A[1, 2]*A[2, 0]
             +A[0, 3]*A[1, 0]*A[2, 2]-A[0, 0]*A[1, 3]*A[2, 2]
             -A[0, 2]*A[1, 0]*A[2, 3]+A[0, 0]*A[1, 2]*A[2, 3])
    D[2, 0]=(A[1, 1]*A[2, 3]*A[3, 0]-A[1, 3]*A[2, 1]*A[3, 0]
             +A[1, 3]*A[2, 0]*A[3, 1]-A[1, 0]*A[2, 3]*A[3, 1]
             -A[1, 1]*A[2, 0]*A[3, 3]+A[1, 0]*A[2, 1]*A[3, 3])
    D[2, 1]=(A[0, 3]*A[2, 1]*A[3, 0]-A[0, 1]*A[2, 3]*A[3, 0]
             -A[0, 3]*A[2, 0]*A[3, 1]+A[0, 0]*A[2, 3]*A[3, 1]
             +A[0, 1]*A[2, 0]*A[3, 3]-A[0, 0]*A[2, 1]*A[3, 3])
    D[2, 2]=(A[0, 1]*A[1, 3]*A[3, 0]-A[0, 3]*A[1, 1]*A[3, 0]
             +A[0, 3]*A[1, 0]*A[3, 1]-A[0, 0]*A[1, 3]*A[3, 1]
             -A[0, 1]*A[1, 0]*A[3, 3]+A[0, 0]*A[1, 1]*A[3, 3])
    D[2, 3]=(A[0, 3]*A[1, 1]*A[2, 0]-A[0, 1]*A[1, 3]*A[2, 0]
             -A[0, 3]*A[1, 0]*A[2, 1]+A[0, 0]*A[1, 3]*A[2, 1]
             +A[0, 1]*A[1, 0]*A[2, 3]-A[0, 0]*A[1, 1]*A[2, 3])
    D[3, 0]=(A[1, 2]*A[2, 1]*A[3, 0]-A[1, 1]*A[2, 2]*A[3, 0]
             -A[1, 2]*A[2, 0]*A[3, 1]+A[1, 0]*A[2, 2]*A[3, 1]
             +A[1, 1]*A[2, 0]*A[3, 2]-A[1, 0]*A[2, 1]*A[3, 2])
    D[3, 1]=(A[0, 1]*A[2, 2]*A[3, 0]-A[0, 2]*A[2, 1]*A[3, 0]
             +A[0, 2]*A[2, 0]*A[3, 1]-A[0, 0]*A[2, 2]*A[3, 1]
             -A[0, 1]*A[2, 0]*A[3, 2]+A[0, 0]*A[2, 1]*A[3, 2])
    D[3, 2]=(A[0, 2]*A[1, 1]*A[3, 0]-A[0, 1]*A[1, 2]*A[3, 0]
             -A[0, 2]*A[1, 0]*A[3, 1]+A[0, 0]*A[1, 2]*A[3, 1]
             +A[0, 1]*A[1, 0]*A[3, 2]-A[0, 0]*A[1, 1]*A[3, 2])
    D[3, 3]=(A[0, 1]*A[1, 2]*A[2, 0]-A[0, 2]*A[1, 1]*A[2, 0]
             +A[0, 2]*A[1, 0]*A[2, 1]-A[0, 0]*A[1, 2]*A[2, 1]
             -A[0, 1]*A[1, 0]*A[2, 2]+A[0, 0]*A[1, 1]*A[2, 2])

    return D/det4(A)

def det4(A):
    ''' Calculates the determinant of A a 4x4 matrix'''
    val=(A[0, 3]*A[1, 2]*A[2, 1]*A[3, 0]-A[0, 2]*A[1, 3]*A[2, 1]*A[3, 0]
         -A[0, 3]*A[1, 1]*A[2, 2]*A[3, 0]+A[0, 1]*A[1, 3]*A[2, 2]*A[3, 0]
         +A[0, 2]*A[1, 1]*A[2, 3]*A[3, 0]-A[0, 1]*A[1, 2]*A[2, 3]*A[3, 0]
         -A[0, 3]*A[1, 2]*A[2, 0]*A[3, 1]+A[0, 2]*A[1, 3]*A[2, 0]*A[3, 1]
         +A[0, 3]*A[1, 0]*A[2, 2]*A[3, 1]-A[0, 0]*A[1, 3]*A[2, 2]*A[3, 1]
         -A[0, 2]*A[1, 0]*A[2, 3]*A[3, 1]+A[0, 0]*A[1, 2]*A[2, 3]*A[3, 1]
         +A[0, 3]*A[1, 1]*A[2, 0]*A[3, 2]-A[0, 1]*A[1, 3]*A[2, 0]*A[3, 2]
         -A[0, 3]*A[1, 0]*A[2, 1]*A[3, 2]+A[0, 0]*A[1, 3]*A[2, 1]*A[3, 2]
         +A[0, 1]*A[1, 0]*A[2, 3]*A[3, 2]-A[0, 0]*A[1, 1]*A[2, 3]*A[3, 2]
         -A[0, 2]*A[1, 1]*A[2, 0]*A[3, 3]+A[0, 1]*A[1, 2]*A[2, 0]*A[3, 3]
         +A[0, 2]*A[1, 0]*A[2, 1]*A[3, 3]-A[0, 0]*A[1, 2]*A[2, 1]*A[3, 3]
         -A[0, 1]*A[1, 0]*A[2, 2]*A[3, 3]+A[0, 0]*A[1, 1]*A[2, 2]*A[3, 3])
    return val

def roots4thdegree(a, b, c, d, e):
    ''' Function that solves a fourth degree polynomial according to
    Ferraris solution alogirthm from: http://en.wikipedia.org/wiki/Quartic_function
    a*x**4 + b*x**3 + c*x**2 + d*x + e = 0
    '''
    alpha=-3*b**2/8/a**2+c/a
    beta=b**3/8/a**3-b*c/2/a**2+d/a
    gamma=-3*b**4/256/a**4+c*b**2/16/a**3-b*d/4/a**2+e/a
    p=-alpha**2/12.-gamma
    q=-alpha**3/108.+alpha*gamma/3.-beta**2/8.
    r=-q/2.+np.sqrt(q**2/4.+p**3/27.)
    u=r**(1.0/3.0)
    y=np.where(u!=0, -5./6.*alpha+u-p/3.0/u, -5./6.+u-q**(1./3.))
    w=np.sqrt(alpha+2*y)
    cond=beta!=0
    x1=-b/4./a+np.where(cond, (w-np.sqrt(-(3*alpha+2*y+2*beta/w)))/2.,
                        np.sqrt(0.5*(-alpha+np.sqrt(alpha**2-4*gamma))))
    x2=-b/4./a+np.where(cond, (w+np.sqrt(-(3*alpha+2*y+2*beta/w)))/2.,
                        np.sqrt(0.5*(-alpha-np.sqrt(alpha**2-4*gamma))))
    x3=-b/4./a+np.where(cond, (-w-np.sqrt(-(3*alpha+2*y-2*beta/w)))/2.,
                        - np.sqrt(0.5*(-alpha+np.sqrt(alpha**2-4*gamma))))
    x4=-b/4./a+np.where(cond, (-w+np.sqrt(-(3*alpha+2*y-2*beta/w)))/2.,
                        - np.sqrt(0.5*(-alpha-np.sqrt(alpha**2-4*gamma))))
    return x1, x2, x3, x4
