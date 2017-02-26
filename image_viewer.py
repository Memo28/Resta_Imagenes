import wx
import cv2
import numpy 
import numpy as np 
import Tkinter 
import FileDialog
from matplotlib import pyplot as plt

#Inicializamos la ventana y agregamos el panel como hijo
class PhotoCtrl(wx.App):
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
        #Etiqueta Histograma
        label_histogram = wx.StaticText(self.panel,label="Histograma",size=(200,20),style=wx.ALIGN_CENTER)
        #Generar Hiograma
        browseBtn_Histo = wx.Button(self.panel, label='Generar Histograma',size=(200,30))
        browseBtn_Histo.Bind(wx.EVT_BUTTON, self.onHistograma)

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
        img = img.Scale(500,500)
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
        img = img.Scale(500,500)
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
        img = img.Scale(500,500)
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
        img = img.Scale(500,500)
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
    #Generacion del HistoGrama
    def onHistograma(self,event):
        im_1 = self.name_Photo_1
        im_2 = self.name_Photo_2
        print im_1
        print im_2
        photo_1 = cv2.imread(im_1)
        photo_2 = cv2.imread(im_2)
        d1 = cv2.absdiff(photo_2,photo_1)
        cv2.imshow('resultado',d1)
        hist = cv2.calcHist([d1], [0], None, [256], [0, 256])
        plt.figure()
        plt.title("Grayscale Histogram")
        plt.xlabel("Bins")
        plt.ylabel("# of Pixels")
        plt.plot(hist)
        plt.xlim([0, 256])
        plt.show()

#------------------------------------------------------------------------
#Main      
if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()