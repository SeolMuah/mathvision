import numpy as np
import sympy as s
from sympy import Symbol, solve


def get_rotation_theta(r1, r2) :
    """
    :param r1: 3X1 벡터
    :param r2: 3X1 벡터
    :return: 회전한 각도 라디안
    """
    
    return np.arccos(np.dot(r1, r2) / (np.linalg.norm(r1) * np.linalg.norm(r2)))
 

def get_rotation_matrix(vec1 : np.array, vec2 : np.array) :
    """
    :param vec1: 3X1 벡터
    :param vec2: 3X1 벡터
    :return: 3X3 회전 행렬
    """
    h = np.cross(vec1, vec2)
    h = h/np.linalg.norm(h)
    theta = get_rotation_theta(vec1, vec2)
    cos = np.cos(theta)
    sin = np.sin(theta)
    ux,uy,uz = h
    R = np.array([(cos+(ux**2)*(1-cos), ux*uy*(1-cos)-uz*sin, ux*uz*(1-cos)+uy*sin),
                    (uy*ux*(1-cos) + uz*sin, cos+(uy**2)*(1-cos), uy*uz*(1-cos)-ux*sin),
                    (uz*ux*(1-cos)-uy*sin, uz*uy*(1-cos)+ux*sin, cos+(uz**2)*(1-cos))])
    return R

def get_rotation_pos(rotation_pos, ref_pos, com_pos, R1, R2=None) :
    
    ref_vec = rotation_pos - ref_pos
    rotation_vec = R2 @ R1 @ ref_vec if R2 is not None else R1 @ ref_vec

    return rotation_vec + com_pos



################################################################

ref_points = np.array([(-0.500000,	0.000000,	2.121320),
                (0.500000,	0.000000,	2.121320),
                (0.500000,	-0.707107,	2.828427)
])
                
com_points = np.array([
    (1.363005,	-0.427130,	2.339082),
    (1.748084,	0.437983,	2.017688),
    (2.636461,	0.184843,	2.400710)
])

ref_vecs = [ref_points[i]-ref_points[0] for i in range(len(ref_points))[1:]]
com_vecs = [com_points[i]-com_points[0] for i in range(len(com_points))[1:]]
print(f"ref_vecs : {ref_vecs}")
print(f"com_vecs : {com_vecs}")

#각 평면의 법선 벡터
h1 = np.cross(ref_vecs[0], ref_vecs[1])
h2 = np.cross(com_vecs[0], com_vecs[1])
print(f"ref_norm_vec : {h1}")
print(f"com_norm_vec : {h2}")


#(1-1) h1 -> h2로 회전하기 위한 Theta 구하기 
theta = get_rotation_theta(h1, h2)
print(f"회전각도  Theta1 (Radian, degree) : ({theta:.4f}, {theta/np.pi*180:.4f})")

#(1-2) h1 -> h2 회전 행렬 
R1 = get_rotation_matrix(h1, h2)
print(f"회전행렬 R1 : {R1}")
#검산 : h1@R == h2
print(f"R1 @ h1 = {R1 @ h1},\nh2 = {h2}") 

#(2-1) R1(p1p3) -> p1'p3'로 회전 회전하기 위한 Theta2 구하기
p13 = ref_vecs[-1]
r1_p13 = R1 @ p13
p13_ = com_vecs[-1]

#R1(p1p3) 과 p1'p3'이 이루는 평면의 법선 벡터
theta2 = get_rotation_theta(r1_p13, p13_)
print(f"회전각도 Theta2 (Radian, degree) : ({theta2:.4f}, {theta2/np.pi*180:.4f})")

#(2-2) R1(p1p3) -> p1'p3' 회전 행렬 

R2 = get_rotation_matrix(r1_p13, p13_)
print(f"회전행렬 R2 : {R2}")
#검산 : R2 @ R1(p1p3) == p13
print(f"R2 @ R1(p1p3) = {R2 @ r1_p13},\nh2 = {p13_}") 
#------------------------------------------------------------
#p4 -> p4' 맞는지 확인

p4 = np.array(
    (0.500000,	0.707107,	2.828427)
)

p4_ = np.array(
    (1.498100,	0.871000,	2.883700)
)

p4_rotaion = get_rotation_pos(p4,  ref_points[0], com_points[0], R1, R2)
print(f"p4 rotaion pos = {p4_rotaion},\nanswer = {p4_}") 

#p5 -> p5' 좌표 구하기

p5 = np.array(
    (1.000000,	1.000000,	1.000000)
)

p5_rotaion = get_rotation_pos(p5,  ref_points[0], com_points[0], R1, R2)
print(f"p5 rotaion pos = {p5_rotaion}") 
