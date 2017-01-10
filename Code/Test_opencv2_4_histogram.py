#!/usr/bin/python
# -*- coding: UTF-8 -*-
# face_detect.py
# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b
# Usage: python face_detect.py <image_file>

#JK完成範例 2012.07.04
#功能: Python 使用 openCV 作人臉偵測
#版本: openCV2.31 + python 2.7.2.3
#------------------------------------------
#import numpy as np
import sys, os
import cv2.cv as cv
#import cv2
#os.chdir('C:\Python27\lib\site-packages\xy') #指定目前資料夾路徑
#import highgui 
from cv import * #
#from PIL import Image, ImageDraw
#import Test_opencv2_4_kmeans as AA # import other file as class: AA
import IO_calculate as CAL
#class

#import numpy as np
 


#--------------------------------------
def get_ContourBest_LimitAda(colorimage_draw,grayimage):
    colorimage=colorimage_draw
    img_size = cv.GetSize(grayimage)#获取原始图像尺寸      
      

  #-------------清除邊框 clear edge line-------         
    clean_thick=50    
    rect_edgeclean_fill=0      
    for i in range ( img_size[1] ): # y
      for j in range ( img_size[0] ):# x         
         for k in range (  clean_thick ):# k think to clren

          if i==(0+k):grayimage[i,j] =  rect_edgeclean_fill
          if j==(0+k):grayimage[i,j] =  rect_edgeclean_fill
          if i==(img_size[1]-k):grayimage[i,j] =  rect_edgeclean_fill
          if j==(img_size[0]-k):grayimage[i,j] =  rect_edgeclean_fill
          
    #cv.ShowImage( "Display window: rect_clean ", grayimage );                   #// Show our image inside it.
    #cv.WaitKey(0);  
    #-------------/清除邊框 clear edge line/-------       

 
   
    #----------draw contour---------    
    #contour_struct=cv.CV_RETR_TREE    
    contour_struct=cv.CV_RETR_LIST    
    #contour_struct=cv.CV_RETR_EXTERNAL    
    #contour_struct=cv.CV_RETR_CCOMP    
       
    #method=cv.CV_CHAIN_CODE    
    #method=cv.CV_CHAIN_APPROX_NONE
    #method=cv.CV_CHAIN_APPROX_NONE
    #method=cv.CV_CHAIN_APPROX_SIMPLE
    #method=cv.CV_CHAIN_APPROX_TC89_L1
    method=cv.CV_CHAIN_APPROX_TC89_KCOS
  #  method=cv.CV_LINK_RUNS
    
    contours = cv.FindContours(grayimage, cv.CreateMemStorage(), contour_struct,method,(0,0))  
    img_contour = cv.CreateImage(img_size, 8, 3)# 建立一个空的灰度图 
    cv.SetZero(img_contour)
#    cv.SetZero (img_contour)
    
    if   contours:       
   #  cv.DrawContours(img_contour, n_contour, external_color=cv.RGB(255, 0, 0), hole_color=cv.RGB(0, 0, 255), max_level=2,thickness=1, lineType=8, offset=(0, 0) )
     #optional:   thickness=1, lineType=8, offset=(0, 0)
     #   cv.DrawContours( img_contour, n_contour, (0,255,0), (255,0,0), -1 )
     colors = [ (0,255,0,0),   # green
                (255,0,0,0),   # blue
                (0,0,255,0), # cyan
                (0,255,255,0), # yellow
                (0,128,0,0), # magenta
                (0,0,128,0),   # red 
                (255,0,255,0), # magenta
                (255,255,0,0),   # red 
                (128,0,128,0),   # red 
                (0,128,255,0)]   # red    
    i=0
    j=0
    #contour_countsALL=0
    contour_countsBig=0
    #contour_legthA=0 
    
    
    #--------Calculate Limit average --------------2012.0803
    contours_Pre=contours
    contour_points_sum=0
    contour_group_sum=0
    contour_points_list=list()
    
    while contours_Pre:
        area=cv.ContourArea(contours_Pre)
        
       # print "area=",area
        contour_group_sum=contour_group_sum+1
       # ct_Pre= list(contours_Pre)
        #contour_legthA_pre= ct_Pre.__len__()
        contour_points_list.append(area)                   
       # print contour_legthA_pre
       # print ct_Pre
        contour_points_sum=contour_points_sum+area
        contours_Pre = contours_Pre.h_next()# go to next contour
        
    contour_points_average=  int(contour_points_sum/contour_group_sum) # (avg add 10) for max limit
  #  print "contour_points_average=",contour_points_average 
    
    
    #----------------------
    contour_points_list.sort()
    contour_points_sum=0
    part_start=0.9
    part_end=1
    
    i_start=int(contour_points_list.__len__()*(part_start))
    i_end=int(contour_points_list.__len__()*(part_end))
    for ii in range( i_start, i_end ):
        contour_points_sum=contour_points_sum+contour_points_list[ii]
    contour_group_sum=i_end-  i_start
    contour_points_average_high=  int(contour_points_sum/contour_group_sum) # (avg add 10) for max limit
    
 #   print "contour_points_average_high",contour_points_average_high
 #   print contour_points_list  # Area list
    
    
    #--------remove small contour Area-------------------
    smallArea_list=list()
    for a in range(len(contour_points_list)):
        v=contour_points_list[a]
        if v<999 : # min Area Limit
            smallArea_list.append(v)
    for a in range(len(smallArea_list)):            
            contour_points_list.remove(smallArea_list[a])
    #--------/remove small contour Area/-------------------
    contour_points_list.pop()        
   # print contour_points_list  # Area list            
    best_contoutArea=CAL.Choose_MinErrorsum_Offset(contour_points_list,contour_points_list)
  #  print "best_contoutArea=",best_contoutArea
   #----------/Calculate Limit average/--------------
   
 
    #--------count valid contour-----------------------------      
   # contour_Limit=int( (contour_points_average_high*0.7+contour_points_average)/2 )  
   # contour_Limit=int( contour_points_average_high*0.68 )  
    contour_Limit=best_contoutArea[0]
    #contour_Limit=20
    
 #   print "contour_Limit",contour_Limit
    contours_copy=contours 
    while contours_copy:
        contour_areaA=cv.ContourArea(contours_copy)          
        if contour_areaA > contour_Limit :
            contour_countsBig= contour_countsBig+1
           
        contours_copy = contours_copy.h_next()# go to next contour
        #contour_countsALL= contour_countsALL+1  
        #print "# contour_counts ALL=",contour_countsALL
        #print "# contour_counts limitBig=",contour_countsBig
    #--------/count valid contour/-----------------------------  
        
        
    #---------get best contour------------------------
    Best_center=[0,0]    
    while contours:
       contour_areaA=cv.ContourArea(contours)                  
       if contour_areaA > contour_Limit :
           cv.DrawContours(colorimage, contours, colors[i], colors[j], 0, thickness=-1)
           i = (i+1) % len(colors)
           j = (i+1+1) % len(colors)
           #cv.ShowImage('img',img)
           #cv.WaitKey(0)
           gray_bestcontour=cv.CreateImage(img_size, 8, 1)# 建立一个空的灰度图      
           cv.CvtColor(colorimage, gray_bestcontour, cv.CV_BGR2GRAY)#转换 to Gray
           Best_center=GetBinaryImg_MassCenter( gray_bestcontour ,colorimage)
           
           break # only choose 1 big contour for the best
           
       contours = contours.h_next()# go to next contour
       #cv.ShowImage('colorimgTest',colorimage)
      # cv.WaitKey(0)
    #---------/get best contour/----------------------------   
    


      
  #  cv.ShowImage( "Display window: img_contour", img_contour )
  #  cv.WaitKey(0);
    BestContour_Center=Best_center
 #   print "BestContour_Center",BestContour_Center
    return colorimage   ,contour_countsBig ,BestContour_Center
  #  return   contours
    #-----/draw contour/-----
  







#----------------------------------------
def extract_Foreground( grayImage , binaryFBG ,Direction_fore_back):
   
   img_size = cv.GetSize( grayImage)#获取原始图像尺寸   
    #  print "x", img_size[0]
    #  print "y", img_size[1]
   if type(grayImage) == cv.cvmat:  
            grayImage = cv.GetImage(grayImage)
            
            
   for i in range ( img_size[1] ): # y
       for j in range ( img_size[0] ):# x
       
            g=binaryFBG[i,j]
            if Direction_fore_back==1: #take foreground
                if not g==0:g=1
                else:g=0
            if Direction_fore_back==0:            
                if g==0:g=1
                else:g=0
            
            v= grayImage[i,j]*g #(y,x)
            grayImage[i,j] = v  
                       
   return grayImage




#----------------------------------------
def extract_Rect_binary( color_img , pt1,pt2 ,img_drawAll):
   
   
   base_x=pt1[0]
   base_y=pt1[1]
   head_x=pt2[0]
   head_y=pt2[1]
  
   
  
   img_size = cv.GetSize(color_img)#获取原始图像尺寸
   if head_x>img_size[0]:head_x=img_size[0]
   if head_y>img_size[1]:head_y=img_size[1]
   
   if base_x<0:base_x=0
   if base_y<0:base_y=0
   
 #  print "base_x",base_x    
 #  print "base_y",base_y       
 #  print "head_x",head_x    
 #  print "head_y",head_y  
  
   grayscale=cv.CreateImage(img_size, 8, 1)# 建立一个空的灰度图      
   binary_RECT=cv.CreateImage(img_size, 8, 1)# 建立一个空的灰度图
   cv.SetZero(grayscale)    
   cv.SetZero(binary_RECT) 
   
   #cv.ShowImage( "Display window:  Rect binary " , binary_img );
   #cv.WaitKey(0);
   #cv.ShowImage( "Display window:  Rect gray " , grayscale );
   #cv.WaitKey(0);
   
  
  #---------process per polygon------------
   cv.CvtColor(color_img, grayscale, cv.CV_BGR2GRAY)#转换 to Gray     
 #  cv.ShowImage( "Display window:  binary_RECT " , binary_RECT );
 #  cv.WaitKey(0);   
#   cv.destroyWindow()
 #  cv.ShowImage( "Display window:  color to gray " , grayscale );
 #  cv.WaitKey(0);
   
  
   for j in range ( base_y , head_y ): # y        
       for i in range ( base_x,head_x ):# x                
           v= grayscale[j,i] #(y,x)
         #  print  i,j
           if v>0  :
         #if v>0 and (i%10==0) and ((j%10==0)) :
               binary_RECT[j,i] = 255  
               grayscale[j,i]=255 #(y,x) #'just to display 
               img_drawAll[j,i]=(255,255,255) #'just to display All
             #  cv.ShowImage( "Display window:  Rect binary " , binary_RECT );
             #  cv.WaitKey(0);
             
 #  cv.NamedWindow ("Display window:  Rect binary ")
 #  cv.ShowImage( "Display window:  Rect binary " , binary_RECT );
 #  cv.WaitKey(0);
   #cv.ShowImage( "Display window:  Rect gray " , grayscale );
   #cv.WaitKey(0);  
  #---------/process per polygon/------------
   
     
   #-----Calcute mass center----------------  
   pt_c=GetBinaryImg_MassCenter( binary_RECT,img_drawAll )    
  # print"x_c:"+ str(pt_c[0]) ,"y_c:"+str(pt_c[1])
  #-----/Calcute mass center/----------------

 
   return pt_c
   
       
#----------------------------------------
def GetBinaryImg_MassCenter( binary_img ,img_drawAll):
    
    mat=cv.GetMat(binary_img)    
  #  m00=0.0
  #  m10=0.0
  #  m01=0.0
    moment=cv.Moments(mat)
#    print "m00=", moment.m00
#    print "m01=",moment.m01
#    print "m10=",moment.m10
        
    x_avg=int( moment.m10 / moment.m00)
    y_avg=int( moment.m01 / moment.m00)
   # print int(x_avg) ,int(y_avg)
    pt_c=(x_avg,y_avg)
    pt1=(x_avg,y_avg)
    pt2=(x_avg+1,y_avg+1)
    
    Rectangle(img_drawAll, pt1, pt2, color=(0,255,255), thickness=5, lineType=8, shift=0)


    """
    #--------plot------------------
    img_size = cv.GetSize(binary_img)#获取原始图像尺寸
    color_img=cv.CreateImage(img_size, 8, 3)# 建立一个空的灰度图
    cv.CvtColor(binary_img, color_img, cv.CV_GRAY2BGR)#转换 to Gray
    Rectangle(color_img, pt1, pt2, color=(0,255,0), thickness=5, lineType=8, shift=0)
    cv.ShowImage( " Display window:plot Mass Center", color_img );                   #// Show our image inside it.
    cv.WaitKey(0);
    #-------/plot/------------------
    """
    
    return  pt_c
   
   

       
#----------------------------------------
def GetBinaryImg_ForeBackGround( colorimg,convert_dir ,otsu_ntimes):
    #  cam = cv2.VideoCapture(0)
    # img_name = "c:\\AG3_CD65_P150_T06O.png"
    # img_name = "c:\\people_small.jpg"
     #img = cv.LoadImage(img_name) 
     image_size = cv.GetSize(colorimg)#获取原始图像尺寸  
     grayscale = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图  
     grayscale_ini = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图  
     
     
     cv.CvtColor(colorimg, grayscale, cv.CV_BGR2GRAY)#转换 to Gray  
     cv.CvtColor(colorimg, grayscale_ini, cv.CV_BGR2GRAY)#转换 to Gray  
#     cv.ShowImage( "Display window: gray", grayscale );                   #// Show our image inside it. 
     
     
    # cv.EqualizeHist(grayscale,grayscale) 
    # cv.ShowImage( "Display window: grayimg_equ", grayscale );                   #// Show our image inside it.
    # cv.WaitKey(0);
      
        
     
     #cv.Smooth(grayscale, grayscale, cv.CV_GAUSSIAN, 5, 5,0,0)
     #cv.Smooth(grayscale_ini, grayscale_ini, cv.CV_GAUSSIAN, 5, 5,0,0)
    # block_num=11
#     block_num=median_blocksizeN
     block_num=5
     for k in range(1): #repeat N time for median filter process of all image
         cv.Smooth(grayscale,grayscale,CV_MEDIAN, block_num, block_num,0,0)
         cv.Smooth(grayscale_ini,grayscale_ini,CV_MEDIAN, block_num, block_num,0,0)
     
     #cv.Smooth(grayscale,grayscale,CV_BLUR,3,3,0,0)
     #cv.Smooth(grayscale_ini,grayscale_ini,CV_BLUR,3,3,0,0)
     
    # cv.ShowImage( "Display window: sm_gray", grayscale );                   #// Show our image inside it.
    # cv.WaitKey(0)
     
    
     #------Adative for threshold ---------------- 
     threshold_rst=100 # initial threshold will be update 
     
     for n in range(otsu_ntimes): 
         threshold= OtsuGray( grayscale ,debug = 0)
         if threshold>1: threshold_rst=threshold #cache 
            
         print "threshold" , n ,"st:", threshold
         Push_histtogram(grayscale,threshold) # push 1.st
       #  cv.ShowImage( "Display window: grayscale", grayscale );                   #// Show our image inside it.
       #  cv.WaitKey(0)

         """       
        #---------otsu plot---------------
         colorscale = cv.CreateImage(image_size, 8, 3)# 建立一个空的灰度图
         cv.CvtColor( grayscale,colorscale, cv.CV_GRAY2BGR)#转换 to Gray  
         img_drawHistogram0, histdata=getImage_Histogram( colorscale,(0,255,0),True)
          #cv.ShowImage('colorhist',img_drawHistogram0)
          # cv.WaitKey(0)
         img_drawHistogram=drawImage_Histogram( colorscale,histdata,(0,0,255),True   )
         cv.ShowImage('drawcolorhist',img_drawHistogram)
         cv.WaitKey(1000)
        #---------/otsu plot/---------------
         """ 
    # print "-----------------------"
     print "# threshold_rst:", threshold_rst
 #    print "-----------------------"
        #------/Adative for threshold/ ---------------
    
     
      
    
     #------display for test ----------------
     binaryscale = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图  
     fill_depth=255  
    # threshold_rst=26
     if convert_dir==0:
         cv.Threshold(grayscale_ini,binaryscale,(threshold_rst), fill_depth,CV_THRESH_BINARY_INV); 
     if convert_dir==1:
         cv.Threshold(grayscale_ini,binaryscale,(threshold_rst), fill_depth,CV_THRESH_BINARY);         
         
    #cv.AdaptiveThreshold(grayscale_ini,binaryscale,255,CV_ADAPTIVE_THRESH_GAUSSIAN_C, CV_THRESH_BINARY,13,5);
    # cv.Threshold(grayscale_ini,binaryscale,fill_depth,CV_ADAPTIVE_THRESH_GAUSSIAN_C, CV_THRESH_OTSU);
    
    
     #cv.ShowImage( "Display window: grayscale_ini", grayscale_ini );                   #// Show our image inside it.
     #cv.ShowImage( "Display window: binarycale", binaryscale );                   #// Show our image inside it.
     #cv.WaitKey(0);
     #cv.SaveImage("c:\\gray_ini.png",grayscale_ini)
     #cv.SaveImage("c:\\binary.png",binaryscale)
    #------/display for test/ ----------------
    # cv.ShowImage( "Display window: img", binaryscale ); 
    # cv.WaitKey(0)
     
     
     for m in range(1):
        for k in range(200):             
            cv.Dilate(binaryscale, binaryscale, iterations=1) 
            #cv.ShowImage( "Display window: Dilate", binaryscale ); 
            #cv.WaitKey(0)     
            cv.Smooth(binaryscale,binaryscale,CV_MEDIAN, 5, 5,0,0)
            #cv.ShowImage( "Display window: median", binaryscale ); 
            #cv.WaitKey(0)    
            cv.Erode(binaryscale, binaryscale, iterations=1)
            #cv.ShowImage( "Display window: erode", binaryscale ); 
            #cv.WaitKey(0)
            cv.Dilate(binaryscale, binaryscale, iterations=1)
            cv.Smooth(binaryscale,binaryscale,CV_MEDIAN, 5, 5,0,0)
            cv.Erode(binaryscale, binaryscale, iterations=1)    
        #cv.ShowImage( "Display window: binarycaleAA", binaryscale );                   #// Show our image inside it.
        #cv.WaitKey(0)
     """   
     for m in range(10):
        #for k in range(100):             
             
            cv.Erode(binaryscale, binaryscale, iterations=1)
           # cv.ShowImage( "Display window: erode", binaryscale ); 
           # cv.WaitKey(0)
            cv.Dilate(binaryscale, binaryscale, iterations=1)
            cv.Smooth(binaryscale,binaryscale,CV_MEDIAN, 5, 5,0,0)
            cv.Erode(binaryscale, binaryscale, iterations=1)    
            cv.ShowImage( "Display window: binarycaleAA", binaryscale );                   #// Show our image inside it.
            cv.WaitKey(0)
    """
     

     return binaryscale    ,threshold_rst                  
     
#----------------------------------------
def GetBinaryImg_ForeBackGround_contour( colorimg,convert_dir,threshold_rst,thin_times ):
    #  cam = cv2.VideoCapture(0)
    # img_name = "c:\\AG3_CD65_P150_T06O.png"
    # img_name = "c:\\people_small.jpg"
     #img = cv.LoadImage(img_name) 
     image_size = cv.GetSize(colorimg)#获取原始图像尺寸  
     grayscale = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图  
     grayscale_ini = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图  
     
     
     cv.CvtColor(colorimg, grayscale, cv.CV_BGR2GRAY)#转换 to Gray  
     cv.CvtColor(colorimg, grayscale_ini, cv.CV_BGR2GRAY)#转换 to Gray  
#     cv.ShowImage( "Display window: gray", grayscale );                   #// Show our image inside it. 
     
     block_num=5
     for k in range(1): #repeat N time for median filter process of all image
         cv.Smooth(grayscale,grayscale,CV_MEDIAN, block_num, block_num,0,0)
         cv.Smooth(grayscale_ini,grayscale_ini,CV_MEDIAN, block_num, block_num,0,0)
     
     """
     #------Adative for threshold ---------------- 
     threshold_rst=100 # initial threshold will be update 
     for n in range(3): 
         threshold= OtsuGray( grayscale ,debug = 0)
         if threshold>1: threshold_rst=threshold #cache 
         
      #   print "threshold" , n ,"st:", threshold
         
         Push_histtogram(grayscale,threshold) # push 1.st
       #  cv.ShowImage( "Display window: grayscale", grayscale );                   #// Show our image inside it.
       #  cv.WaitKey(0)
         
    # print "-----------------------"
    # print "# threshold_rst:", threshold_rst
 #    print "-----------------------"
        #------/Adative for threshold/ ---------------
     """
     
      
    
     #------display for test ----------------
     binaryscale = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图  
     fill_depth=255  
    # threshold_rst=26
     if convert_dir==0:
         cv.Threshold(grayscale_ini,binaryscale,(threshold_rst), fill_depth,CV_THRESH_BINARY_INV); 
     if convert_dir==1:
         cv.Threshold(grayscale_ini,binaryscale,(threshold_rst), fill_depth,CV_THRESH_BINARY);         
             
     for m in range(1):
        for k in range(100):             
            cv.Dilate(binaryscale, binaryscale, iterations=1) 
            #cv.ShowImage( "Display window: Dilate", binaryscale ); 
            #cv.WaitKey(0)     
            cv.Smooth(binaryscale,binaryscale,CV_MEDIAN, 5, 5,0,0)
            #cv.ShowImage( "Display window: median", binaryscale ); 
            #cv.WaitKey(0)    
            cv.Erode(binaryscale, binaryscale, iterations=1)
            #cv.ShowImage( "Display window: erode", binaryscale ); 
            #cv.WaitKey(0)
            cv.Dilate(binaryscale, binaryscale, iterations=1)
            cv.Smooth(binaryscale,binaryscale,CV_MEDIAN, 5, 5,0,0)
            cv.Erode(binaryscale, binaryscale, iterations=1)    
        #cv.ShowImage( "Display window: binarycaleAA", binaryscale );                   #// Show our image inside it.
        #cv.WaitKey(0)
        
     for m in range(thin_times): # make the contour be  Obvious , "thin_times" process is control parameter
        #for k in range(100):             
             
            cv.Erode(binaryscale, binaryscale, iterations=1)
           # cv.ShowImage( "Display window: erode", binaryscale ); 
           # cv.WaitKey(0)
            cv.Dilate(binaryscale, binaryscale, iterations=1)
            cv.Smooth(binaryscale,binaryscale,CV_MEDIAN, 5, 5,0,0)
            cv.Erode(binaryscale, binaryscale, iterations=1)    
           # cv.ShowImage( "Display window: binarycaleAA", binaryscale );                   #// Show our image inside it.
           # cv.WaitKey(0)
     return binaryscale          
     
#-----------------------------------------------           
def getForeground(colorimg,binaryFBG,extract_direction):
    image_size = cv.GetSize(colorimg)#获取原始图像尺寸 
     
    grayscale = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图   
    cv.CvtColor(colorimg, grayscale, cv.CV_BGR2GRAY)#转换 to Gray
   # extract_direction=0
    ForeGround_Img =extract_Foreground( grayscale , binaryFBG ,extract_direction)  
     
    ForeGround_Img_color = cv.CreateImage(image_size, 8, 3)# 建立一个空的灰度图      
    cv.CvtColor(ForeGround_Img, ForeGround_Img_color, cv.CV_GRAY2BGR)#转换 to Gray
    return       ForeGround_Img_color



   
#----------------------------------------
def OtsuGray( grayImage ,debug = 0):  
        # 如果图片是Mat对象，则转换为Image对象  
        if type(grayImage) == cv.cvmat:  
            grayImage = cv.GetImage(grayImage)  
              
        # 创建Hist  
        hist = cv.CreateHist([256],cv.CV_HIST_ARRAY,[[0,256]])  
        cv.ClearHist(hist)  
        # 计算Hist  
        cv.CalcHist([grayImage],hist)  
      
        # 开始计算  
        # 计算总亮度  
        totalH = 0  
        for h in range(0,256):  
            v = cv.QueryHistValue_1D(hist,h)  
            if v == 0 : continue  
            totalH += v*h  
            if debug > 3 : print "t=%d,%d,%d"%(h,totalH,v*h)  
              
      
        width  = grayImage.width  
        height = grayImage.height  
        total  = width*height  
          
        if debug > 1 : print "总像素:%d;总亮度:%d平均亮度:%0.2f"%(total,totalH,totalH/total)  
      
        # t=0和t=255的时候无法构成分割，所以从t=1开始计算一致到t=255  
        # 初始化v值  
        v = 0  
      
        gMax = 0.0  
        tIndex = 0  
          
        # temp  
        n0Acc = 0  
        n1Acc = 0  
        n0H   = 0  
        n1H   = 0  
        for t in range(1,255):  
            v = cv.QueryHistValue_1D(hist,t-1)  
            if v == 0: continue  
              
            n0Acc += v          #灰度小于t的像素的数目  
            n1Acc = total - n0Acc #灰度大于等于t的像素的数目  
            n0H += (t-1)*v          #灰度小于t的像素的总亮度  
            n1H = totalH - n0H  #灰度大于等于t的像素的总亮度  
      
            if n0Acc > 0 and n1Acc > 0:  
                u0 = n0H/n0Acc # 灰阶小于t的平均灰度  
                u1 = n1H/n1Acc # 灰阶大于等于t的平均灰度  
                w0 = n0Acc/total # 灰阶小于t的像素比例  
                w1 = 1.0-w0      # 灰阶大于等于t的像素的比例  
                uD = u0-u1  
                g = w0 * w1 * uD * uD  
      
                if debug > 2: 
                    print "t=%3d; u0=%.2f,u1=%.2f,%.2f;n0H=%d,n1H=%d; g=%.2f"  %(t,u0,u1,u0*w0+u1*w1,n0H,n1H,g)  
      
                if gMax < g:  
                    gMax   = g  
                    tIndex = t  
              
        if debug >0 : 
            print "gMaxValue=%.2f; t = %d ; t_inv = %d"%(gMax,tIndex,255-tIndex)              
      
        return tIndex  
   
#----------------------------------------
def Push_histtogram( grayImage ,threshold):
   
   img_size = cv.GetSize( grayImage)#获取原始图像尺寸   
    #  print "x", img_size[0]
    #  print "y", img_size[1]
   if type(grayImage) == cv.cvmat:  
            grayImage = cv.GetImage(grayImage)
            
            
   for i in range ( img_size[1] ): # y
       for j in range ( img_size[0] ):# x
            v= grayImage[i,j] #(y,x)
            if v>threshold:    
                grayImage[i,j] = threshold  
                       
    #return v

#---------------------------


#--------------------------------------
def cleanEdge_grayimage(grayimage,clean_thick):
    img_size = cv.GetSize(grayimage)#获取原始图像尺寸      
      
  #-------------清除邊框 clear edge line-------         
   # clean_thick=10    
    rect_edgeclean_fill=0      
    for i in range ( img_size[1] ): # y
      for j in range ( img_size[0] ):# x         
         for k in range (  clean_thick ):# k think to clren

          if i==(0+k):grayimage[i,j] =  rect_edgeclean_fill
          if j==(0+k):grayimage[i,j] =  rect_edgeclean_fill
          if i==(img_size[1]-k):grayimage[i,j] =  rect_edgeclean_fill
          if j==(img_size[0]-k):grayimage[i,j] =  rect_edgeclean_fill
          
    #cv.ShowImage( "Display window: rect_clean ", grayimage );                   #// Show our image inside it.
    #cv.WaitKey(0);  
    #-------------/清除邊框 clear edge line/-------       
    return grayimage



#----------------------------
def getImage_Histogram(img,BGRcolor,isLine):
        # 创建Hist  
        #hist = cv.CreateHist([256],cv.CV_HIST_ARRAY,[[0,256]])  
        
        #img = ForeGround_Img
        image_size = cv.GetSize(img)#获取原始图像尺寸  
        grayscale = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图 
        cv.CvtColor(img, grayscale, cv.CV_BGR2GRAY)#转换 to Gray 
        color_imgdraw = cv.CreateImage((256+image_size[0],image_size[1]), 8, 3)
        cv.Zero(color_imgdraw)
        for j in range(image_size[1]):
            for i in range(image_size[0]):
                   color_imgdraw[j,256+i]=img[j,i]
        #cv.Copy(img, color_imgdraw)#转换 to Gray 
        # 创建Hist
        hist = cv.CreateHist([256],cv.CV_HIST_ARRAY,[[0,256]])  
        cv.ClearHist(hist)  
        cv.CalcHist([grayscale],hist)
        NormalizeHist(hist,1)
             
        HH=cv.GetMinMaxHistValue(hist)
        min_v=HH[0]
        max_v=HH[1]
     #   print HH
     #   print "max_v ,min_v",max_v ,min_v
        hist_data=list()
        
    
                   
        fullscale=10000
        min_v=fullscale*min_v
        max_v=fullscale*max_v          
        #---------for plot 256 histogram--------------------------    
        for i in range(0,256):
            v=cv.QueryHistValue_1D(hist,i)
            v=  fullscale*(v)                        
            #print v
            #hist_data.append((v))
            hist_data.append( (v)  )
        
            v= 256* (v-min_v)/(max_v-min_v)
            #print v                
            pt1=(i,image_size[1])
            pt2=(i ,image_size[1]-int(v+5))
            CircleCenter=pt2
            Radius=1;
            #Color=CV_RGB(0,255,0);
            Color=BGRcolor;
            Thickness=2;
            Shift=0
            #Line(img, (0,image_size[1]-0),(255,image_size[1]-0), color=(255,255,255), thickness=10, lineType=8, shift=0)         
            #Line(img, (0,image_size[1]-0),(0,image_size[1]-255), color=(255,255,255), thickness=10, lineType=8, shift=0)        
            #Line(img, (0,image_size[1]-255),(255,image_size[1]-255), color=(255,255,255), thickness=10, lineType=8, shift=0)         
            if isLine==True: 
                Line(color_imgdraw, pt1,pt2, color=(0,255,0), thickness=3, lineType=2, shift=0)
            Circle(color_imgdraw,CircleCenter,Radius,Color,Thickness,CV_AA,Shift);        
            
        #cv.ShowImage('color_imgdraw',color_imgdraw)
        #cv.WaitKey(0)
        
        #---------/for plot 256 histogram/--------------------------
        print "hist_data sum=",sum(hist_data)
        
        return color_imgdraw ,hist_data

    
#---------------------------------------    
def drawImage_Histogram(colorimg,hist_data,BGRcolor,isDrawLine):
        # 创建Hist
        image_size = cv.GetSize(colorimg)#获取原始图像尺寸 
        color_imgdraw = cv.CreateImage(image_size, 8, 3)# 建立一个空的灰度图  
        cv.Copy(colorimg, color_imgdraw)#转换 to Gray 
        #img = ForeGround_Img
        #image_size = cv.GetSize(img)#获取原始图像尺寸  
        #grayscale = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图  
        #cv.CvtColor(img, grayscale, cv.CV_BGR2GRAY)#转换 to Gray 
       
       # hist_data256=list(hist_data)
       # while len(hist_data256)<256:
       #     hist_data256.append(0)
            #print hist_data
  
        print "len(hist_data)",len(hist_data)
        for i in range(0,len(hist_data)):
            v=  hist_data[i]
            #print v
            pt1=(i,image_size[1])
            pt2=(i ,image_size[1]-int(v+5))
            CircleCenter=pt2
            Radius=1;
            Color=BGRcolor;
            Thickness=2;
            Shift=0
            #Line(img, (0,image_size[1]-0),(255,image_size[1]-0), color=(255,255,255), thickness=10, lineType=8, shift=0)         
            #Line(img, (0,image_size[1]-0),(0,image_size[1]-255), color=(255,255,255), thickness=10, lineType=8, shift=0)        
            #Line(img, (0,image_size[1]-255),(255,image_size[1]-255), color=(255,255,255), thickness=10, lineType=8, shift=0)         
            if isDrawLine==True:
                Line(color_imgdraw, pt1,pt2, color=(0,255,255), thickness=2, lineType=2, shift=0)
            Circle(color_imgdraw,CircleCenter,Radius,Color,Thickness,CV_AA,Shift);        
            
      #  cv.ShowImage('colorhist',img)
       # cv.WaitKey(0)
        return color_imgdraw
#---------------------------------------------

#---------------------------------------------
#---------------------------------------------
def drawNewImage_Histogram(hist_data,GBRcolor,isLinePlot):
        # 创建Hist
        image_size =(256,256)#获取原始图像尺寸 
        color_imgdraw = cv.CreateImage(image_size, 8, 3)# 建立一个空的灰度图 
        cv.Zero(color_imgdraw)
        #cv.Copy(colorimg, color_imgdraw)#转换 to Gray 
        #img = ForeGround_Img
        #image_size = cv.GetSize(img)#获取原始图像尺寸  
        #grayscale = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图  
        #cv.CvtColor(img, grayscale, cv.CV_BGR2GRAY)#转换 to Gray 
       
        # hist_data256=list(hist_data)
        # while len(hist_data256)<256:
        #     hist_data256.append(0)
            #print hist_data
  
        print "len(hist_data)",len(hist_data)
        for i in range(0,len(hist_data)):
            v=  hist_data[i]
            #print v
            pt1=(i,image_size[1])
            pt2=(i ,image_size[1]-int(v+5))
            CircleCenter=pt2
            Radius=1;
            Color=GBRcolor
            #Color=CV_RGB(255,0,0);
            Thickness=1;
            Shift=0
            #Line(img, (0,image_size[1]-0),(255,image_size[1]-0), color=(255,255,255), thickness=10, lineType=8, shift=0)         
            #Line(img, (0,image_size[1]-0),(0,image_size[1]-255), color=(255,255,255), thickness=10, lineType=8, shift=0)        
            #Line(img, (0,image_size[1]-255),(255,image_size[1]-255), color=(255,255,255), thickness=10, lineType=8, shift=0)         
            Circle(color_imgdraw,CircleCenter,Radius,Color,Thickness,CV_AA,Shift);                                
            if isLinePlot==True:
                Line(color_imgdraw, pt1,pt2, color=(0,255,255), thickness=2, lineType=2, shift=0)
            
        #  cv.ShowImage('colorhist',img)
        # cv.WaitKey(0)
        return color_imgdraw
#---------------------------------------------
              
#---------main-----------------------------------
#---------main-------------------------------
if __name__ == "__main__":

#-----FreBackGround-------------------
    #img_name = "c:\\AG3_CD65_P150_T06O.png"  
    #img_name = "c:\\bad02.png"
    img_name = "c:\\hard01.png"
    img = cv.LoadImage(img_name)
    image_size = cv.GetSize(img)#获取原始图像尺寸 
    #median_blocksize=5 # min >=5  fixed   
    binaryFBG,threshold=GetBinaryImg_ForeBackGround(img,1,6)      
    #cv.ShowImage( "Display window: binarycale", binaryFBG );                   #// Show our image inside it.
    #cv.WaitKey(0);
    
    #----extract Fore Ground---------- 
    ForeGround_Img=getForeground(img,binaryFBG,extract_direction=0)    
    #cv.ShowImage('Fore Ground to measure', ForeGround_Img)
   # cv.WaitKey(0)
       
    #Fore_Img_color = cv.CreateImage(image_size, 8, 3)# 建立一个空的灰度图   
    #cv.CvtCo8lor(Fore_Img, Fore_Img_color, cv.CV_GRAY2BGRA)#转换 to Gray        
    #cv.SaveImage("c:\\aaa.png",Fore_Img_color)
    #----/extract Fore Ground/----------    
    
    img_drawHistogram0, histdata=getImage_Histogram( ForeGround_Img,(0255,0),True)
    #cv.ShowImage('colorhist',img_drawHistogram0)
   # cv.WaitKey(0)
    img_drawHistogram=drawImage_Histogram(  ForeGround_Img,histdata,(0,0,255),True   )
    cv.ShowImage('drawcolorhist',img_drawHistogram)
    cv.WaitKey(0)
    
    
  
  
    
        
#-----/ForeBackGround/-------------------


"""  
#------ main Feature contour Analyize----------------
    # nc=get_contour(grayscale_ini)
    colorimage = cv.LoadImage(img_name)
    draw_img= colorimage
    #contour_minLimitPoints=60
    contour_img,contour_Num=get_contourB_limitAvg(draw_img ,binaryFBG)
    #nA=AA.get_contourA(binaryscale) # from  Test_opencv2_4_kmeans.py
    #print contour_Num    
    cv.ShowImage('Find contour_img',contour_img)
    cv.WaitKey(0)
#------ /main Feature contour Analyize/----------------
""" 
                                    
""" 
# IML
 img_name = "c:\\AG3_CD65_P150_T06O.png"
 im = Image.open(img_name)
 image = im.convert("L")
 image.load()
 putpixel = image.im.putpixel
 getpixel = image.im.getpixel
 v=0
 s=[0, 0]
 for i in range ( image.size[0] ):
     for j in range ( image.size[1] ):
           v= getpixel(( i,j ))
           if v>threshold:    
                putpixel( (i , j) , threshold-1 )
            
 image.show()
 """


