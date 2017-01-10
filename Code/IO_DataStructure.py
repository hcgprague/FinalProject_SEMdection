# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 10:16:38 2012

@author: jqhuang
"""

# -*- coding: utf-8 -*-

from __future__ import division  # 使用float 除法
import os
os.chdir('C://Temp') #指定目前資料夾路徑
import sys
import cv2.cv as cv
#os.chdir('C:\Python27\lib\site-packages\xy') #指定目前資料夾路徑
#import highgui 
from cv import * 
from PIL import Image, ImageDraw

import Test_opencv2_4_histogram as FBG
import IO_calculate as CAL

 
class Class0_image_table:
    """data structure for output file column :B1 B2 B3 B4 """
    IMAGE="path"
    pattern_series=""
    split_variation=""
    highlight_name=""
    process_condition=""
    repeat_take=""
    
    #-----new Add-----
    defect_index=""
    
    def initial(self,line_array,Cimg):
             
                Cimg.IMAGE=line_array[0]
                Cimg.pattern_series=line_array[1]
                Cimg.split_variation=line_array[2]
                Cimg.highlight_name=line_array[3] #AL3_CD65_P200  AK3_CD65_P190
                #  print     Cimg.highlight_name
                Cimg.process_condition=line_array[4]
                Cimg.repeat_take=line_array[5].replace("\n","")
                Cimg.defect_index=line_array[6].replace("\n","")
               # testlineA=Cimg.IMAGE
                imgsize_x=0.01
                imgsize_y=0.01
                                
                return Cimg 
             
    
    def PreCount_polygonNumber(self,Lines_highlight, Lines_polygon):
        #-------------------------PreCount polygon conuts---------------------                    
        for lineB in Lines_highlight: #stage B
            Chilight= Class1_highlight_window()
            line_array = lineB.split("\t")
            if not str(line_array[2]).__contains__("base"):  #number sureance
            
                 Chilight.HIGHLIGHT=line_array[0]  #AG3_CD65_P150  AG3_CD65_P160
                 #print Chilight.HIGHLIGHT
        
                 if  Chilight.HIGHLIGHT.__contains__( self.highlight_name):
                    highlight_Polygons=0
                    #-----------polygon conuts-----------------                    
                    for lineC1 in Lines_polygon: #stage C1
                        #print lineC1
                        Cpolygon= Class2_cell_polygon()
                        line_array = lineC1.split("\t")
                        #Cpolygon.POLYGON=line_array[0] # POLYGON:  P1
                        Cpolygon.POLYGON=line_array[6] # hilight_polygon: AG3_CD65_P150
                            
                        if not str(line_array[2]).__contains__("base"):  #number sureance   
                            if  Cpolygon.POLYGON.__contains__( Chilight.HIGHLIGHT):
                              #  print Chilight.HIGHLIGHT, Cpolygon.POLYGON
                              highlight_Polygons=highlight_Polygons+1
                            
                    #-----------/polygon conuts/---------------------
        #print "++++++++++++++++++"
        #print " CC highlight_Polygons", highlight_Polygons
    
        return highlight_Polygons
        
        #---------------------------------------
    def getImgFileName( self,file_path):
        img_filename_array=file_path.split("/")
        img_filename=""
        for line in img_filename_array:
            if line.__contains__("."):
                img_filename=line
        
        return img_filename
        #print "img_filename",img_filename  
        #--------------------------------------  
        
        
    def PreCount_polygonOffset(self,Cimg,Chighlight,Cconfig, Lines_polygon,BestContourCenter):
            #-------------------------PreCount polygon conuts---------------------                    
                     #print Chilight.HIGHLIGHT
                     
                     if  Chighlight.HIGHLIGHT.__contains__( Cimg.highlight_name):
                      #  highlight_Polygons=0
                        Dmin_xy=100*100
                        
                        Bestpolygon_offset_x=0
                        Bestpolygon_offset_y=0
                        Bestpolygon_center_x=0
                        Bestpolygon_center_y=0
                        #-----------polygon conuts offset-----------------                    
                        for lineC1 in Lines_polygon: #stage C1
                            #print lineC1
                            
                            Cpolygon= Class2_cell_polygon()
                            line_array = lineC1.split("\t")
                            #Cpolygon.POLYGON=line_array[0] # POLYGON:  P
                            #print"#Cpolygon.error_range=", Cpolygon.error_range     
                            if not str(line_array[2]).__contains__("base"):  #number sureance
                                Cpolygon.POLYGON=line_array[0]  
                                Cpolygon.polygon_type=line_array[1]
                                Cpolygon.polygon_base_x= float(line_array[2])
                                Cpolygon.polygon_base_y=float(line_array[3])
                                Cpolygon.polygon_head_x=float(line_array[4])
                                Cpolygon.polygon_head_y=float(line_array[5])
                                Cpolygon.parent_highlight=line_array[6].replace("\n","")
                           
                                Cpolygon.error_range=int(Cconfig.ALIGNMENT_RANGE)
                                #print    line_array[2]  
                        
                                if  Cpolygon.parent_highlight.__contains__( Chighlight.HIGHLIGHT):
                                 # print Chilight.HIGHLIGHT, Cpolygon.POLYGON
                                 # highlight_Polygons=highlight_Polygons+1
                                  #------------draw_polygon --------------------------------                    
                                  dx_base=int(Cpolygon.polygon_base_x-Chighlight.highlight_base_x)
                                  dy_base=int(Cpolygon.polygon_base_y-Chighlight.highlight_base_y)
                                  dx_head=int(Cpolygon.polygon_head_x-Chighlight.highlight_base_x)
                                  dy_head=int(Cpolygon.polygon_head_y-Chighlight.highlight_base_y)
                                
                                  dx_center=(dx_head-dx_base)/2  +dx_base #nm
                                  dy_center=(dy_head-dy_base)/2  +dy_base#nm
                                 #print "#dx_highlight:",(dx_head-dx_base)
                                 #print "#dy_hilight:",(dy_head-dy_base)
                                 # print "#hilight_center(x,y):",dx_center ,dy_center
                                 
                                 #----nm To pixels------------
                                  pt_c=(    int(dx_center/Chighlight.scale_x) , int(dy_center/Chighlight.scale_y)   )
                                  pt1=( int( abs(dx_base)/Chighlight.scale_x),int( (dy_base/Chighlight.scale_y)   )    )
                                  pt2=( int( abs(dx_head)/Chighlight.scale_x),int((dy_head/Chighlight.scale_y)    )     ) 
                                 #----/nm To pixels/------------
                                  print "p_base p_head p_center",pt1 ,pt2 ,pt_c
                                  
                             
                                #  print "Chilight.highlight_base_x",Chilight.highlight_base_x
                                #  print "polygon_center_x",polygon_center_x
                                #  print "polygon_center_y",polygon_center_y
                                  #---------decide Nearest polygon offset---------------------------
                                  polygon_center_x=pt_c[0] # pixel
                                  polygon_center_y=pt_c[1] # pixel
                                  D_xy=abs(BestContourCenter[0]-polygon_center_x)**2 +abs(BestContourCenter[1]-polygon_center_y)**2
                                     
                                  if  D_xy< Dmin_xy:
                                      Dmin_xy=D_xy
                                      Bestpolygon_offset_x= polygon_center_x-BestContourCenter[0]
                                      Bestpolygon_offset_y= polygon_center_y-BestContourCenter[1]
                                      
                                      Bestpolygon_center_x=polygon_center_x
                                      Bestpolygon_center_y=polygon_center_y # y follow x , (x,y)is the sameset
                                  #---------/decide Nearest polygon offset/---------------------------
                                                     
                        #-----------/polygon conuts offset/---------------------
                        BestPolygonCenter=[ Bestpolygon_center_x, Bestpolygon_center_y]
                        BestPolygonOffset=[Bestpolygon_offset_x,Bestpolygon_offset_y]
                        return BestPolygonCenter ,BestPolygonOffset  
            #print "++++++++++++++++++"
            #print " CC highlight_Polygons", highlight_Polygons
    
                     
         #--------------------------/PreCount polygon conuts/---------------------    
    
class Class1_highlight_window:
    HIGHLIGHT=""
    highlight_base_x	=0.0
    highlight_base_y	=0.0
    highlight_head_x	=0.0
    highlight_head_y	=0.0
    pattern_series=""	
    split_variation=""

    #----JK add-----
    scale_x=0.0 
    scale_y=0.0
    Bigoffset_x=0
    Bigoffset_y=0
    Smalloffset_x=0
    Smalloffset_y=0
    
    
    
    def initial(self,line_array,Chilight):
                Chilight.HIGHLIGHT=line_array[0]  #AG3_CD65_P150  AG3_CD65_P160
              #  print Chilight.HIGHLIGHT
                Chilight.highlight_base_x=float( line_array[1] )        
                #print "-highlight_base_x=",Chilight.highlight_base_x                
                Chilight.highlight_base_y=float( line_array[2] )
                #print "-highlight_base_y=",Chilight.highlight_base_y
                Chilight.highlight_head_x=float( line_array[3] )
             #   print "highlight_head_x=",Chilight.highlight_head_x                
                                  
             #   print"hilight_interval_x:",hilight_interval_x                
                Chilight.highlight_head_y=float( line_array[4])
                Chilight.pattern_series=line_array[5]
                Chilight.split_variation=line_array[6].replace("\n","")
                return Chilight 
             
#================================================   
class Class2_cell_polygon:
    POLYGON	=""
    polygon_type=""	
    polygon_base_x=0.0	
    polygon_base_y=0.0	
    polygon_head_x=0.0	
    polygon_head_y=0.0	
    parent_highlight=""
 
    #----JK add-----
    error_range=0
    
    
    #----JK add-----
    def initial(self,line_array,Cpolygon,Cconfig):
               Cpolygon.POLYGON=line_array[0]  
               Cpolygon.polygon_type=line_array[1]
               Cpolygon.polygon_base_x= float(line_array[2])
               Cpolygon.polygon_base_y=float(line_array[3])
               Cpolygon.polygon_head_x=float(line_array[4])
               Cpolygon.polygon_head_y=float(line_array[5])
               Cpolygon.parent_highlight=line_array[6].replace("\n","")  
               Cpolygon.error_range=int(Cconfig.ALIGNMENT_RANGE)
               return Cpolygon 
               
    def draw_Polygon_rect(self,ForeGroundImg_color,pt1,pt2,colorBGR):        
        # img_name = "c:\\AG3_CD65_P150_T06O.png"
        # img_name = "c:\\people_small.jpg"
        #img = cv.LoadImage(img_name) 
        image_size = cv.GetSize(ForeGroundImg_color)#获取原始图像尺寸 
        color_imgdraw = cv.CreateImage(image_size, 8, 3)# 建立一个空的灰度图  
        cv.Copy(ForeGroundImg_color, color_imgdraw)#转换 to Gray 
        Rectangle(color_imgdraw, pt1, pt2, color=colorBGR, thickness=2, lineType=2, shift=0)
       #    print "pt1-pt2" pt1 ,pt2   
       #    baseP=str(pt2[0])+","+str(pt2[1])
       #    headP=str(pt1[0])+","+str(pt1[1])     
       #   print baseP
       #  print headP 
       # cv.ShowImage( "Display window: rect " , ForeGroundImg_color );
       # cv.ShowImage( "Display window: rect ("+baseP+"),("+headP+")" , ForeGroundImg_color );
       #cv.WaitKey(1000);
        return color_imgdraw
    

class Class3_measure_gauge:
    GAUGE=""
    gauge_base_x=0.0
    gauge_base_y=0.0
    gauge_head_x=0.0
    gauge_head_y=0.0
    gauge_tone=""
    parent_highlight=""
    measure_mode=""
    measure_range=0
    measure_number=0
    
    #--------JK add---------
    error_range=0
    def initial(self,line_array,Cconfig,Cmeasure):
         Cmeasure.GAUGE=line_array[0] #image
         Cmeasure.gauge_base_x=float(line_array[1])
         Cmeasure.gauge_base_y=float(line_array[2])
         Cmeasure.gauge_head_x=float(line_array[3])
         Cmeasure.gauge_head_y=float(line_array[4])
         Cmeasure.gauge_tone=line_array[5]
         Cmeasure.parent_highlight=line_array[6]
         Cmeasure.measure_mode=line_array[7]
         Cmeasure.measure_range=float(line_array[8])
         Cmeasure.measure_number=float(line_array[9].replace("\n",""))                            
         Cmeasure.error_range=int(Cconfig.GAUGE_EXTENSION) #nm
         return Cmeasure
   
    def draw_gaugeLineALL(self,ForeGroundImg_color,pt1,pt2,gauge_extend,measure_range,measure_number):        
        line_type="LineType"
        pt1_new=[0,0]
        pt2_new=[0,0]
        pt1_collect=list()
        pt2_collect=list()
        K_interval=int( measure_range/measure_number) #300 /20 =15
        n_times=int(measure_number/2) 
        pt1_LeftLast=[0,0]
        pt2_LeftLast=[0,0]
        pt1_RightLast=[0,0]
        pt2_RightLast=[0,0]  
#        print pt1
        
       # pt_center=(0,0)    
      #-------LINE direction judge---------
        if pt1[0]==pt2[0]:
            #print "vertical Line"
            line_type="vertical Line"
        if pt1[1]==pt2[1]:
          #  print "horizontal Line"
            line_type= "horizontal Line"
        if not pt1[0]==pt2[0] and not pt1[1]==pt2[1]:    
            line_type= "m Line"                
      #      dx= pt1[0]-pt2[0]
      #      dy= pt1[1]-pt2[1]
      #      m=dy/dx       
       #-------/LINE direction judge/---------
              
       #----------------
        img_size = cv.GetSize(ForeGroundImg_color)#获取原始图像尺寸
        img_draw = cv.CreateImage(img_size, 8, 3)# 建立一个空的灰度图
        
        cv.SetZero(img_draw)
        cv.Copy(ForeGroundImg_color ,img_draw)
      #  Line(img_draw, pt1, pt2, color=(0,255,0), thickness=1, lineType=8, shift=0)
      #  print "pt1-pt2", pt1,pt2, line_type
       
    #-------------- extend gauge----------  
    #   gauge_extend=10
        pt1=list(pt1)
        pt2=list(pt2)                
        pt1[0]=pt1[0]-gauge_extend
        pt1[1]=pt1[1]
        pt2[0]=pt2[0]+gauge_extend
        pt2[1]=pt2[1]
    #-------------- /extend gauge/----------  
        Line(img_draw, (pt1[0],pt1[1]), (pt2[0],pt2[1]), color=(0,255,0), thickness=1, lineType=8, shift=0)
        
        pt1_new[0]=int(pt1[0])
        pt1_new[1]=int(pt1[1])
        pt2_new[0]=int(pt2[0])
        pt2_new[1]=int(pt2[1])                
        pt1_collect.append(  (pt1_new[0],pt1_new[1] ) )
        pt2_collect.append(  (pt2_new[0],pt2_new[1] ) )
      
 
       # cv.ShowImage( "Display window: gaugeLine " , img_draw );
       # cv.WaitKey(0);   
      #-----draw update pt1 pt2------------------ 
       # n_times=int(gauge_extend_lines/K_interval)     
        if  line_type=="m Line" or line_type=="vertical Line" :       
            #--------------------------------            
            #Left( positive )Direction 
            pt1_new[0]=int(pt1[0])
            pt1_new[1]=int(pt1[1])
            pt2_new[0]=int(pt2[0])
            pt2_new[1]=int(pt2[1])                        
            for i in range(n_times): 
                pt1_new[0]=pt1_new[0]+ K_interval      
                pt2_new[0]=pt2_new[0]+ K_interval    
              #  print "left pt1-pt2", pt1_new,pt2_new
                pt1_collect.append(  (pt1_new[0],pt1_new[1])  )
                pt2_collect.append(  (pt2_new[0],pt2_new[1])  )           
                Line(img_draw, (pt1_new[0],pt1_new[1]), (pt2_new[0],pt2_new[1]), color=(255,255,255), thickness=1, lineType=8, shift=0)
    
            #--------------------------------
            #Right(negative) Direction
            pt1_new[0]=int(pt1[0])
            pt1_new[1]=int(pt1[1])
            pt2_new[0]=int(pt2[0])
            pt2_new[1]=int(pt2[1])             
            for i in range(n_times): 
                pt1_new[0]=pt1_new[0]- K_interval      
                pt2_new[0]=pt2_new[0]-K_interval    
                #print "left pt1-pt2", pt1_new,pt2_new
                pt1_collect.append(  (pt1_new[0],pt1_new[1])  )
                pt2_collect.append(  (pt2_new[0],pt2_new[1])  ) 
                Line(img_draw, (pt1_new[0],pt1_new[1]), (pt2_new[0],pt2_new[1]), color=(255,255,255), thickness=1, lineType=8, shift=0)
        if  line_type=="horizontal Line":
            #positive dir 
            pt1_new[0]=int(pt1[0])
            pt1_new[1]=int(pt1[1])
            pt2_new[0]=int(pt2[0])
            pt2_new[1]=int(pt2[1])                          
            for i in range(n_times): 
                pt1_new[1]=pt1_new[1]+ K_interval      
                pt2_new[1]=pt2_new[1]+ K_interval 
               # print " pt1_new[1]=" ,pt1_new[1]
               # print "left pt1-pt2", pt1_new,pt2_new
                pt1_collect.append(  (pt1_new[0],pt1_new[1])  )
                pt2_collect.append(  (pt2_new[0],pt2_new[1])  )             
                Line(img_draw, (pt1_new[0],pt1_new[1]), (pt2_new[0],pt2_new[1]), color=(255,255,255), thickness=1, lineType=8, shift=0)
        
            #----------------------------------   
            #Negitive dir                  
            pt1_new[0]=int(pt1[0])
            pt1_new[1]=int(pt1[1])
            pt2_new[0]=int(pt2[0])
            pt2_new[1]=int(pt2[1]) 
            for i in range(n_times): 
                pt1_new[1]=pt1_new[1]- K_interval      
                pt2_new[1]=pt2_new[1]-K_interval    
                #print "left pt1-pt2", pt1_new,pt2_new
                pt1_collect.append(  (pt1_new[0],pt1_new[1])  )
                pt2_collect.append(  (pt2_new[0],pt2_new[1])  )  
                Line(img_draw, (pt1_new[0],pt1_new[1]), (pt2_new[0],pt2_new[1]), color=(255,255,255), thickness=1, lineType=8, shift=0)           
            #print "horizontal Line RightLast:"                 
      #-----/draw  update pt1 pt2/-------------------
        
        
        
        #--------gauge ROI ----------------------------------
        pt1_LeftLast=pt1_collect[n_times]
        pt2_LeftLast=pt2_collect[n_times]
        pt1_RightLast=pt1_collect[2*n_times]
        pt2_RightLast=pt2_collect[2*n_times]
        print"pt1_base_LeftLast,pt2_head_LeftLast =",pt1_LeftLast,pt2_LeftLast
        print"pt1_base_RightLast,pt2_head_RightLast =",pt1_RightLast,pt2_RightLast
           #img = cv.LoadImage(img_name)
        gauge_ROI_size_x_max=0
        Dx_list=list()
        Dx_L1L2=abs(pt1_LeftLast[0]-pt2_LeftLast[0])
        Dx_L1R2=abs(pt1_LeftLast[0]-pt2_RightLast[0])
        Dx_L1R1=abs(pt1_LeftLast[0]-pt2_RightLast[0])
        Dx_list.append(Dx_L1L2)
        Dx_list.append(Dx_L1R2)
        Dx_list.append(Dx_L1R1)
        Dx_list.sort()
        gauge_ROI_size_x_max=Dx_list[len(Dx_list)-1]
        print"gauge_ROI_size_x_max=",gauge_ROI_size_x_max
        
        gauge_ROI_size_y_max=0
        Dy_list=list()
        Dy_L1L2=abs(pt1_LeftLast[1]-pt2_LeftLast[1])
        Dy_L1R2=abs(pt1_LeftLast[1]-pt2_RightLast[1])
        Dy_L1R1=abs(pt1_LeftLast[1]-pt2_RightLast[1])
        Dy_list.append(Dy_L1L2)
        Dy_list.append(Dy_L1R2)
        Dy_list.append(Dy_L1R1)
        Dy_list.sort()
        gauge_ROI_size_y_max=Dy_list[len(Dy_list)-1]
        print"gauge_ROI_size_y_max=",gauge_ROI_size_y_max
                
        ROI_size = (gauge_ROI_size_x_max,gauge_ROI_size_y_max)
        gauge_ROI_gray = cv.CreateImage(ROI_size, 8, 1)# 建立一个空的灰度图 
        img_size = cv.GetSize(ForeGroundImg_color)#获取原始图像尺寸
        ForeGroundImg_gray = cv.CreateImage(img_size, 8, 1)# 建立一个空的灰度图
        cv.CvtColor(ForeGroundImg_color, ForeGroundImg_gray, cv.CV_BGR2GRAY)#转换 to Gray
        
        
        for j in range ( ROI_size[1] ): # y
            for i in range ( ROI_size[0] ):# x
                centerP=(i+pt1_RightLast[0],  j+pt1_RightLast[1]  )
                #print"center",centerP
                
                #Circle(img_draw,centerP,1,(255,255,0),1,CV_AA,0);
                
                g=  ForeGroundImg_gray[centerP[1],centerP[0]] #(y,x)
                gauge_ROI_gray[j,i] = g
                
       #cv.ShowImage('gaugeROI ',gauge_ROI_gray)
       #cv.WaitKey(0)
       
        #RectROI=(pt1_RightLast[0],pt1_RightLast[1],ROI_size[0],ROI_size[1])
        #print "RectROI",RectROI
      
      #gauge_ROI_gray=cv.GetSubRect(ForeGroundImg_gray,RectROI)
        #cv.ShowImage('gaugeROI_cv.GetSubRect ',imgROI)
       # cv.WaitKey(0)
       
         #--------gauge ROI /----------------------------------
        
        gauge_ROI_color = cv.CreateImage(ROI_size, 8, 3)# 建立一个空的灰度图 
        cv.CvtColor(gauge_ROI_gray, gauge_ROI_color, cv.CV_GRAY2BGR)#转换 to Gray        
        
        return img_draw,gauge_ROI_color   ,pt1_collect,pt2_collect
    
    def calculate_defect_index_CMRR(self,ROI_Hist_list,TemplateSpace_Histogram_list,ROIimg_histtogram):
         #------CMRR--------
                                    ROI_Hist_list.sort()
                                    TemplateSpace_Histogram_list.sort()
                                    print "sum(ROI_Hist_list)=",sum(ROI_Hist_list)
                                    print "sum(TemplateSpace_Histogram_list)=",sum(TemplateSpace_Histogram_list)
                                    
                                    imgHist_ROIsort=FBG.drawImage_Histogram(ROIimg_histtogram,ROI_Hist_list,(0,0,255),False)     
                                   # cv.ShowImage( "imgHist(ROIsort)" ,  imgHist_ROIsort);
                                    #cv.WaitKey(1000);                                    
                                    imgHist_ROI_Template=FBG.drawImage_Histogram(imgHist_ROIsort,TemplateSpace_Histogram_list,(0,255,255),False)
                                   # cv.ShowImage( "imgHist(ROI & Template)" , imgHist_ROI_Template );
                                   # cv.WaitKey(1000);
                                  
                                    Differ_Hist_list=list()
                                    for i in range(256):
                                        #print "ROI_Hist_list,TemplateSpace_Histogram_list",ROI_Hist_list[i],TemplateSpace_Histogram_list[i]
                                        #Differ_Hist_list.append(   abs(ROI_Hist_list[i]-TemplateSpace_Histogram_list[i])**2/(256*256)  )
                                        Differ_Hist_list.append(   abs(ROI_Hist_list[i]-TemplateSpace_Histogram_list[i])  )
                                   
                                    #print  "Differ_Hist_list=",Differ_Hist_list
                                    print "#sum(Differ_Hist_list)=",sum(Differ_Hist_list)
                                    
                                    #Differ_Hist_list.sort()
                                    #imgHist_Differ_sort=FBG.drawNewImage_Histogram(Differ_Hist_list,(255,0,0),False )
                                    imgHist_ROI_Template_Differ_sort=FBG.drawImage_Histogram(imgHist_ROI_Template,Differ_Hist_list,(255,0,0),False )
                                                                      
                                    #cv.ShowImage( "imgHist_ROI_Template_Differ_sort" , imgHist_ROI_Template_Differ_sort );
                                   # cv.WaitKey(1000);
                                  
                                    H_max=max(Differ_Hist_list)
                                    H_min=1
                                    for m in range(256):
                                        if Differ_Hist_list[m]>1:
                                            H_min=Differ_Hist_list[m]
                                            break
                                    print"(H_max,H_min)=",(H_max,H_min)
                                    CMRR=int(100* (H_max-H_min)/(H_max+H_min))
                                    print "#CMRR= ",CMRR
                                    #cv.WaitKey(0);
                                    
                                    #-----------------------------
                                    DiffSumArea= 0#sum(Differ_Hist_list)
                                    TemplateSumArea=0
                                                                     
                                    for i in range(256):
                                        DiffSumArea=DiffSumArea+Differ_Hist_list[i]
                                        TemplateSumArea=TemplateSumArea+TemplateSpace_Histogram_list[i]
                                    
                                    DiffSumArea=DiffSumArea/TemplateSumArea  # To percent %
                                    DSAE=int(DiffSumArea*100)
                                    print"#DSAE= ",DSAE
                                    #ROIimg_histtogramTT=FBG.drawImage_Histogram(ROIimg_histtogram,ROI_Hist_list)
                                    #ROIimg_Differ_Hist=FBG.drawImage_Histogram(ROIimg_histtogram,Differ_Hist_list)
                                    #cv.ShowImage( "Display window: ROIimg_Differ_Hist " , ROIimg_Differ_Hist );
                                    #cv.WaitKey(4000);
                                    #------/CMRR/--------
                                    return CMRR,DSAE,imgHist_ROI_Template_Differ_sort
    
    
    #--------/JK add/---------
    
#----------------------------------------------

    
class Class4_alignment_output(Class0_image_table):
    ALIGNMENT=""
    detect_shape =""
    scaling_x =0.0
    scaling_y =0.0
    alignment_x =0.0
    alignment_y =0.0
    def initial(self,Cimg,Chilight,Coutput_ali):
                    Coutput_ali.ALIGNMENT=Cimg.IMAGE
                    # print "AAAA",Cimg.IMAGE
                    Coutput_ali.split_variation=Cimg.split_variation
                    Coutput_ali.pattern_series=Cimg.pattern_series
                    Coutput_ali.highlight_name=Cimg.highlight_name
                    Coutput_ali.process_condition=Cimg.process_condition
                    Coutput_ali.repeat_take=Cimg.repeat_take
                    # print Coutput_ali.repeat_take+"AA"
                                  
                    Coutput_ali.detect_shape="9" 
                    """
                    input Calculate parameter :scale_x scale_y alignment_x alignment_y
                    """
                    #print "(scale_X,Chilight.scale_X)=",(scale_X,Chilight.scale_x)
                    Coutput_ali.scaling_x=Chilight.scale_x
                    Coutput_ali.scaling_y=Chilight.scale_y
                    #Coutput_ali.alignment_x=(alignment_X)+Chilight.Bigoffset_x   #pixel
                    #Coutput_ali.alignment_y=(alignment_Y)+Chilight.Bigoffset_y    #pixel
                    Coutput_ali.alignment_x=Chilight.Smalloffset_x+Chilight.Bigoffset_x   #pixel
                    Coutput_ali.alignment_y=Chilight.Smalloffset_y+Chilight.Bigoffset_y    #pixel
                    return Coutput_ali
    
"""
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    def __iter__(self):
        return self
    def next(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]     
"""
class Class5_assessment_output(Class0_image_table,Class3_measure_gauge):
    ASSESSMENT=""  # - ASSESSMENT(GAUGE)   
    image_path=""
    inner_mean =0.0
    inner_variance =0.0
    outer_mean =0.0
    outer_variance =0.0
    defect_index =""
    
    
    
    def gauge_measuremet(self,Cmeasure,Cimg,Coutput_ass):
                           # Coutput_ass=Class5_assessment_output()                          
                            Coutput_ass.ASSESSMENT= Cmeasure.GAUGE
                            Coutput_ass.gauge_base_x= Cmeasure.gauge_base_x.__str__()
                            Coutput_ass.gauge_base_y= Cmeasure.gauge_base_y.__str__()
                            Coutput_ass.gauge_head_x= Cmeasure.gauge_head_x.__str__()
                            Coutput_ass.gauge_head_y= Cmeasure.gauge_head_y.__str__()
                            Coutput_ass.parent_highlight= Cmeasure.parent_highlight
                            Coutput_ass.gauge_tone= Cmeasure.gauge_tone
                            Coutput_ass.measure_mode= Cmeasure.measure_mode
                            Coutput_ass.measure_range= Cmeasure.measure_range
                            Coutput_ass.measure_number= Cmeasure.measure_number
                                  
                            Coutput_ass.image_path= Cimg.IMAGE
                            Coutput_ass.split_variation= Cimg.split_variation
                            Coutput_ass.pattern_series=Cimg.pattern_series
                            Coutput_ass.process_condition= Cimg.process_condition
                            Coutput_ass.repeat_take= Cimg.repeat_take
                            
                            """
                            Coutput_ass.inner_mean=  inner_mean
                            Coutput_ass.inner_variance=inner_variance
                            Coutput_ass.outer_mean=outer_mean
                            Coutput_ass.outer_variance=outer_variance
                            Coutput_ass.defect_index="none"
                            """       
                            line_output_ass= Coutput_ass.ASSESSMENT+"," +Coutput_ass.gauge_base_x+"," + Coutput_ass.gauge_base_y+","+ Coutput_ass.gauge_head_x+","+Coutput_ass.gauge_head_y+","+Coutput_ass.parent_highlight+","+Coutput_ass.gauge_tone+","+Coutput_ass.measure_mode+","+str(Coutput_ass.measure_range)+","+str(Coutput_ass.measure_number)+","\
                            +Coutput_ass.image_path+","+Coutput_ass.split_variation+","+Coutput_ass.pattern_series+","+Coutput_ass.process_condition+","+Coutput_ass.repeat_take+"," \
                            +str(Coutput_ass.inner_mean)+","+str(Coutput_ass.inner_variance)+","+str(Coutput_ass.outer_mean)+","+str(Coutput_ass.outer_variance)+","+str(Coutput_ass.defect_index)\
                            +"\n"
                            
                            return line_output_ass
#--------------------------------------------------------
class Class6_config:
 """
 config parameter ,could be added or removed  
 """
 POLYGON_TABLE=""#	./data/metro/cell_polygon.txt
 HIGHLIGHT_TABLE=""#	./data/metro/highlight_window.txt
 IMAGE_TABLE=""#	./data/metro/image_table.txt
 GAUGE_TABLE	=""#./data/metro/measure_gauge.txt
 IMAGE_MARGIN=	10
 ALIGNMENT_RANGE=	10 #nm
    #SCALING_RANGE=	0.1
 GAUGE_EXTENSION=	0 # nm 
 INNER_CD_FACTOR=	0.3 # for gauge 
 OUTER_CD_FACTOR=	0.4
 ASSESSMENT_TABLE=""#	./output/sample_assessment_output.txt
 ALIGNMENT_TABLE=""#	./output/sample_alignment_output.txt 
 TEMPLATE_POLYGON_TABLE="" #./template_polygon
 TEMPLATE_SPACE_TABLE=""  #./template_space
 
 
 #---JKadd--------
 gaugeLine_spaceGain=1.0    
 thin_times=9
 def initial(self,line_array,Cconfig):
        
        if line_array[0].__contains__("POLYGON_TABLE"):Cconfig.POLYGON_TABLE=line_array[1]
        if line_array[0].__contains__("HIGHLIGHT_TABLE"):Cconfig.HIGHLIGHT_TABLE=line_array[1]
        if line_array[0].__contains__("IMAGE_TABLE"):Cconfig.IMAGE_TABLE=line_array[1]
        if line_array[0].__contains__("GAUGE_TABLE"):Cconfig.GAUGE_TABLE=line_array[1]
        if line_array[0].__contains__("IMAGE_MARGIN"):Cconfig.IMAGE_MARGIN=line_array[1]
        if line_array[0].__contains__("ALIGNMENT_RANGE"):Cconfig.ALIGNMENT_RANGE=line_array[1]
       # if line_array[0].__contains__("SCALING_RANGE"):Cconfig.=line_array[1]
        if line_array[0].__contains__("GAUGE_EXTENSION"):Cconfig.GAUGE_EXTENSION=line_array[1]
        if line_array[0].__contains__("INNER_CD_FACTOR"):Cconfig.INNER_CD_FACTOR=line_array[1]
        if line_array[0].__contains__("OUTER_CD_FACTOR"):Cconfig.OUTER_CD_FACTOR=line_array[1]
        if line_array[0].__contains__("ASSESSMENT_TABLE"):Cconfig.ASSESSMENT_TABLE=line_array[1]
        if line_array[0].__contains__("ALIGNMENT_TABLE"):Cconfig.ALIGNMENT_TABLE=line_array[1]
        if line_array[0].__contains__("TEMPLATE_TABLE_POLYGON"):Cconfig.TEMPLATE_POLYGON_TABLE=line_array[1]
        if line_array[0].__contains__("TEMPLATE_TABLE_SPACE"):Cconfig.TEMPLATE_SPACE_TABLE=line_array[1]
                
        return Cconfig
    
    
    
    
#=========================================================
def LoadToShowImg(img_name_path):        
    # img_name = "c:\\AG3_CD65_P150_T06O.png"
    # img_name = "c:\\people_small.jpg"  
    img = cv.LoadImage(img_name_path) 
    image_size = cv.GetSize(img)#获取原始图像尺寸  
    grayscale = cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图  
    cv.CvtColor(img, grayscale, cv.CV_BGR2GRAY)#转换 to Gray
    cv.ShowImage( "Display window: gray", grayscale );
    
#------------------------------------------------     
def PutText_InImage(image,cinText,startPoint,BGRcolor):
     #----write Text in image--------
        font=cv.InitFont( CV_FONT_HERSHEY_PLAIN,1.0, 1.0,0, 1, CV_AA);         
        cv.PutText(image, cinText, startPoint,font, BGRcolor )       
    #----/write Text in image/--------
def openFiles(filepath_image,filepath_highlight,filepath_polygon,filepath_measure):
    fp_image = open(filepath_image, "r")
      #讀檔fp.readlines() #把整個檔案以一行一行形式讀入list
    Lines_image=fp_image.readlines() # skip first row
    print "fileLines_image=",Lines_image.__len__()-1
    fp_image.close()  
   #B.
    fp_highlight = open(filepath_highlight, "r")
      #讀檔fp.readlines() #把整個檔案以一行一行形式讀入list
    Lines_highlight=fp_highlight.readlines() # skip first row
    print "fileLines_highlight=",Lines_highlight.__len__()-1   
    #C.
    fp_polygon = open(filepath_polygon, "r")
      #讀檔fp.readlines() #把整個檔案以一行一行形式讀入list
    Lines_polygon=fp_polygon.readlines() # skip first row
    print "fileLines_polygon=",Lines_polygon.__len__()-1   
       #D.
    fp_measure = open(filepath_measure, "r")
      #讀檔fp.readlines() #把整個檔案以一行一行形式讀入list
    Lines_measure=fp_measure.readlines() # skip first row
    print "fileLines_measure=",Lines_measure.__len__()-1
        
    return  Lines_image,Lines_highlight, Lines_polygon,Lines_measure
