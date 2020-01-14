# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 23:11:00 2017

@author: Jan
"""


import math
import numpy as np
import random
from scipy.misc import imrotate 
from PIL import Image

numero_de_creaciones = 40 # los diseños creados iran a la carpeta con nombre WHEELS


# creacion del canvas (elemento que se repetira en cada brazo de la rueda)
for wheel in range(numero_de_creaciones):
    
    params = []

    w = 100
    h = 170
    canvas = np.zeros(( h , w ),dtype=int)
    w_sequence = list(range(1,w))
    
    
    lines = 3 #------------------------------------------------ modificable
    paint_value = 255
        
    pico_m = random.uniform( 1.4 , 1.57079633) # radianes
    pico_n = random.uniform(-500 , 0 )
    
    symmetry = False
    
    #print('\n', '       m                   n')
    #print (pico_m, pico_n,'\n')
    
    for slope in range(lines):     
    
        line =  np.zeros(( h , w ),dtype=int) # es un canvas temporal  (solo por una linea)
        shadow = np.zeros(( h , w ),dtype=int) # pintado
        
        # avoiding strokes from outside the canvas
        seen=False
        
        while not seen:
            phi = random.triangular( 1, pico_m , 1.57079633 )#radianes
            m = math.tan(phi)
            n = random.triangular(-100, pico_n, 0)
            
            # corrección analysis_v1x0 evita diseños vacios
            if m > 5:
                limit = (-35*m/2)+(115/2) #(ver analysis/params3000000areathreshold.jpg )
                if n > limit:
                    n = random.uniform(-500, limit)
                
            brush = random.randint(30,200) #------------------ modificable
            y_seen = int(m*w + n)
            if (y_seen-brush)>0:
                seen=True

        y_sym = int(m*(w/2) + n) # y = mx + n
        if y_sym > h:
            symmetry = True # for more than 3 lines becomes messy
        
        # pintar en la imagen pasando por cada columna       
        for x in w_sequence:
            # recuerda: x -> column, y -> row, visto invertido en eje horizontal
            y = int(m*x + n)#--------------------------------------------------------TRY TO MODIFY SKETCH FUNCTION

            # gradient shadow
            grad_paint = int(paint_value/brush)
            for y_pix in range(1,brush):
                y_pixclip = np.clip(y + y_pix,   0,h-1)
                shadow [  y_pixclip  ,  x ] = grad_paint*y_pix
                #simetric shadow        
                if symmetry:
                    shadow[ y_pixclip , w-x ] = grad_paint*y_pix 
                    pass
            
        # -------simetrias espejo------
                
        mirror = random.randint(0,3)#------------------------ modificable
        if mirror == 0:
            line   = np.flipud(line)
            shadow = np.flipud(shadow)
            
        if mirror == 1:
            line   = np.fliplr(line)
            shadow = np.fliplr(shadow)
            
        if mirror == 2:
            line   = np.fliplr(line)
            line   = np.flipud(line)
            shadow = np.fliplr(shadow)
            shadow = np.flipud(shadow)
            
        else: pass
    
        canvas = canvas + shadow
        
        #print (round(m,1),round(n,1), brush, mirror)
        params.extend([round(m,1),round(n,1),brush, mirror])

    
    # guardo el canvas y lo vulevo a abrir para reconfigurar los valores
    im = Image.fromarray(canvas.astype(np.uint8))
    im.save('C:/Users/Administrator/Desktop/wheelMSGv1/canvas.png')
    aux_canvas = np.asarray(Image.open('C:/Users/Administrator/Desktop/wheelMSGv1/canvas.png'))
    
    
    # poniendo la imagen creada (canvas) en una imagen mayor que contendra todos los brazos de la rueda (wheel_canvas)
    H = h*2 # size of wheel canvas
    wheel_canvas = np.zeros(( H , H ),dtype=int)
    
    for row in range(canvas.shape[0]):
        for col in range(canvas.shape[1]):
            wheel_canvas[row, col + 120] = aux_canvas[row, col]

    # mascara. Borra las partes del canvas que no interesan para dar la forma del brazo de la rueda
    im_mask = Image.open("C:/Users/Administrator/Desktop/wheelMSGv1/psd/wheelcanvas_mask.bmp")
    mask = np.array(list(im_mask.getdata(band=0)))    
    mask = np.reshape(mask, (H,H))
    mask[mask==255]=1
    
    wheel_canvas = np.multiply( wheel_canvas, mask )

    # radial symmetry. Creando los cinco brazos de la rueda
    arm = np.zeros(( H , H ),dtype=int)
    
    arm = imrotate(wheel_canvas, 72*1, interp='bilinear') # bilinear, lancsoz, bicubic   
    arm = arm + imrotate(wheel_canvas, 72*2, interp='bicubic') # bilinear, lancsoz, bicubic
    arm = arm + imrotate(wheel_canvas, 72*3, interp='bicubic') # bilinear, lancsoz, bicubic
    arm = arm + imrotate(wheel_canvas, 72*4, interp='bicubic') # bilinear, lancsoz, bicubic
    
    wheel_canvas = wheel_canvas + arm

    im_deco = Image.open("C:/Users/Administrator/Desktop/wheelMSGv1/psd/deco.png").convert('L') # deco = decorative
    arr_deco = np.asarray(im_deco)
    wheel_canvas[np.where(arr_deco > 0)] = arr_deco[np.where(arr_deco > 0)] # 
    '''    
    pico_m
    pico_n
    slope
    m
    n
    brush
    mirror

    params.insert(0,int(wheel_canvas.sum()))
    #if wheel_canvas.sum() > 0:    # treshold of area density
    # save final image wheel
    im = Image.fromarray(wheel_canvas.astype(np.uint8))    
    
    #im.save('C:/Users/Administrator/Desktop/wheelMSGv1/WHEELS_2/wheel' + str(wheel) + '.png')
    im.save('C:/Users/Administrator/Desktop/wheelMSGv1/WHEELS/' + str(params[:]) + '.png')
    #im.save('C:/Users/Administrator/Desktop/wheelMSGv1/WHEELS/' + str(wheel_canvas.sum()) + ','+ str(mirror) + '.png')
    '''
    #4700000
    if wheel_canvas.sum() > 4300000:
        # save final image wheel
        im = Image.fromarray(wheel_canvas.astype(np.uint8))    
        
        im.save('C:/Users/Administrator/Desktop/wheelMSGv1/WHEELS/wheel' + str(wheel) + '.png')
        #im.save('C:/Users/Administrator/Desktop/wheelMSGv1/WHEELS/' + str(params[:]) + '.png')
        #im.save('C:/Users/Administrator/Desktop/wheelMSGv1/WHEELS/' + str(wheel_canvas.sum()) + ','+ str(mirror) + '.png')


