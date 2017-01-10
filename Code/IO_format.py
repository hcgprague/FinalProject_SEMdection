# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 15:31:51 2012

@author: jqhuang
"""
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
#from  IO_DataStructure  import Class0_image_table,Class1_highlight_window,Class2_cell_polygon, Class3_measure_gauge, Class4_alignment_output
#from  IO_DataStructure  import  Class5_assessment_output, Class6_config
from  IO_DataStructure  import * 
import thread, time
"""
def IPL_show_gif(img_name):
    # IML
    im = Image.open(img_name)
    image = im.convert("L")
    image.load()
    image.show()
"""          
    
#---------main-----------------------------------
#---------main-------------------------------

#if __name__ == "__main__":
     
def mainT(  isopen_bigoffse):   

    #-----------------------------
    
   # isopen_bigoffset=False
  #  isopen_bigoffset=True
    
    Cconfig=Class6_config()
    fp_config = open("data/metro/main_config.txt", "r")
    #讀檔fp.readlines() #把整個檔案以一行一行形式讀入list
    Lines_config=fp_config.readlines() # skip first row
    #print "fileLines_config=",Lines_config.__len__()-1
    fp_config.close() 
    
    for line in Lines_config:
        line_array=line.split("\t")
     #   print line_array
        if len(line_array)>1:
            line_array[1]=line_array[1].replace("\n","")
            Cconfig=Cconfig.initial(line_array,Cconfig)
         
       
    #print "Cconfig.POLYGON_TABLE=",Cconfig.POLYGON_TABLE
    #print "Cconfig.ALIGNMENT_TABLE=",Cconfig.ALIGNMENT_TABLE    
    
    filepath_polygon=  Cconfig.POLYGON_TABLE #'data/metro/cell_polygon.txt'
    filepath_highlight=Cconfig.HIGHLIGHT_TABLE    #'data/metro/highlight_window.txt'
    filepath_image=Cconfig.IMAGE_TABLE#'data/metro/image_table.txt'
    filepath_measure=Cconfig.GAUGE_TABLE#'data/metro/measure_gauge.txt'
    filepath_output_alignment=Cconfig.ALIGNMENT_TABLE
    filepath_output_assessment=Cconfig.ASSESSMENT_TABLE
    
    #fp_out_ali = open('IOformat_output_alignment.csv','w') #開啟檔案,w沒有該檔案就新增    
    #fp_out_ass = open('IOformat_output_assessment.csv','w') #開啟檔案,w沒有該檔案就新增    
    fp_out_ali = open(filepath_output_alignment,'w') #開啟檔案,w沒有該檔案就新增    
    fp_out_ass = open( filepath_output_assessment,'w') #開啟檔案,w沒有該檔案就新增    
      
    line_column_ali= "ALIGNMENT"+","+"split_variation"+","+"pattern_series"+","+"highlight_name"+","+"process_condition"+","+"repeat_take"+","+"detect_shape"+","+ "scaling_x"+","+ "scaling_y"+","+ "alignment_x"+","+"alignment_y"+"\n"
    line_column_ass= "ACCESSMENT,base_x,base_y,head_x,head_y,parent_highlight,gauge_tone,measure_mode,measure_range,measure_number,image_path,split_variation,pattern_series,process_condition,repeat_take,inner_mean,inner_variance,outer_mean,outer_variance,defect_index,peak_mean,peak_var,CSA"+"\n"
    fp_out_ali.writelines(line_column_ali)                     
    fp_out_ass.writelines(line_column_ass)                     
    ntimes=0
    #C1=Class0_image_table()
    #C1.IMAGE="A"
    #C4=Class3_measure_gauge()
    #C4.IMAGE="AA"    
    #print "C4",C4.IMAGE
    
    #------test how many total items-------------------------------------    
    #A.  
    Lines_image,Lines_highlight, Lines_polygon,Lines_measure=openFiles(filepath_image,filepath_highlight,filepath_polygon,filepath_measure)
    
   #------/test how many total items/-------------------------------------    
    
    
    
  #------------- Template_img  search Prepare -----------------
    #template_polygon_path=Cconfig.TEMPLATE_POLYGON_TABLE
    print "Cconfig.TEMPLATE_POLYGON_TABLE=",Cconfig.TEMPLATE_POLYGON_TABLE
   # fp_template_polygon = open(Cconfig.TEMPLATE_POLYGON_TABLE, "r")
   # Lines_template_polygon=fp_template_polygon.readlines() # skip first row

    fp_template_space = open(Cconfig.TEMPLATE_SPACE_TABLE , "r")
    Lines_template_space=fp_template_space.readlines() # skip first row
    print Lines_template_space
    TemplateSpace_Histogram_list=list()
    TemplatePolygon_Histogram_list=list()   
    TemplateSpace_Histogram_list_Collection=list()
 
    Img_avgTemplate_Histogram=FBG.drawNewImage_Histogram( TemplateSpace_Histogram_list,(255,255,255),True)

    count_N=0    
    for line in Lines_template_space:
        count_N=count_N+1
        file_path=line.replace("\n","")
       # print file_path
        img_templateSpace = cv.LoadImage(file_path) 
        #image_size = cv.GetSize(img_templateSpace)#获取原始图像尺寸  
        img_TemplateSpace_Histogram,TemplateSpace_Histogram_list=FBG.getImage_Histogram(img_templateSpace,(0,0,255),True )           
        Img_avgTemplate_Histogram=FBG.drawImage_Histogram(Img_avgTemplate_Histogram,TemplateSpace_Histogram_list,(0,count_N*30,0),False)
       # print "TemplateSpace_Histogram_list=",TemplateSpace_Histogram_list  
        PutText_InImage(img_TemplateSpace_Histogram,"space Template"+str(count_N),(50,50),(255,255,255))       
        cv.ShowImage( "img_TemplateSpace_Histogram", img_TemplateSpace_Histogram );
        cv.WaitKey(1000)
        cv.ShowImage( "img_avgTemplateSpace_Histogram", Img_avgTemplate_Histogram);
        cv.WaitKey(1000)
        
        TemplateSpace_Histogram_list_Collection.append(TemplateSpace_Histogram_list)
    print"#eTemplateSpace_Nsets=",len(TemplateSpace_Histogram_list_Collection)
    TemplateSpace_Nsets=len(TemplateSpace_Histogram_list_Collection)
    
    Bin_sum_list=list()
    for b in range(256):            
        Bin_sum_list.append(0)    
    for b in range(256):
        #print"-------------",b            
        for s in range(  TemplateSpace_Nsets ): # N set imageTemplate
            Bin_sum_list[b]=Bin_sum_list[b]+TemplateSpace_Histogram_list_Collection[s][b]
           # Bin_sum_list[b]=TemplateSpace_Histogram_list_Collection[s][b]
                        
            #print  Bin_sum_list[b]
        Bin_avg=(Bin_sum_list[b]/ TemplateSpace_Nsets)
        TemplateSpace_Histogram_list[b]=Bin_avg
        #print "avg=",  Bin_avg
       
            
    #print"#TemplateSpace_avgHistogram_list=",TemplateSpace_Histogram_list
    Img_avgTemplate_Histogram=FBG.drawImage_Histogram(Img_avgTemplate_Histogram, TemplateSpace_Histogram_list,(255,255,255),False)
    PutText_InImage(Img_avgTemplate_Histogram,"Avg:Mix SpaceTemplate of "+str(count_N),(10,200),(0,255,255))       
            
    cv.ShowImage( "img_TemplateSpace_Histogram", Img_avgTemplate_Histogram );
    cv.SaveImage( file_path.replace(".png","_Mixed.png"), Img_avgTemplate_Histogram );
    cv.WaitKey(3000)  
      #------------- /Template_img  search Prepare/ -----------------
    #print "AAAAAAA"
    """ 
    # Template_img  search Prepare 
    for lineA in Lines_image: #stage A
        Cimg= Class0_image_table()
        line_array = lineA.split("\t")
        Cimg.IMAGE=line_array[0]
        Cimg.pattern_series=line_array[1]
        Cimg.split_variation=line_array[2]
        Cimg.highlight_name=line_array[3] #AL3_CD65_P200  AK3_CD65_P190
      #  print     Cimg.highlight_name
        Cimg.process_condition=line_array[4]
        Cimg.repeat_take=line_array[5].replace("\n","")
        Cimg.defect_index=line_array[6].replace("\n","")
        if Cimg.defect_index=="0":
           Template_img.append (lineA)
    #print "Template_img=", Template_img
    #print "Lines_img=", Lines_image
    
    #----------make Template image insert to the First------2012.0813
    for i in range(len(Template_img)):
        Lines_image.insert(1,Template_img[i])
    #print "LinesT_imgO=", Lines_image
    #----------/make Template image insert to the First/------
    """
    
    
    
    # ALL Image Process Start  
    #---------search stage of all items-----------------  
    for lineA in Lines_image: #stage A
        
        Cimg= Class0_image_table()
        line_array = lineA.split("\t")
        Cimg=Cimg.initial(line_array,Cimg)

        
        if    (not Cimg.IMAGE.__contains__("IMAGE")):
            print  Cimg.IMAGE
           # countA=countA+1
            #testlineA=Cimg.IMAGE+","+Cimg.pattern_series+","+Cimg.split_variation+","+Cimg.highlight_name+","+Cimg.process_condition+","+Cimg.repeat_take
            #print          testlineA
            """
            forground and background
            """
           #-----forground and background ---------
            img_name=Cimg.IMAGE.replace("gif","png")
            print img_name        
            img = cv.LoadImage(img_name) 
            image_size = cv.GetSize(img)#获取原始图像尺寸 
            imgsize_x=image_size[0]
            imgsize_y=image_size[1]
            print "imgsize_x=",imgsize_x
            print "imgsize_y=",imgsize_y
            
            #take binaryFBG_contour
            binaryFBG,otsu_threshold=FBG.GetBinaryImg_ForeBackGround(img,convert_dir=1 ,otsu_ntimes=3)         
            binaryFBG_contour=FBG.GetBinaryImg_ForeBackGround_contour(img,convert_dir=1,threshold_rst=otsu_threshold,thin_times=Cconfig.thin_times) 
            """            
            cv.ShowImage( "Display window: binaryFBG", binaryFBG )
            cv.WaitKey(1000);
            """
            #take ForeGround_colorImg
            ForeGround_colorImg=FBG.getForeground(img,binaryFBG,extract_direction=1) #extract    
            #-----show foreground-------
            #cv.ShowImage('Fore Ground to measure ForeGround_colorImg', ForeGround_colorImg)
            #cv.WaitKey(1000)
            #-----/show foreground/-------
            
           #-----/forground and background/ ---------
           
              
          
           #------------------------- main Feature contour Analyize---------------------------
          
           #--------------Find contour_img-----------------
            draw_img = cv.CreateImage(image_size, 8, 3) 
            cv.Zero(draw_img)
            contour_Num=3
            BestContour_Center=(0,0)
            binaryFBG_contour=FBG.cleanEdge_grayimage(binaryFBG_contour,clean_thick=40)
            if isopen_bigoffset==True:
                
                contour_img,contour_Num,BestContour_Center=FBG.get_ContourBest_LimitAda(draw_img ,binaryFBG_contour)
            
            print "CC>> Contour_countNum:", contour_Num 
            print "BestContour_Center:",BestContour_Center
                   
            
           # cv.ShowImage('Find contour_img',contour_img)
           #cv.SaveImage(  img_name.replace(".png","best_contour_MsssCenetr.png"),contour_img)
           # cv.WaitKey(0)
            
           #--------------/Find contour_img/-----------------
            
            
            
            #-------------PreCount polygon conuts-----------------  
            #print Lines_highlight        
            FilePreCount_polygonNumber=Cimg.PreCount_polygonNumber(Lines_highlight, Lines_polygon)
            print "CC>> FilePreCount_polygonNumber:", FilePreCount_polygonNumber 
            #  cv.ShowImage(  img_name,img)                    
            #  cv.WaitKey(0)
            #-------------/PreCount polygon conuts/----------------   
            
            
            #-----------Contour error count Warning Test-----------------        
            err_contour_Num= (contour_Num-FilePreCount_polygonNumber)   
            if abs(err_contour_Num) >int(FilePreCount_polygonNumber*0.7) :
                print "!!  err_contour_Num) > "+str(FilePreCount_polygonNumber*0.7)
                #cv.ShowImage('err contour_img',contour_img)
                filename=Cimg.getImgFileName(Cimg.IMAGE)
                filename=filename.replace(".png","_ContourCount_Warnning.png")
                cv.SaveImage("c:\\contour_countwarn\\" +filename ,contour_img )
                           
            #-----------/Contour error count Warning Test/-----------------        
          
          
            """
            #------------Save ALL contour_img--------------------       
            #pxy=str(BestContour_center[0])+"_"+str(BestContour_center[1])+"_"
            img_filename=Cimg.getImgFileName(Cimg.IMAGE)        
            #print "img_filename",img_filename  
            
            img_filename =img_filename.replace(".png","all_Best.png") 
            cv.SaveImage("c:\\contour_all\contour_"+img_filename,contour_img)
            #cv.SaveImage("c:\\contour_all\contour_CountPolygon_img"+str(countA)+".png",contour_img)     
            
            #------------Save ALL contour_img--------------------       
            """
            
            
           #------------------------ /main Feature contour Analyize/----------------------------------------
                
            for lineB in Lines_highlight: #stage B
                Chilight= Class1_highlight_window()
                line_array = lineB.split("\t")
                if not str(line_array[2]).__contains__("base"):  #number sureance   
                    Chilight.initial(line_array,Chilight)                
      
                  #  hilight_interval_x=   int(Chilight.highlight_head_x -Chilight.highlight_base_x ) 
                  #  print "scaleX:",scale_X 
                  #  print "scaleY:",scale_Y
                   # testlineB=Chilight.HIGHLIGHT+","+Chilight.highlight_base_x+","+Chilight.highlight_base_y+","+Chilight.highlight_head_x+","+Chilight.highlight_head_y+","+Chilight.pattern_series+","+Chilight.split_variation
                    
                
                        
                    if  Chilight.HIGHLIGHT.__contains__( Cimg.highlight_name):
                        #testlineB=Chilight.HIGHLIGHT            
                        highlight_Polygons=0
                        #print Cimg.highlight_name , Chilight.HIGHLIGHT
                        scale_X=  int(Chilight.highlight_head_x-Chilight.highlight_base_x)   / imgsize_x
                        scale_Y=  int(Chilight.highlight_head_y-Chilight.highlight_base_y)  /imgsize_y
                        Chilight.scale_x=scale_X
                        Chilight.scale_y=scale_Y
                        
                        #--------PreCount_polygonOffset----------
                        NearestPolygon_Center,NearestPolygon_Offset=Cimg.PreCount_polygonOffset(Cimg,Chilight,Cconfig,Lines_polygon,BestContour_Center)
                        print "##NearestPolygon_Center",NearestPolygon_Center#pixel
                        print "#NeatestPolygon_Offset",NearestPolygon_Offset #pixel
                        Chilight.Bigoffset_x=NearestPolygon_Offset[0]
                        Chilight.Bigoffset_y=NearestPolygon_Offset[1]
                        #--------/PreCount_polygonOffset/----------
                        print "Chilight.scale_x'" ,Chilight.scale_x 
                        print "Chilight.scale_y':" ,Chilight.scale_y
                        print "Chilight.Bigoffset_x=",Chilight.Bigoffset_x
                        print "Chilight.Bigoffset_y=",Chilight.Bigoffset_y
                      
                        offset_collect_x=list()
                        offset_collect_y=list()
                        img_drawAll_polygons=  cv.CreateImage(image_size, 8, 3)# 建立一个空的灰度图 
                     
                        for lineC1 in Lines_polygon: #stage C1
                            Cpolygon= Class2_cell_polygon()
                            line_array = lineC1.split("\t")
                            
                            if not str(line_array[2]).__contains__("base"):  #number sureance      
                                Cpolygon.initial(line_array,Cpolygon,Cconfig)
                        
                                # print    line_array[2]  
                                #print"#Cpolygon.error_range=", Cpolygon.error_range 
                                
                                if  Cpolygon.parent_highlight.__contains__( Chilight.HIGHLIGHT):
                                     #testlineC1=Cpolygon.POLYGON 
                                     #    print Chilight.HIGHLIGHT, Cpolygon.POLYGON
                                    # Cpolygon.error_range=0
                                    #------------draw_polygon --------------------------------                    
                                     dx_base=int(Cpolygon.polygon_base_x-Chilight.highlight_base_x-Cpolygon.error_range)
                                     dy_base=int(Cpolygon.polygon_base_y-Chilight.highlight_base_y)#+Cpolygon.error_range)
                                     dx_head=int(Cpolygon.polygon_head_x-Chilight.highlight_base_x+Cpolygon.error_range)
                                     dy_head=int(Cpolygon.polygon_head_y-Chilight.highlight_base_y)#+Cpolygon.error_range
                                    
                                     dx_center=(dx_head-dx_base)/2  #nm
                                     dy_center=(dy_head-dy_base)/2  #nm
                                     #print "Chilight.highlight_base_x",Chilight.highlight_base_x
                                     #print "Chilight.highlight_base_y",Chilight.highlight_base_y
                                    
                                     #print "Cpolygon.polygon_base_x",Cpolygon.polygon_base_x
                                     #print "Cpolygon.polygon_base_y",Cpolygon.polygon_base_y
                                     #print "Cpolygon.polygon_head_x",Cpolygon.polygon_head_x
                                     #print "Cpolygon.polygon_head_y",Cpolygon.polygon_head_y
                                     
                                     #----nm To pixels------------
                                     pt1=( int( (dx_base)/Chilight.scale_x),int( (dy_base/Chilight.scale_y)   )    )
                                     pt2=( int( (dx_head)/Chilight.scale_x),int( (dy_head/Chilight.scale_y)    )     ) 
                                    # print "pt1_base",pt1
                                    # print "pt2_head",pt2 
                                     #----/nm To pixels/------------
                           
                                    
                                    
                                     # before Big offset display
                                     draw_img=Cpolygon.draw_Polygon_rect(ForeGround_colorImg,pt1,pt2,(0,0,255))
                                     cv.ShowImage( "Display window:BigOffset_fix " , draw_img);
                                     cv.WaitKey(1000);
                                     
                                     #------Big offset fix----------------2012.0808
                                     pt1=list(pt1)
                                     pt2=list(pt2) 
                                     pt1[0]= pt1[0]- Chilight.Bigoffset_x
                                     pt2[0]= pt2[0]- Chilight.Bigoffset_x                                
                                     pt1[1]= pt1[1]- Chilight.Bigoffset_y
                                     pt2[1]= pt2[1]- Chilight.Bigoffset_y
                                     pt1_bigoffsetFix=(pt1[0],pt1[1])
                                     pt2_bigoffsetFix=(pt2[0],pt2[1]) 
                                     #reset polygon position  
                                     Cpolygon.polygon_base_x= pt1_bigoffsetFix[0]
                                     Cpolygon.polygon_base_y= pt1_bigoffsetFix[1]
                                     Cpolygon.polygon_head_x= pt1_bigoffsetFix[0]
                                     Cpolygon.polygon_head_y= pt1_bigoffsetFix[1]
                                     #------/Big offset fix/--------------
                                     
                                     # Afetr Big offset display
                                     draw_img=Cpolygon.draw_Polygon_rect(ForeGround_colorImg,pt1_bigoffsetFix,pt2_bigoffsetFix,(0,255,0))
                                     cv.ShowImage( "Display window:BigOffset_fix " , draw_img);
                                     cv.WaitKey(1000);
                                     
                                                   
                                     
                                                     
                                    #---------calculate polygon mm center-------
                                     dx_center_nmTopixel=int((pt1[0]+pt2[0])/2)
                                     dy_center_nmTopixel=int((pt1[1]+pt2[1])/2)
                                     pt_c = FBG.extract_Rect_binary(ForeGround_colorImg,pt1,pt2,img_drawAll_polygons)
                                    #    print "hilight_center_nmTopixel:",dx_center_nmTopixel ,dy_center_nmTopixel
                                    #    print "polygon_center=",pt_c[0],pt_c[1]
                                     offset_x=int(pt_c[0])-dx_center_nmTopixel
                                     offset_y=int(pt_c[1])-dy_center_nmTopixel
                                    #     print "=========================="
                                    #    print "offset =",offset_x , offset_y
                                     offset_collect_x.append(offset_x)                                    
                                     offset_collect_y.append(offset_y)                                                                        
                                     #---------/calculate polygon mm center/----
                                     
                            
                                    #------------/draw_polygon /-------------------------------
                       
                       #----choice best offset-----------------                    
                        print "@ End a hilight (for N polygon)"  
                        """
                        cv.SaveImage(  img_name.replace(".png","mc.png"),img_drawAll_polygons) # draw a hilight (polygons and MassCenters)
                        #  cv.ShowImage(  "all_mc.png",img_drawAll_polygons)                    
                        #  cv.WaitKey(0)
                        """ 
                        
                        print "offset_collect(x,y) =", offset_collect_x,offset_collect_y 
                        pt_offset_MinErrorsum=CAL.Choose_MinErrorsum_Offset(offset_collect_x,offset_collect_y)
                        pt_offset_avg=CAL.Choose_average_Offset(offset_collect_x,offset_collect_y)
                        alignment_X=pt_offset_MinErrorsum[0]
                        alignment_Y=pt_offset_MinErrorsum[1]
                        Chilight.Smalloffset_x=alignment_X   #2012.0815 add
                        Chilight.Smalloffset_y=alignment_Y   #2012.0815 add
                        print "pt_offset_MinErrorsum=",pt_offset_MinErrorsum
                        print "pt_offset_avg=",pt_offset_avg
                        print"Chilight.Smalloffset_x=",Chilight.Smalloffset_x
                        print"Chilight.Smalloffset_y=",Chilight.Smalloffset_y
                                          
                       # print "-------------------"    
                       # ntimes=0 #,another highlight set of polygons ,start                                        
                        fp_out_offset = open( "c:\offset.csv",'a') #開啟檔案,w沒有該檔案就新增
                        str_offset=str(pt_offset_MinErrorsum[0])+","+str(pt_offset_MinErrorsum[1])+","+str(pt_offset_avg[0])+","+str(pt_offset_avg[1])                   
                        fp_out_offset.writelines(str_offset+"\n")
                        fp_out_offset.flush() 
                        fp_out_offset.close()                    
                        #----/choice best offset/----------------
                   
                       
                       
                       
                        #------For every gauge in a Highlight----------------------------------
                        
                        #--------A.alignment of highlight,  output fileformat------
                        Coutput_ali=Class4_alignment_output()                          
                        # print testlineA, testlineB ,testlineC,testlineD                          
                        # testlineALL=testlineA+","+testlineB+","+testlineC+","+testlineD +"\n"                          
                        Coutput_ali=Coutput_ali.initial(Cimg,Chilight,Coutput_ali)                   
         
                             
                             
                        line_output_ali= Coutput_ali.ALIGNMENT+","+Coutput_ali.split_variation+","+Coutput_ali.pattern_series+","+Coutput_ali.highlight_name+","+Coutput_ali.process_condition+","+Coutput_ali.repeat_take+","+ str(Coutput_ali.detect_shape)+","+ str(Coutput_ali.scaling_x)+","+ str(Coutput_ali.scaling_y)+","+ str(Coutput_ali.alignment_x)+","+str( Coutput_ali.alignment_y)+"\n"
                        fp_out_ali.writelines( line_output_ali)
                        # print line_output_ali                     
                        # for item in list(Coutput):
                        # print line_output                              
                        #--------/-A.alignment of highlight, output fileformat/----------------
                        
                        
                        
                       
                        #---For every gauge process of a hilightlight :  B.assessment------------
                        for lineC2 in Lines_measure: #stage C2
                            Cmeasure= Class3_measure_gauge()
                            line_array = lineC2.split("\t")
                            if not str(line_array[1]).__contains__("base"):  #number sureance   
                                
                                Cmeasure.initial(line_array,Cconfig,Cmeasure)
                  
                               # print"Cmeasure.error_range", Cmeasure.error_range
                               # print "Cmeasure.measure_range",Cmeasure.measure_range
                               # print"Cmeasure.measure_number",Cmeasure.measure_number
                                if Cmeasure.parent_highlight.__contains__( Chilight.HIGHLIGHT):
                                   # print  Cmeasure.GAUGE+" in ",Chilight.HIGHLIGHT
                                    #testlineC2= Cmeasure.GAUGE   
                                    #Cmeasure.error_range=0
                        #-----------------------------draw_gauge in Polygon ------------------------- 
                                    #print "Cmeasure.gauge_base_x",Cmeasure.gauge_base_x
                                    #print "Chilight.highlight_base_x",Chilight.highlight_base_x
                                    #print "Cmeasure.gauge_head_x",Cmeasure.gauge_head_x
                                    #print "Chilight.highlight_head_x",Chilight.highlight_head_x
                                    
                                    dx_base=Cmeasure.gauge_base_x-Chilight.highlight_base_x # 'nm
                                    dy_base=Cmeasure.gauge_base_y-Chilight.highlight_base_y #'nm
                                    dx_head=Cmeasure.gauge_head_x-Chilight.highlight_base_x #'nm
                                    dy_head=Cmeasure.gauge_head_y-Chilight.highlight_base_y #'nm 
                                    
                                  #  print "dx_base",dx_base    
                                  #  print "dx_head",dx_head    
                                    
                                    print "Coutput_ali.alignment_x =",Coutput_ali.alignment_x 
                                    print "Coutput_ali.alignment_y =",Coutput_ali.alignment_y 
                                    """
                                    """
                                    #----do Adaptive extend gaugeLine of polygon by space----------
                                    gaugeLine_Distance= ((dx_head-dx_base)**2+(dy_head-dy_base)**2)**0.5
                                    gaugeLine_gain=( gaugeLine_Distance/90)
                                    #print "gaugeLine_Distance=",gaugeLine_Distance                           
                                    #print "Cmeasure.gauge_tone=",Cmeasure.gauge_tone    
                                    if Cmeasure.gauge_tone=="space":
                                        Cconfig.gaugeLine_spaceGain=gaugeLine_gain # JK add
                                        extend_x=gaugeLine_Distance*(Cconfig.gaugeLine_spaceGain-1.0)
                                        extend_x= extend_x*0.35
                                        dx_base= dx_base+ extend_x # avoid polygon edge
                                        dx_head= dx_head- extend_x # avoid polygon edge
                                        #print "s-gaugeLine_spaceGain=", Cconfig.gaugeLine_spaceGain
                                    if Cmeasure.gauge_tone=="polygon":
                                         extend_x=gaugeLine_Distance*(Cconfig.gaugeLine_spaceGain-1.0)
                                         extend_x= extend_x*0.8
                                         dx_base= dx_base-extend_x
                                         dx_head= dx_head+extend_x
                                         #print "p-gaugeLine_spaceGain=", Cconfig.gaugeLine_spaceGain
                                         #print "p-extend_x=",extend_x
                                         #print "p-dx_base,dx_head=",dx_base,dx_head
                                    #----/do Adaptive extend gaugeLine of polygon  by space/----------
                                    
                                     
                                    
                                    
                                    #---- nm To pixel-------
                                    pt1=( int( abs(dx_base)/Chilight.scale_x),int( (dy_base/Chilight.scale_y)   )   )
                                    pt2=( int( abs(dx_head)/Chilight.scale_x),int((dy_head/Chilight.scale_y)   )    ) 
                                    print "polygon range:" ,pt1,pt2
                                    pt1=list(pt1)
                                    pt2=list(pt2) 
                                  
                                    #---- /nm To pixel/-------
                                    
                                    
                                    
                                    #-----before offset-------------------                            
                                    img_drawLine,imgcolor_gaugeROI ,pt1_base_gauge,pt2_head_gauge=Cmeasure.draw_gaugeLineALL(img,pt1,pt2,Cmeasure.error_range,Cmeasure.measure_range,Cmeasure.measure_number)                        
                                    cv.ShowImage( "Display window: extract_Line drawHist " , img_drawLine );
                                    cv.WaitKey(1000); 
                                    #-----/before offset/-------------------                            
                                                            
                                   
                                    #---------do  offset --------------------
                                    #do (BigOffset+ SmallOffset) =   alignment
                                    pt1[0]=pt1[0]- Coutput_ali.alignment_x  # pixel (Big +small Offsets)
                                    pt2[0]=pt2[0]- Coutput_ali.alignment_x 
                                    pt1[1]=pt1[1]- Coutput_ali.alignment_y
                                    pt2[1]=pt2[1]- Coutput_ali.alignment_y
                                    
        
                                    #Dist_offsex=Chilight.Bigoffset_x**2+Chilight.Bigoffset_y**2-(Coutput_ali.alignment_x**2+Coutput_ali.alignment_y**2)
                                    # gaugeLines generate
                                    img_drawLine,imgcolor_gaugeROI ,pt1_base_gauge,pt2_head_gauge=Cmeasure.draw_gaugeLineALL(img,pt1,pt2,Cmeasure.error_range,Cmeasure.measure_range,Cmeasure.measure_number)                        
                                    # print"pt1_base_gauge:", pt1_base_gauge                                                        
                                   # print"pt2_head_gauge:", pt2_head_gauge
                                    cv.ShowImage( "Display window: extract_Line drawHist " , img_drawLine );
                                   # cv.ShowImage( "Display window: imgcolor_gaugeROI " , imgcolor_gaugeROI );
                                    cv.WaitKey(1000);
                                    
                                    file_name=Cimg.getImgFileName(Cimg.IMAGE)
                                    file_savePath="c:\\ROI_img\\"+Cmeasure.GAUGE+"_"+file_name
                                    print "#ROI_file_savePath=",file_savePath
                                   # cv.SaveImage(file_savePath,imgcolor_gaugeROI)
                                   
                                    # print "Chilight.Bigoffset_x",Chilight.Bigoffset_x
                                    #print "Chilight.Bigoffset_y",Chilight.Bigoffset_y
                                
                                    #dx_center_nmTopixel=int((pt1[0]+pt2[0])/2)
                                    #dy_center_nmTopixel=int((pt1[1]+pt2[1])/2)                                                               
                                    # print pt1,pt2,Cimg.IMAGE.replace("gif","png")                        
                                    
                                    #cv.ShowImage( "Display window: ForeGround_colorImg " , ForeGround_colorImg );
                                    #cv.WaitKey(0);
                                   #---------/do  offset/ --------------------
                                 
                                    
                                   
                      
                                    
                                   
                                    
                                    
                                    #----------For every pologon , calculate gaugeLines------------
                                    
                                    pt_N=len(pt1_base_gauge) # =len( pt2_head_gauge)
                                    # print "pt_N=", pt_N
                                    gaugeline_list=CAL.collect_gaugeLines(img,pt1_base_gauge,pt2_head_gauge,pt_N)
                                    print "per Gauge, gaugeline_list count=",len(gaugeline_list)   
                                    #print gaugeline_list[0]
                                    print "---------"
                                    
                                    #-----drawLine Histogram----------
                                    histdata=gaugeline_list[0] # the middle gaugeLine
                                    img_drawLine=FBG.drawImage_Histogram(  img_drawLine,histdata,(0,255,0),True)
                                    cv.ShowImage( "Display window: extract_Line drawHist " , img_drawLine );
                                    #cv.WaitKey(2000); 
                                    #-----/drawLine Histogram/--------   
                                    
                                   #----------/For every pologon , calculate gaugeLines/----------   
                                       
                                       
                                 
                                  
                                    #A.--------every gaugeline measure for inner and outter-------
                                    """
                                    #part A (gaugeLine measure):
                                    """ 
                                    if Cmeasure.measure_mode=="WIDTH":
                                        print "#Cmeasure.measure_mode=WIDTH"
                                        
                                        #Template_width_ROI,Template_widthHist=FBG.getImage_Histogram(imgcolor_gaugeROI)
                                        #cv.ShowImage( "Get width_TemplateROI " , Template_width_ROI );
                                        #cv.WaitKey(2000);
                                        #cv.DestroyWindow("Get width_TemplateROI ")
                                        #aa=FBG.drawImage_Histogram(img_drawLine,Template_widthHist)
                                        #cv.ShowImage( "width_TemplateROI " , aa );
                                        #cv.WaitKey(0);
                                            
                                        
                                        INNER_CD_FACTOR=float(Cconfig.INNER_CD_FACTOR)
                                        OUTER_CD_FACTOR=float(Cconfig.OUTER_CD_FACTOR)
                                        Inner_set,Peak_set,Outter_set=CAL.measure_gaugelines_InnerMean_0808(gaugeline_list,INNER_CD_FACTOR, OUTER_CD_FACTOR)                             
     #                                   Inner_set,Peak_set,Outter_set=CAL.measure_gaugelines_InnerMean(gaugeline_list,INNER_CD_FACTOR, OUTER_CD_FACTOR)                             
                                                                            # print "gaugeInner(mean,var)=",Inner_set
                                        # print "gaugePeak(mean,var)=",Peak_set
                                        # print "gaugeOutter(mean,var)=",Outter_set
                                        #  print "----------------"
                                        # cv.ShowImage( "Display window: extract_Line " , img_drawLine );
                                        # cv.WaitKey(0);
                                        
                                        img_ROIhisttogram,ROI_Hist_list=FBG.getImage_Histogram(imgcolor_gaugeROI,(0,255,0),True)
                                        #------CMRR--------
                                        CMRR,DSAE,imgHist_ROI_Template=Cmeasure.calculate_defect_index_CMRR(ROI_Hist_list,TemplateSpace_Histogram_list,img_ROIhisttogram)
                                        PutText_InImage(imgHist_ROI_Template,"CMRR="+str(CMRR),(100,100),(255,255,255))
                                        PutText_InImage(imgHist_ROI_Template,"DSAE="+str(DSAE),(100,256),(255,255,255))                                     
                                        cv.ShowImage( "imgHist(ROI & Template)CMRR" , imgHist_ROI_Template );
                                        #cv.WaitKey(1000); 
                                        #------/CMRR/--------      
                                       # print"ROI_Hist_list=",ROI_Hist_list,sum(ROI_Hist_list)
                                       # cv.ShowImage( "Display window: ROIimg_histtogram " , ROIimg_histtogram );
                                       # cv.WaitKey(1000);
                                       # cv.PutText(img_ROIhisttogram,"The Text,in OpenCV,just only wrote in English--",(100,100),(1,1),(255,255,255));
                                        file_name=Cimg.getImgFileName(Cimg.IMAGE)
                                        PutText_InImage(imgHist_ROI_Template,"DSAE="+str(DSAE),(100,50),(255,255,255))                                     
                            
                                        file_savePath="c:\\ROI_img\\"+Cmeasure.GAUGE+"_"+file_name
                                        cv.SaveImage(file_savePath,imgHist_ROI_Template)
                                        
                                      
                                        PutText_InImage(img_drawLine,"p2p length="+str(Peak_set[0]),(10,256),(0,255,255))                                         
                                        PutText_InImage(img_drawLine,"CMRR="+str(CMRR),(10,150),(0,255,0)    )
                                        PutText_InImage(img_drawLine,"DSAE="+str(DSAE),(10,200),(0,0,255)   )                                     
                                        file_savePath="c:\\Profile_img\\"+Cmeasure.GAUGE+"_"+file_name
                                        cv.SaveImage(file_savePath,img_drawLine)
                                        cv.ShowImage( "Display window: extract_Line drawHist " , img_drawLine );
                                        cv.WaitKey(1500); 
                                                                            
                                        
                                    #/A--------/every gaugeline measure for inner and outter/--------
                                    
                                    
                                    #B--------every Gauge ROI--------------
                                    
                                    """
                                    #part B (ROI defect index similarity):
                                    """
                                    if Cmeasure.measure_mode=="DEFECT":
                                        print "#Cmeasure.measure_mode=DEFECT"
                                        
                                        img_ROIhisttogram,ROI_Hist_list=FBG.getImage_Histogram(imgcolor_gaugeROI,(0,0,0),True)
                                        #------CMRR--------
                                        CMRR,DSAE,imgHist_ROI_Template=Cmeasure.calculate_defect_index_CMRR(ROI_Hist_list,TemplateSpace_Histogram_list,img_ROIhisttogram)
                                        PutText_InImage(imgHist_ROI_Template,"CMRR="+str(CMRR),(100,100),(255,255,255))
                                        PutText_InImage(imgHist_ROI_Template,"DSAE="+str(DSAE),(100,50),(255,255,255))                                    
                                        cv.ShowImage( "imgHist(ROI & Template)CMRR" , imgHist_ROI_Template );
                                       # cv.WaitKey(1000); 
                                         
                                        #------/CMRR/--------
                                         
                                        #cv.ShowImage( "Display window: ROIimg_histtogram " , ROIimg_histtogram );
                                        #cv.WaitKey(1000);
                                        file_name=Cimg.getImgFileName(Cimg.IMAGE)
                                        file_savePath="c:\\ROI_img\\"+Cmeasure.GAUGE+"_"+file_name
                                        cv.SaveImage(file_savePath,imgHist_ROI_Template)
    
                                       
                                        PutText_InImage(img_drawLine,"CMRR="+str(CMRR),(10,150),(0,255,0)    )
                                        PutText_InImage(img_drawLine,"DSAE="+str(DSAE),(10,200),(0,0,255)   )                                     
                                        file_savePath="c:\\Profile_img\\"+Cmeasure.GAUGE+"_"+file_name
                                     
                                        cv.ShowImage( "Display window: extract_Line drawHist " , img_drawLine );
                                        cv.WaitKey(1500); 
                                        cv.SaveImage(file_savePath,img_drawLine)
                                    #/B------/every Gauge ROI/--------------
                                    
                                    
                                    
                              
                                    
                              #-----------------------------/draw_gauge in Polygon/ ------------------------- 
                                   
                                                 
                                                 
                                                 
                                    #-------B. assessment output fileformat--------                              
                                    Coutput_ass=Class5_assessment_output()
                                   # print "Coutput_ali.scaling_x",Coutput_ali.scaling_x
                                    Coutput_ass.inner_mean=int( Inner_set[0]*  Coutput_ali.scaling_x) #'pixel To nm
                                    Coutput_ass.inner_variance=int(Inner_set[1]*Coutput_ali.scaling_x)#'pixel To nm
                                    Coutput_ass.outer_mean=int( Outter_set[0]*  Coutput_ali.scaling_x) #'pixel To nm
                                    Coutput_ass.outer_variance=int( Outter_set[1]*  Coutput_ali.scaling_x) #'pixel To nm
                                    
                                    Coutput_ass.defect_index= str(CMRR)
                                    
                                    peak_mean=int( Peak_set[0]*  Coutput_ali.scaling_x)
                                    peak_var=int( Peak_set[1]*  Coutput_ali.scaling_x)
                                    
                                    line_output_ass=Coutput_ass.gauge_measuremet(Cmeasure,Cimg,Coutput_ass)  
                                 #   print "-->"+line_output_ass.replace("\n",","+str(peak_mean)+"\n"  )                         
                                 #   fp_out_ass.writelines( line_output_ass)
                                    fp_out_ass.writelines( line_output_ass.replace("\n",","+str(peak_mean)+","+str(peak_var)+","+","+str(DSAE)+"\n"  )    )                                                  
                                    fp_out_ass.flush()    
                                   # print Coutput_ass.image_path
                                    # showimg(Coutput_ass.image_path)
                                    #cv.ShowImage( "Display window: extract_Line " , img_drawLine );
                                    #cv.WaitKey(0);   
                                    """
                                    #-----for test static------------------
                                    neme="A"
                                    name=Cimg.getImgFileName(Cimg.IMAGE)
                                    name=name.replace(".png","_")
                                    #print Cmeasure.gauge_tone
                                    if not Cmeasure.gauge_tone.__contains__("space"):
                                       # print "--->> Cmeasure.gauge_tone= pologon---)"
                                        print "--------------------   "
                                        if   peak_mean>30 :
                                            cv.SaveImage( "c:\\ERR_PPmean30_99\errPPmean_"+name+"_xalign_"+str(Coutput_ali.alignment_x)+".png" , img_drawLine );
                                           # cv.ShowImage( "Display window: peak_mean>30 " , img_drawLine );
                                           # cv.WaitKey(0);
                                        if   peak_mean<30:
                                            cv.SaveImage( "c:\\ERR_PPmean30\errPPmean_"+name+"_xalign_"+str(Coutput_ali.alignment_x)+".png" , img_drawLine );
                                            #cv.ShowImage( "Display window: peak_mean<30 " , img_drawLine );
                                            #cv.WaitKey(0);
                                        
                                        if   peak_var<6:
                                           #cv.ShowImage( "Display window: peak_mean<30 " , img_drawLine );
                                           #cv.WaitKey(0);
                                           cv.SaveImage( "c:\\ERR_PPvar11\errPPvar_"+name+"_xalign_"+str(Coutput_ali.alignment_x)+".png" , img_drawLine );
                                        if   peak_var>6 and peak_var<99 :
                                           #cv.ShowImage( "Display window: peak_mean<30 " , img_drawLine );
                                           #cv.WaitKey(0);
                                           cv.SaveImage( "c:\\ERR_PPvar11_99\errPPvar_"+name+"_xalign_"+str(Coutput_ali.alignment_x)+".png" , img_drawLine );
                                    #-----/for test static/------------------
                                    """ 
                                                                
                                    #-------/B. assessment output fileformat/--------
                                 
                             
                             
                             
                             
                            #---/For every gauge process of a hilightlight : B.assessment/------------
                                                    
                        #------/For every gauge in a Highlight/----------------------------------
                          
                                              
    #    print "ntimes=",ntimes    
    #   print "imageTimes=",countA
    #---------/search stage of all items/-----------------  
    
    
    #=============/End main/=================================================
        
                        """
                        #-----------polygon conuts-----------------                    
                        for lineC1 in Lines_polygon: #stage C1
                            Cpolygon= Class2_cell_polygon()
                            line_array = lineC1.split("\t")
                            Cpolygon.POLYGON=line_array[0]
                                
                            if not str(line_array[2]).__contains__("base"):  #number sureance   
                                if  Cpolygon.POLYGON.__contains__( Chilight.HIGHLIGHT):
                                  #  print Chilight.HIGHLIGHT, Cpolygon.POLYGON
                                  highlight_Polygons=highlight_Polygons+1
                        #  print "++++++++++++++++++"
                        #  print " highlight_Polygons", highlight_Polygons 
                        #-----------/polygon conuts/---------------------
                        """
                        
                        
    #lock.release() #释放琐  
if __name__ == "__main__":
   # for i in xrange(1):  
   #mainT()
   isopen_bigoffset=True    
   
  # thread.start_new_thread( mainT,(isopen_bigoffset,)   )
   mainT( isopen_bigoffset )
   
   
   