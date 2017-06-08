
import wx
import wx, wx.html
import cv2
import numpy 
import argparse
import numpy as np 
import Tkinter 
import FileDialog
import tkFileDialog
import tkMessageBox
from decimal import *
from matplotlib import pyplot as plt


#Inicializamos la ventana y agregamos el panel como hijo

class PhotoCtrl(wx.App):
    refPt = []
    cropping = False
    def __init__(self, redirect=False, filename=None, *args, **kwargs):
        super(PhotoCtrl, self).__init__(*args, **kwargs) 
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Sistema Medico',size=(3000,3000))       
        self.panel = wx.Panel(self.frame)
#Establecemos el  tamano maximo de la foto
        name_photo_1 = "No Definido"
        name_Photo_2 = "No Definido"
        self.PhotoMaxSize = 600
        self.createWidgets()
        self.frame.Show()

#--------------------------------------------------------------------------       
    def createWidgets(self):
        img = wx.EmptyImage(600,600)
        img_2 = wx.EmptyImage(600,600)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
        self.imageCtrl_2 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img_2))
        #Menu
        fileMenu = wx.Menu()
        self.photoTxt = wx.TextCtrl(self.panel, size=(200,-1))
        #Etiqueta ruta imagen
        label_ri = wx.StaticText(self.panel,label="Ruta de la Imagen",size=(200,20),style=wx.ALIGN_CENTER)
        #Boton 1
        browseBtn = wx.Button(self.panel, label='Abrir Primera Radiografia',size=(200,30),pos=(0,700))
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
        #Boton 2
        browseBtn_2 = wx.Button(self.panel, label='Abrir Segunda Radiografia',size=(200,30))
        browseBtn_2.Bind(wx.EVT_BUTTON, self.onBrowse)
        #Boton de rotar Primera Imagen 90 Derecha
        label_rot = wx.StaticText(self.panel,label="Rotaciones",size=(200,20),style=wx.ALIGN_CENTER)
        browseBtn_Rd_1 = wx.Button(self.panel, label='Rotar 90 Derecha Imagen 1',size=(200,30))
        browseBtn_Rd_1.Bind(wx.EVT_BUTTON, self.onRotate_90R)
        #Boton de rotar Primera Imagen 90 Izquierda
        browseBtn_Ri_1 = wx.Button(self.panel, label='Rotar 90 Izquierda Imagen 1',size=(200,30))
        browseBtn_Ri_1.Bind(wx.EVT_BUTTON, self.onRotate_90L)
        #Boton de Rotar Segunda Imagen 90 Derecha
        browseBtn_Rd_2 = wx.Button(self.panel, label='Rotar 90 Derecha Imagen 2',size=(200,30))
        browseBtn_Rd_2.Bind(wx.EVT_BUTTON, self.onRotate_90R)
        #Boton de Rotar Segunda Imagen 90 Izquierda
        browseBtn_Ri_2 = wx.Button(self.panel, label='Rotar 90 Izquierda Imagen 2',size=(200,30))
        browseBtn_Ri_2.Bind(wx.EVT_BUTTON, self.onRotate_90L)
        #Rotacion Libre Imagen 1
        browseBtn_rlibre_1=wx.Button(self.panel,label="Rotacion Libre Imagen 1",size=(200,30))
        browseBtn_rlibre_1.Bind(wx.EVT_BUTTON, self.onFreeRo)
        #Rotacion Libre Imagen 2
        browseBtn_rlibre_2=wx.Button(self.panel,label="Rotacion Libre Imagen 2",size=(200,30))
        browseBtn_rlibre_2.Bind(wx.EVT_BUTTON, self.onFreeRo)
        #Ajuste de Imagen
        label_ajustar = wx.StaticText(self.panel,label="Ajuste de Imagenes",size=(200,30))
        browseBtn_ajImg_1=wx.Button(self.panel,label="Imagen 1",size=(200,30))
        browseBtn_ajImg_1.Bind(wx.EVT_BUTTON, self.onCrop)

        browseBtn_ajImg_2=wx.Button(self.panel,label="Imagen 2",size=(200,30))
        browseBtn_ajImg_2.Bind(wx.EVT_BUTTON, self.onCrop)
        #Etiqueta Histograma
        label_histogram = wx.StaticText(self.panel,label="Histograma",size=(200,20),style=wx.ALIGN_CENTER)
        #Generar Hiograma A-B
        browseBtn_Histo = wx.Button(self.panel, label='Generar Histograma A-B',size=(200,30))
        browseBtn_Histo.Bind(wx.EVT_BUTTON, self.onHistograma)
        #Generar Hiograma B-A
        browseBtn_Histo_2 = wx.Button(self.panel, label='Generar Histograma B-A',size=(200,30))
        browseBtn_Histo_2.Bind(wx.EVT_BUTTON, self.onHistograma)

        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)

        #Agregamos al Mainsizer los bitmap
        self.sizer.Add(label_ri, 0 , wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl_2, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        #Agregamos la ubicacion de los Botones
        self.sizer.Add(browseBtn, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn_2, 0 , wx.ALL, 6) 
        self.sizer.Add(label_rot, 0 , wx.ALL, 5) 
        self.sizer.Add(browseBtn_Rd_1,0,wx.ALL,5)
        self.sizer.Add(browseBtn_Ri_1,0,wx.ALL,5) 
        self.sizer.Add(browseBtn_Rd_2,0,wx.ALL,5)
        self.sizer.Add(browseBtn_Ri_2,0,wx.ALL,5)
        self.sizer.Add(browseBtn_rlibre_1,0,wx.ALL,5)
        self.sizer.Add(browseBtn_rlibre_2,0,wx.ALL,5)
        self.sizer.Add(label_histogram, 0 , wx.ALL, 5) 
        self.sizer.Add(browseBtn_Histo,0,wx.ALL,5)
        self.sizer.Add(browseBtn_Histo_2,0,wx.ALL,5)
        self.sizer.Add(label_ajustar,0,wx.ALL,5)
        self.sizer.Add(browseBtn_ajImg_1,0,wx.ALL,5)
        self.sizer.Add(browseBtn_ajImg_2,0,wx.ALL,5)     
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()

#----------------------------------------------
    def OnQuit(self, e):
        self.Close()


#---------------------------------------------------------
    #Abre Explorador de Archivos    
    def onBrowse(self, event):
        id_b=event.GetEventObject().GetLabel()
        #Abrimos el explorador de archivos
        wildcard = "JPEG files (*.jpg)|*.jpg|" \
        "Dicom File (*.dicom)|*.dicom"
        dialog = wx.FileDialog(None, "Seleccione Un Archivo",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy() 
        self.onView(id_b)
        
#---------------------------------------------------------
    #Rota Imagenes derecha
    def onRotate_90R(self,event):
        id_b= event.GetEventObject().GetLabel()
        print id_b
        filepath = self.photoTxt.GetValue()
        #Rotaremos la imagen con opencv 
        #Abrimos la Imagen y obtenemos el tamano 
        image_cv = cv2.imread(filepath)
        (h,w)= image_cv.shape[:2]
        #Calculamos el centro de la rotacion y rotamos 90 
        center = (w/2,h/2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotated = cv2.warpAffine(image_cv, M, (w, h))
        cv2.imwrite(filepath,rotated)
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H =img.GetHeight()
        if W < H :
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(600,600)
        if(id_b=="Rotar 90 Derecha Imagen 1"):
            #Le decimos que ira hacia al primer imagrCtrl
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
            self.panel.Refresh()
            self.mainSizer.Fit(self.frame)
        else:
            #Le decimos que ira hacia el segundo imagrCtrl_2
            self.imageCtrl_2.SetBitmap(wx.BitmapFromImage(img))
            self.panel.Refresh()
            self.mainSizer.Fit(self.frame)

#---------------------------------------------------------
    #Rota Imagenes Izquierda
    def onRotate_90L(self,event):
        id_b= event.GetEventObject().GetLabel()
        print id_b
        filepath = self.photoTxt.GetValue()
        #Rotaremos la imagen con opencv 
        #Abrimos la Imagen y obtenemos el tamano 
        image_cv = cv2.imread(filepath)
        (h,w)= image_cv.shape[:2]
        #Calculamos el centro de la rotacion y rotamos 90 
        center = (w/2,h/2)
        M = cv2.getRotationMatrix2D(center,-90, 1.0)
        rotated = cv2.warpAffine(image_cv, M, (w, h))
        cv2.imwrite(filepath,rotated)
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H =img.GetHeight()
        if W < H :
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(600,600)
        if(id_b=="Rotar 90 Izquierda Imagen 1"):
            #Le decimos que ira hacia al primer imagrCtrl
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
            self.panel.Refresh()
            self.mainSizer.Fit(self.frame)
        else:
            #Le decimos que ira hacia el segundo imagrCtrl_2
            self.imageCtrl_2.SetBitmap(wx.BitmapFromImage(img))
            self.panel.Refresh()
            self.mainSizer.Fit(self.frame)
#-----------------------------------------------------------------------
    #Rotacion Libre 
    def onFreeRo(self,event):
        #Se obtiene los grados a rotar
        dlg = wx.TextEntryDialog(None, 'Grados','Rotacion Libre')
        if dlg.ShowModal() == wx.ID_OK:
            grados=float(dlg.GetValue())
            print(type(grados))
        dlg.Destroy()

        id_b= event.GetEventObject().GetLabel()
        print id_b
        filepath = self.photoTxt.GetValue()
        print filepath
        #Abrimos la Imagen y obtenemos el tamano 
        image_cv = cv2.imread(filepath)
        (h,w)= image_cv.shape[:2]
        #Calculamos el centro de la rotacion y rotamos 90 
        center = (w/2,h/2)
        M = cv2.getRotationMatrix2D(center,grados, 1.0)
        rotated = cv2.warpAffine(image_cv, M, (w, h))
        cv2.imwrite(filepath,rotated)
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H =img.GetHeight()
        if W < H :
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(600,600)
        if(id_b=="Rotacion Libre Imagen 1"):
            #Le decimos que ira hacia al primer imagrCtrl
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
            self.panel.Refresh()
            self.mainSizer.Fit(self.frame)
        else:
            #Le decimos que ira hacia el segundo imagrCtrl_2
            self.imageCtrl_2.SetBitmap(wx.BitmapFromImage(img))
            self.panel.Refresh()
            self.mainSizer.Fit(self.frame)


#------------------------------------------------------------------------
    #Muestra Imagenes
    def onView(self,id_i):
        """
        Intentamos Cargar la imagen y mostrarla
        """
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W < H :
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(600,600)
        if(id_i=="Abrir Primera Radiografia"):
            self.name_Photo_1 = filepath
            #Le decimos que ira hacia al primer imagrCtrl
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
            self.panel.Refresh()
            self.mainSizer.Fit(self.frame)
        else:
            self.name_Photo_2 = filepath
            #Le decimos que ira hacia el segundo imagrCtrl_2
            self.imageCtrl_2.SetBitmap(wx.BitmapFromImage(img))
            self.panel.Refresh()
            self.mainSizer.Fit(self.frame)

#---------------------------------------------------------

    #Aujuste de Imagen
    def onCrop(self,event):
        filepath = self.name_Photo_1
        #Ponemos la Imagen 1 en modo de espera para recibir los clicks
        global image
        global clone
        #Redimencionamos la imagen original a 600 px, creamos una copia para trabajar
        #sobre ella y la desplegamos en una nueva ventana
        image = cv2.imread(filepath)
        r = 600.0 / image.shape[1]
        dim = (600, int(image.shape[0] * r))
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        clone = image.copy()
        cv2.imshow("imagen",image)
        cv2.namedWindow("imagen")
        cv2.resizeWindow("imagen", 600,600)
        cv2.setMouseCallback("imagen",self.get_clicks)
    
    def get_clicks(self,event,x,y,flags,param):
        filepath = self.name_Photo_1
        global refPt
        global cropping
        #Detectamos los clicks y guardamos en rftPt
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True
        elif event == cv2.EVENT_LBUTTONUP:
            refPt.append((x, y))
            cropping = False
            # Dibujamos un rectangulo sobre la seleccion
            cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
            cv2.imshow("imagen", image)
            print (refPt)
            roi = clone[refPt[0][1]:refPt[1][1],refPt[0][0]:refPt[1][0]]
            #Guardamos el recorte y abrimos la imagen en la interfaz principal
            r = 600.0 / roi.shape[1]
            dim = (600, int(roi.shape[0] * r))
            roi = cv2.resize(roi, dim, interpolation = cv2.INTER_AREA)
            cv2.imwrite(filepath,roi)
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
            print img.GetSize()
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
            self.panel.Refresh()
            self.mainSizer.Fit(self.frame)
            cv2.destroyAllWindows()

#---------------------------------------------------------
    #Generacion del HistoGrama
    def onHistograma(self,event):
        im_1 = self.name_Photo_1
        im_2 = self.name_Photo_2
        id_b= event.GetEventObject().GetLabel()
        print id_b
        photo_1 = cv2.imread(im_1)
        photo_2 = cv2.imread(im_2)
        
        print photo_1.shape[0], photo_1.shape[1]
        col = photo_1.shape[0]
        fil = photo_1.shape[1]

        r = fil / photo_1.shape[0]
        dim = (int(photo_1.shape[1] * r), col)
        photo_2 = cv2.resize(photo_2, dim, interpolation = cv2.INTER_AREA)
        #Detectamos cual resta se hara
        print photo_2.shape[0], photo_2.shape[1]
        if(id_b=="Generar Histograma A-B"):
            d1 = cv2.absdiff(photo_1,photo_2)
        else:
            d1 = cv2.absdiff(photo_2,photo_1) 

        gray_image =cv2.cvtColor(d1,cv2.COLOR_BGR2GRAY) 
        gray_image_2 =cv2.cvtColor(photo_1,cv2.COLOR_BGR2GRAY) 

        val_prom_res = 0;
        val_prom_ini = 0;

        #Calculamos el valor promedio de escala de grises para la imagen resultante
        for i in range(gray_image.shape[0]):
            for j in xrange(gray_image.shape[1]):
                val_prom_res = val_prom_res + gray_image[i][j]


        #Calculamos el valor promedio de escala de grises para la imagen inicia
        for i in range(gray_image_2.shape[0]):
            for j in xrange(gray_image_2.shape[1]):
                val_prom_ini = val_prom_ini + gray_image_2[i][j]

        ganancia_osea = (Decimal(val_prom_res)/Decimal(val_prom_ini))*100

        self.new = NewWindow(parent=None, id=-1, g_osea=ganancia_osea,inicial=val_prom_ini,resultante=val_prom_res)
        self.new.Show()
        plt.imshow(d1)
        hist = cv2.calcHist([d1], [0], None, [256], [0, 256])
        plt.figure()
        plt.title("Grayscale Histogram")
        plt.xlabel("Bins")
        plt.ylabel("# of Pixels")
        plt.plot(hist)
        plt.xlim([0, 256])
        plt.show()



class NewWindow(wx.Frame):

    def __init__(self,parent,id,g_osea,inicial,resultante):
        wx.Frame.__init__(self, parent, id, 'New Window', size=(450,200))
        wx.Frame.CenterOnScreen(self)
        panel = wx.Panel(self) 
        box = wx.BoxSizer(wx.VERTICAL) 
        lbl = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER) 
            
        txt1 = "GANANCIA OSEA = "+str(g_osea)+"\n"
        txt2= "Valor promedio de los tonos de girs de la imagen resultante = " + str(resultante)+"\n"
        txt3 = "Valor promedio de los tonos de girs de la imagen inicial = "+ str(inicial) 
        txt = txt1 + txt2 + txt3 

        font = wx.Font(10, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        lbl.SetFont(font) 
        lbl.SetLabel(txt) 


class MyWindowsInfo(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Ingresar", size=(300, 250))
        self.panel = wx.Panel(self,-1)
        wx.StaticText(self.panel, -1, "Sistema Medico para el Analisis de Radiografias", pos=(20, 12))
        wx.StaticText(self.panel, -1, "Guillermo Vara De Gante", pos=(70, 48))
        wx.StaticText(self.panel, -1, "Dr. Barbara Emma Sanchez Rinza", pos=(50, 64))
        wx.StaticText(self.panel, -1, "Dr. Alberto Jaramillo Nunez", pos=(60, 80))
        wx.StaticText(self.panel, -1, "Version 1.0 ", pos=(100, 94))
        button=wx.Button(self.panel,label="Ingresar",pos=(90, 150), size = (100,50))
        self.Bind(wx.EVT_BUTTON, self.newwindow, button)

    def newwindow(self, event):
        app = PhotoCtrl()
        self.Close()
        app.MainLoop()


#------------------------------------------------------------------------
#Main      
if __name__ == '__main__':
    app = wx.App(False)
    frame = MyWindowsInfo()
    frame.Show(True)
    frame.Centre()

    app.MainLoop()