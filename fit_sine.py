import sys
import numpy as np
import cv2
from enum import Enum

RED = (0,0,255)
ORANGE = (0,50,255)
YELLOW = (0,255,255)
GREEN = (0,255,0)
BLUE = (255,0,0)
NAVY = (255,51,0)
PURPLE = (255,0,100)
WHITE = (255,255,255)
RAINBOW = [RED, ORANGE, YELLOW, GREEN, BLUE, NAVY, PURPLE]
WINDOW_H, WINDOW_W = 480, 640

tolerence = 1
MAX_ITER = 500
a, b, c, d = 0, 0, 0, 0
PARAM_NUM = 4

def compute_residual(points, params):
    a,b,c,d = params
    y_pred = a*np.sin(b*points[:, 0] + c) + d
    res = y_pred - points[:, 1]
    return res

def compute_jacobian(points, params) :
    a,b,c,d = params
    num_points = len(points)
    jaco = np.zeros((num_points, PARAM_NUM))


    jaco[:, 0] = np.sin(b*points[:, 0] + c)
    jaco[:, 1] = a*points[:, 0]*np.cos(b*points[:, 0] + c)
    jaco[:, 2] = a*np.cos(b*points[:, 0] + c)
    jaco[:, 3] = 1

    return jaco

import sympy
from sympy import symbols, diff, Matrix, solve, Abs
a,b,c,d,x,y = symbols('a,b,c,d,x,y')
res = (a*sympy.sin(b*x + c) + d) -y
print(f"r_i / a = {diff(res, a)}") 
print(f"r_i / b = {diff(res, b)}") 
print(f"r_i / c = {diff(res, c)}") 
print(f"r_i / d = {diff(res, d)}") 




def on_mouse(event, x, y, flags, param):
    # event는 마우스 동작 상수값, 클릭, 이동 등등
    # x, y는 내가 띄운 창을 기준으로 좌측 상단점이 0,0이 됌
    # flags는 마우스 이벤트가 발생할 때 키보드 또는 마우스 상태를 의미, Shif+마우스 등 설정가능
    # param은 영상이룻도 있도 전달하고 싶은 데이터

    global points, draw_on, bg, params
    
    if event == cv2.EVENT_LBUTTONDOWN and draw_on: # 왼쪽이 눌러지면 실행
        points.append((x,y))
        print('EVENT_LBUTTONDOWN: %d, %d' % (x, y)) # 좌표 출력

    elif event == cv2.EVENT_LBUTTONUP and draw_on:
        #점 찍기
        cv2.line(bg, points[-1], points[-1], (np.random.randint(0,256),np.random.randint(0,256),np.random.randint(0,256)), 5, cv2.LINE_AA)  
        # cv2.putText(bg, f"{chr(64+len(points))}'({x},{y})", (x-10,y-10), cv2.FONT_HERSHEY_PLAIN, 1.0, WHITE, 1, cv2.LINE_AA)
        cv2.imshow(name, bg)
        print(f'입력 받은 좌표: {points}') # 좌표 출력

    elif event == cv2.EVENT_RBUTTONDOWN :
        #근사 직선 그리기
        if len(points) >= 3  and draw_on:
            past_bg = bg.copy()
            points = np.array(points)
         
            a, b, c, d = np.std(points[:,1]), 0.001, 1.0, np.mean(points[:,1])
            x = np.linspace(0, WINDOW_W, 1000)
            for i in range(MAX_ITER) :
                bg = past_bg.copy()
                r = compute_residual(points, [a,b,c,d])
                J = compute_jacobian(points, [a,b,c,d])

                diff = np.linalg.inv(J.T @ J + 1e-5*np.diag(np.diag(J.T @ J))) @ J.T @ r
                a, b, c, d = np.array([a,b,c,d]) -  diff

                y = a*np.sin(b*x + c) + d
                cv2.polylines(bg, np.dstack([x, y]).astype(int), False, GREEN, 1)

                cv2.putText(bg, f'Iter : {i}', (10, 20), cv2.FONT_HERSHEY_PLAIN, 1.0, GREEN, 1, cv2.LINE_AA)   
                cv2.imshow(name, bg)
                cv2.waitKey(10) 
        
                if np.sqrt(np.sum(r**2)) < tolerence :
                    break
   
            cv2.putText(bg, f'Iter : {i} complete', (10, 20), cv2.FONT_HERSHEY_PLAIN, 1.0, GREEN, 1, cv2.LINE_AA)   
            cv2.imshow(name, bg)

            draw_on = False

    elif event == cv2.EVENT_RBUTTONDBLCLK :
        #다시 그리기
        draw_on = True
        points = []
        bg = np.ones((WINDOW_H, WINDOW_W, 3), dtype=np.uint8) * 0
        cv2.imshow(name, bg)
    

draw_on = True
points = []
v2_left_m = []
v2_right_m = []
v3_left_m = []

# 흰색 배경 이미지 생성
bg = np.ones((WINDOW_H, WINDOW_W, 3), dtype=np.uint8) * 0

# 윈도우 창
name = 'Fit Line'
cv2.namedWindow(name)

# 마우스 입력, namedWIndow or imshow가 실행되어 창이 떠있는 상태에서만 사용가능
# 마우스 이벤트가 발생하면 on_mouse 함수 실행
cv2.setMouseCallback(name, on_mouse, bg)

# 영상 출력
cv2.imshow(name, bg)
cv2.waitKey()
cv2.destroyAllWindows()