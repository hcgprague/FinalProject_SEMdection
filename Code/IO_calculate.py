# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 10:11:10 2012

@author: jqhuang
"""
from __future__ import division  # 使用float 除法

import sys,os
import cv2.cv as cv
#os.chdir('C:\Python27\lib\site-packages\xy') #指定目前資料夾路徑
#import highgui 
from cv import * 
from PIL import Image, ImageDraw


#----------------------------------------------

def collect_gaugeLines(ForeGround_colorImg,pt1_base_gauge,pt2_head_gauge,N_lines):
    
                            #----------calculate gauge--------------
                           # pt_N=len(pt1_base_gauge) # =len( pt2_head_gauge)
                            pt_N=N_lines
                           # print pt_N
                            gaugeline_list=list() # how many gaugeline sets
                            #pt_N=1 # for test only one time
                            
                            image_size= cv.GetSize(ForeGround_colorImg)
                            foreground_gray=cv.CreateImage(image_size, 8, 1)# 建立一个空的灰度图      
                            cv.CvtColor(ForeGround_colorImg, foreground_gray, cv.CV_BGR2GRAY)#转换 to Gray 
                        
                            for p in range(pt_N): # for every line of a gauge
                                gaugeline_array=list() #data array in a gaugeline
                           
                               #p=(pt1_base_gauge[i],pt2_head_gauge[i])
                               # print "baseP,headP",pt1_base_gauge[p],pt2_head_gauge[p],Cmeasure.gauge_tone
                                base_x= pt1_base_gauge[p][0]
                                base_y= pt1_base_gauge[p][1]
                                head_x= pt2_head_gauge[p][0]
                                head_y= pt2_head_gauge[p][1]
                              #  print "base_x,base_y=", base_x ,base_y
                              #  print "head_x,head_y=", head_x ,head_y
                              #  print "base_y,head_y",base_y,head_y
                                
                                #--------collect gaugelineArray-----------------
                                if base_y==head_y :head_y=base_y+1
                                if base_x==head_x :head_x=base_x+1
                                for jj in range ( base_y , head_y ): # y
                                    #    print "base_x,head_x",base_x,head_x
                                    #    print "A"    
                                    for ii in range ( base_x,head_x ):# x                
                                        if jj<image_size[1] and ii<image_size[0] :                                                                      
                                            v=int( foreground_gray[jj,ii]) #(y,x)
                                            #print  i,j
                                            gaugeline_array.append(v)
                                #--------/collect gaugelineArray/-----------------
                                #print gaugeline_array
                                gaugeline_list.append(gaugeline_array)
                                
                                
                            return gaugeline_list
#-------------------------------------------------

def measure_gaugelines_InnerMean(gaugeline_list,INNER_CD_FACTOR,OUTTER_CD_FACTOR):
                           # print "gaugeline_list=", gaugeline_list
                            gaugeline_innerlength_list=list()
                            gaugeline_peaklength_list=list()
                            gaugeline_outterlength_list=list()
                            #--------every gaugeline measure for inner and outter in Polygon---------------
                            for dataline in gaugeline_list:
                                #print len(dataline)
                                #print "dataline=",dataline
    
                                half=int(len(dataline)/2)
                                left_max=0
                                left_max_index=0
                                for a in range(  half ): 
                                    if dataline[a]>=left_max:
                                        left_max=dataline[a]
                                        left_max_index=a
                                #print "left_max_index, left_max=", left_max_index, left_max
                                
                                
                                
                                
                                right_max=0
                                right_max_index=0
                                for b in range(  half,len(dataline) ): 
                                    if dataline[b]>=right_max:
                                        right_max=dataline[b]
                                        right_max_index=b
                              #  print "right_max_index, right_max=", right_max_index, right_max
                                
                               # inner_count=0
                                peak_avg=(left_max+right_max)/2 
                                """
                                print "left_max_index, left_maxValue=", left_max_index, left_max
                                print "right_max_index, right_maxValue =", right_max_index, right_max
                                """    
                                peak_length= right_max_index-left_max_index
                                gaugeline_peaklength_list.append(peak_length)
                               
                               
                               #-------  threshold--------------
                                #print Cconfig.INNER_CD_FACTOR
                                inner_threshold=float(peak_avg)*INNER_CD_FACTOR
#                                print "inner_threshold=",inner_threshold
                                outter_threshold=float(peak_avg)*OUTTER_CD_FACTOR
                               # print "outter_threshold=",outter_threshold
                                #-------/ threshold/--------------
                                
                                                                
                                
                               
                                #-----------inner_measure---------------------- 
                                inner_left_index=left_max_index
                                inner_right_index=right_max_index
                                for c_left in range(left_max_index,right_max_index):
                                    if dataline[c_left]<inner_threshold: # scan--> first low value
#                                       print dataline[c_left],c_left
 #                                      inner_count=inner_count+1
                                        inner_left_index=c_left
                                        break
                                #print  "inner_count=", inner_count
                               # print  "inner_left_index=",inner_left_index
                                for c in range( inner_left_index, inner_right_index):
                                    c_right=inner_right_index-(c-inner_left_index)  
                                    if dataline[c_right]<inner_threshold:  # scan<-- first low value
                                        inner_right_index=c_right
                                        break
                                    
                                this_inner_length=inner_right_index-inner_left_index
                                #print "(inner_left_index,inner_right_index)=",inner_left_index,inner_right_index
                                #--------/every gaugeline measure for inner and outter in Polygon/---------------
                            
                                gaugeline_innerlength_list.append(this_inner_length)                                
#                                print "# this_inner_length=",this_inner_length

                                """
                                print "dataline=",dataline                                
                                print "left_max_index, left_max=", left_max_index, left_max
                                print "right_max_index, right_max=", right_max_index, right_max
                                print "inner_threshold=",inner_threshold
                                print "(inner_left_index,inner_right_index)=",inner_left_index,inner_right_index
                                print "# this_inner_length=",this_inner_length
                                """
                                #-----------/inner_measure/---------------------- 
                           
                           
                           
                                #-----------outter_measure----------------------
                                outter_left_index=0
                                outter_right_index=len(dataline)
                             #   print "left_max_index, left_maxValue=", left_max_index, left_max
                                for d_left in range(0,left_max_index):
                                    if dataline[left_max_index-d_left+0]<outter_threshold: # scan--> first low value
                                       #print dataline[d_left],d
                                       #outter_count=outterer_count+1
                                       outter_left_index=left_max_index-d_left+0
                                       break
                            #    print "outter_left_index=" ,outter_left_index    
                               # print dataline
                                
                                for d_right in range(right_max_index,len(dataline)):
                                    if dataline[d_right]<outter_threshold: # scan--> first low value
                                       #print dataline[d_left],d
                                       #outter_count=outterer_count+1
                                       outter_right_index=d_right
                                       break
                           #     print "right_max_index,right_max_value",right_max_index,right_max  
                           #     print "outter_right_index=" ,outter_right_index    
                          #      print dataline
                                
                                
                                outter_left_length=left_max_index-outter_left_index
                                outter_right_length=outter_right_index-right_max_index
                                
                           #     print outter_left_length
                           #     print outter_right_length
                                outter_all_length=outter_left_length+outter_right_length+  peak_length  
                                gaugeline_outterlength_list.append( outter_all_length)
                               #-----------/outter_measure/---------------------- 
                                
                           
                           
                          #  print ">>>> gaugeline_innerlength_list=", gaugeline_innerlength_list
                            #------MEAN-------------------
                            gaugeline_innerlength_MEAN=0
                            gaugeline_innerlength_MEAN=  sum(gaugeline_innerlength_list)/len(gaugeline_innerlength_list) #pixel
                          #  print     gaugeline_innerlength_MEAN     #float
                            Inner_Variance=var(gaugeline_innerlength_list) #'pixel
                            Inner_set=(gaugeline_innerlength_MEAN,Inner_Variance)
                          
                            gaugeline_peaklength_MEAN=  sum(gaugeline_peaklength_list)/len(gaugeline_peaklength_list)#pixel
                            Peak_Variance=var(gaugeline_peaklength_list) #'pixel
                            Peak_set=(gaugeline_peaklength_MEAN,Peak_Variance)
                            
                            
                            gaugeline_outterlength_MEAN=  sum(gaugeline_outterlength_list)/len(gaugeline_outterlength_list)#pixel
                          #  print "gaugeline_outterlength_list",gaugeline_outterlength_list                            
                            Outter_Variance=var(gaugeline_outterlength_list) #'pixel
                            Outter_set=(gaugeline_outterlength_MEAN,Outter_Variance)
                           # print Outter_set 
                          # #------/MEAN/-------------------
                            
                            
                            
                            return   Inner_set,Peak_set, Outter_set
#------------------------------

def measure_gaugelines_InnerMean_0808(gaugeline_list,INNER_CD_FACTOR,OUTTER_CD_FACTOR):
                           # print "gaugeline_list=", gaugeline_list
                            gaugeline_innerlength_list=list()
                            gaugeline_peaklength_list=list()
                            gaugeline_outterlength_list=list()
                            #--------every gaugeline measure for inner and outter in Polygon---------------
                            for dataline in gaugeline_list:
                                #print len(dataline)
                                #print "dataline=",dataline
                                dataline_list=list()
                                dataline_list_ini=list()
                                
                                full_N=int(len(dataline))
                                left_max=0
                                left_max_index=0
                                right_max=0
                                right_max_index=0
                                
                                for a in range(  full_N ): 
                                    dataline_list.append(dataline[a])
                                    dataline_list_ini.append(dataline[a])
                                dataline_list.sort()
                                peak1_value=dataline_list[full_N-1]
                                peak2_value=dataline_list[full_N-2]
                                peak1_index=dataline_list_ini.index(peak1_value)
                                peak2_index=dataline_list_ini.index(peak2_value)
                                
                                #-----find Feature---------
                                """
                                if peak1_value <200 :
                                    Inner_set=(0,0)
                                    Peak_set=(0,0) 
                                    Outter_set=(0,0)
                                    return Inner_set,Peak_set, Outter_set
                               
                                if peak2_value <200:
                                    Inner_set=(0,0)
                                    Peak_set=(0,0) 
                                    Outter_set=(0,0)
                                    return Inner_set,Peak_set, Outter_set
                                """
                              #-----/find Feature/--------
                                
                                #print "left_max_index, left_max=", left_max_index, left_max
                                if peak1_index<peak2_index:
                                    left_max=peak1_value
                                    left_max_index=peak1_index
                                    right_max=peak2_value
                                    right_max_index=peak2_index
                                else:
                                    left_max=peak2_value
                                    left_max_index=peak2_index
                                    right_max=peak1_value
                                    right_max_index=peak1_index
                                
                              #  print "dataline_list_ini=",dataline_list_ini
                              #  print "left_max_index, left_maxValue=", left_max_index, left_max
                              #  print "right_max_index, right_maxValue =", right_max_index, right_max
                                
                                peak1_Leftdata_list=list()
                                peak1_Rightdata_list=list()
                                ppLimit_range=10 #peak1> Left scan
                                if  abs(left_max_index-right_max_index)<ppLimit_range:
                                    for i in range(0,left_max_index-ppLimit_range):
                                        peak1_Leftdata_list.append(dataline_list_ini[i])
                                    for i in range(left_max_index+ppLimit_range,full_N):
                                        peak1_Rightdata_list.append(dataline_list_ini[i])
                                
                                peak1_Leftdata_list.append(0)
                                peak1_Rightdata_list.append(0)
                                peak1_Leftdata_list_max=max(peak1_Leftdata_list)
                                peak1_Rightdata_list_max=max(peak1_Rightdata_list)
                                
                               # print "peak1_Rightdata_list",peak1_Rightdata_list
                              #  print "peak1_Rightdata_list_max",peak1_Rightdata_list_max
                              #  print "peak1_Leftdata_list",peak1_Leftdata_list
                               # print "peak1_Leftdata_list_max",peak1_Leftdata_list_max
                               # cv.WaitKey(0);                         
                                if peak1_Rightdata_list_max>peak1_Leftdata_list_max:
                                    right_max=peak1_Rightdata_list_max
                                    peak2_value=right_max
                                if peak1_Rightdata_list_max<peak1_Leftdata_list_max:
                                    right_max=peak1_Leftdata_list_max
                                    peak2_value=right_max

                                peak2_index=dataline_list_ini.index(peak2_value)                         
                                
                                if peak1_index<peak2_index:
                                    left_max=peak1_value
                                    left_max_index=peak1_index
                                    right_max=peak2_value
                                    right_max_index=peak2_index
                                else:
                                    left_max=peak2_value
                                    left_max_index=peak2_index
                                    right_max=peak1_value
                                    right_max_index=peak1_index                         
                               # print "(p1,p2) amp=" ,(peak1_value,peak2_value)
                               # print "(p1,p2) index=" ,(peak1_index,peak2_index)
                                                         
                                """                         
                                print "dataline_list_ini=",dataline_list_ini
                                print "left_max_index, left_maxValue=", left_max_index, left_max
                                print "right_max_index, right_maxValue =", right_max_index, right_max
                                """ 
                               # cv.WaitKey(0);                                   
                                 
                                #----------------
                                peak_avg=(left_max+right_max)/2 
                                peak_length= right_max_index-left_max_index
                                gaugeline_peaklength_list.append(peak_length)
                               
                               
                               #-------  threshold--------------
                                #print Cconfig.INNER_CD_FACTOR
                                inner_threshold=float(peak_avg)*INNER_CD_FACTOR
#                                print "inner_threshold=",inner_threshold
                                outter_threshold=float(peak_avg)*OUTTER_CD_FACTOR
                               # print "outter_threshold=",outter_threshold
                                #-------/ threshold/--------------
                                
                                                                
                                
                               
                                #-----------inner_measure---------------------- 
                                inner_left_index=left_max_index
                                inner_right_index=right_max_index
                                for c_left in range(left_max_index,right_max_index):
                                    if dataline[c_left]<inner_threshold: # scan--> first low value
#                                       print dataline[c_left],c_left
 #                                      inner_count=inner_count+1
                                        inner_left_index=c_left
                                        break
                                #print  "inner_count=", inner_count
                               # print  "inner_left_index=",inner_left_index
                                for c in range( inner_left_index, inner_right_index):
                                    c_right=inner_right_index-(c-inner_left_index)  
                                    if dataline[c_right]<inner_threshold:  # scan<-- first low value
                                        inner_right_index=c_right
                                        break
                                    
                                this_inner_length=inner_right_index-inner_left_index
                                #print "(inner_left_index,inner_right_index)=",inner_left_index,inner_right_index
                                #--------/every gaugeline measure for inner and outter in Polygon/---------------
                            
                                gaugeline_innerlength_list.append(this_inner_length)                                
#                                print "# this_inner_length=",this_inner_length

                                """
                                print "dataline=",dataline                                
                                print "left_max_index, left_max=", left_max_index, left_max
                                print "right_max_index, right_max=", right_max_index, right_max
                                print "inner_threshold=",inner_threshold
                                print "(inner_left_index,inner_right_index)=",inner_left_index,inner_right_index
                                print "# this_inner_length=",this_inner_length
                                """
                                #-----------/inner_measure/---------------------- 
                           
                           
                           
                                #-----------outter_measure----------------------
                                outter_left_index=0
                                outter_right_index=len(dataline)
                             #   print "left_max_index, left_maxValue=", left_max_index, left_max
                                for d_left in range(0,left_max_index):
                                    if dataline[left_max_index-d_left+0]<outter_threshold: # scan--> first low value
                                       #print dataline[d_left],d
                                       #outter_count=outterer_count+1
                                       outter_left_index=left_max_index-d_left+0
                                       break
                            #    print "outter_left_index=" ,outter_left_index    
                               # print dataline
                                
                                for d_right in range(right_max_index,len(dataline)):
                                    if dataline[d_right]<outter_threshold: # scan--> first low value
                                       #print dataline[d_left],d
                                       #outter_count=outterer_count+1
                                       outter_right_index=d_right
                                       break
                           #     print "right_max_index,right_max_value",right_max_index,right_max  
                           #     print "outter_right_index=" ,outter_right_index    
                          #      print dataline
                                
                                
                                outter_left_length=left_max_index-outter_left_index
                                outter_right_length=outter_right_index-right_max_index
                                
                           #     print outter_left_length
                           #     print outter_right_length
                                outter_all_length=outter_left_length+outter_right_length+  peak_length  
                                gaugeline_outterlength_list.append( outter_all_length)
                               #-----------/outter_measure/---------------------- 
                                
                           
                           
                          #  print ">>>> gaugeline_innerlength_list=", gaugeline_innerlength_list
                            #------MEAN-------------------
                            gaugeline_innerlength_MEAN=0
                            gaugeline_innerlength_MEAN=  sum(gaugeline_innerlength_list)/len(gaugeline_innerlength_list) #pixel
                          #  print     gaugeline_innerlength_MEAN     #float
                            Inner_Variance=var(gaugeline_innerlength_list) #'pixel
                            Inner_set=(gaugeline_innerlength_MEAN,Inner_Variance)
                          
                            gaugeline_peaklength_MEAN=  sum(gaugeline_peaklength_list)/len(gaugeline_peaklength_list)#pixel
                            Peak_Variance=var(gaugeline_peaklength_list) #'pixel
                            Peak_set=(int(gaugeline_peaklength_MEAN),Peak_Variance)
                            
                            
                            gaugeline_outterlength_MEAN=  sum(gaugeline_outterlength_list)/len(gaugeline_outterlength_list)#pixel
                          #  print "gaugeline_outterlength_list",gaugeline_outterlength_list                            
                            Outter_Variance=var(gaugeline_outterlength_list) #'pixel
                            Outter_set=(gaugeline_outterlength_MEAN,Outter_Variance)
                           # print Outter_set 
                          # #------/MEAN/-------------------
                            
                            
                            
                            return   Inner_set,Peak_set, Outter_set



#-----------------------------------------------
def var(dataArray):
    N_all=len(dataArray)
    mean= sum(dataArray)/N_all
    var_sum=0.0    
    for i in range(N_all):
       var_sum= var_sum+(dataArray[i]-mean)**2
    var_sqrt= (var_sum/N_all)**0.5
    return var_sqrt 
    
    


#------------------------------    
def Choose_MinErrorsum_Offset(offset_collect_x,offset_collect_y):
    
    #--------Create array--------------------    
    n=len(offset_collect_x) # n =len(offset_collect_y)   
    #  print n
    #-------special case----------    
    if n==1:
        pt_offset=(offset_collect_x,offset_collect_y)
        return pt_offsex
    #-------/special case/--------   
  
    err_sum_x=list() 
    err_sum_y=list() 
        
    for i in range(n) :   
        err_sum_x.append(0)
        err_sum_y.append(0)
    
    #--------/Create array/---------------------        
 

    best_offset_x=0
    best_offset_y=0
    minErr_index_x=0
    minErr_index_y=0
    
    for i in range(n):
        for j in range(n):
            err_sum_x[i]=err_sum_x[i]+  abs(offset_collect_x[j]- offset_collect_x[i])**2
            err_sum_y[i]=err_sum_y[i]+  abs(offset_collect_y[j]- offset_collect_y[i])**2
        if i>0 and (err_sum_x[i]< err_sum_x[minErr_index_x]) :
            minErr_index_x=i
        if i>0 and (err_sum_y[i]< err_sum_y[minErr_index_y]) :
            minErr_index_y=i

    best_offset_x=offset_collect_x[minErr_index_x]
    best_offset_y=offset_collect_y[minErr_index_y]
    pt_bestoffset=(best_offset_x,best_offset_y)
    """
    print "err_sum_x", err_sum_x 
    print "err_sum_y", err_sum_y 
   # print "best_offset(x,y)", pt_bestoffset
    """
    
    return pt_bestoffset
    



#------------------------------    
def Choose_average_Offset(offset_collect_x,offset_collect_y):
    
    n=len(offset_collect_x) # n =len(offset_collect_y)   
    #  print n
    #-------special case----------    
    if n==1:
        pt_offset=(offset_collect_x,offset_collect_y)
        return pt_offsex
    #-------/special case/--------   
  
    sum_x=0 
    sum_y=0  
    for i in range(n):
        sum_x=sum_x+offset_collect_x[i]
        sum_y=sum_y+offset_collect_y[i]
    avg_offset_x=int( sum_x/n)
    avg_offset_y=int(sum_y/n)
    
    pt_avg_offset=(avg_offset_x,avg_offset_y)    
   # print "avg_offset(x,y)", pt_avg_offset    
    
    return pt_avg_offset        
   



"""
#------------------------------    
def Choose_RMS_Offset(offset_collect_x,offset_collect_y):
    
    n=len(offset_collect_x) # n =len(offset_collect_y)   
    #  print n
    #-------special case----------    
    if n==1:
        pt_offset=(offset_collect_x,offset_collect_y)
        return pt_offsex
    #-------/special case/--------   
  
    sum_x=0 
    sum_y=0  
    for i in range(n):
        sum_x=sum_x+ offset_collect_x[i]**2
        sum_y=sum_y+offset_collect_y[i]**2
    RMS_offset_x=int( (sum_x**0.5)/n)
    RMS_offset_y=int((sum_y**0.5)/n)
    
    pt_RMS_offset=(RMS_offset_x,RMS_offset_y)    
   # print "avg_offset(x,y)", pt_avg_offset    
    
    return pt_RMS_offset        
        
"""

     
#----------------main------------------------------
#----------------main------------------------------

if __name__ == "__main__":
    print "A"