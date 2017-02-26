import wx
import cv2
import numpy as np
import Tkinter
import FileDialog
from matplotlib import pyplot as plt


class windowClass(wx.Frame):
    name_Photo_1 = "No Definido"
    name_Photo_2 = "No Definido"

    def __init__(self,*args,**kwargs):
        super(windowClass,self).__init__(*args,**kwargs)
        self.PhotoMaxSize = 500
        self.window()


    def window(self):
        #Especificaciones de la ventana
        self.SetTitle('Verificador')
        self.SetSize(wx.Size(1100,600))
        #Barra de Menu
        menuBar = wx.MenuBar()
        Imagen1Button = wx.Menu()
        Imagen2Button = wx.Menu()
        #Contenedores de Imagenes
        img = wx.EmptyImage(400,400)
        img_2 = wx.EmptyImage(400,400)
        self.imageCtrl = wx.StaticBitmap(self,wx.ID_ANY,wx.BitmapFromImage(img))
        self.imageCtrl_2 = wx.StaticBitmap(self,wx.ID_ANY,wx.BitmapFromImage(img_2))
        self.imageCtrl.SetPosition((50,50))
        self.imageCtrl_2.SetPosition((500,50))
        self.photoTxt = wx.TextCtrl(self, size=(200,-1))
        self.photoTxt.SetPosition((150,480))

        #Menu
        rotar90_Im1 = Imagen1Button.Append(wx.ID_ANY,'Rotar 90','Rota la Primera Imagen +90 Grados')
        rotar_Menos_90_Im1 = Imagen1Button.Append(wx.ID_ANY,'Rotar -90','Rota la Primera Imagen -90 Grados')
        rotar_Libre_1 = Imagen1Button.Append(wx.ID_ANY,'Rotacion Libre','Rotacion Libre de la Primera Imagen')
        rotar90_Im2 = Imagen2Button.Append(wx.ID_ANY, 'Rotar 90', 'Rota la Segunda Imagen -90 Grados')
        rotar_Menos_90_Im2 = Imagen2Button.Append(wx.ID_ANY, 'Rotar -90', 'Rota la Segunda Imagen  -90 Grados')
        rotar_Libre_2 = Imagen2Button.Append(wx.ID_ANY,'Rotacion Libre','Rotacion Libre de la Segunde Imagen')
        histograma_Im1 = Imagen1Button.Append(wx.ID_ANY,'Histograma Im 1 - Ima2','Restar 1 menos 2')
        histograma_Im2 = Imagen2Button.Append(wx.ID_ANY,'Histograma Im 2 - Ima1','Restar 2 menos 1')



        #Botones
        browseBtn = wx.Button(self, label='Abrir Primera Radiografia')
        browseBtn.SetPosition((920,50))
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowser)
        browseBtn_2 = wx.Button(self, label='Abrir Segunda Radiografia')
        browseBtn_2.SetPosition((920,100))
        browseBtn_2.Bind(wx.EVT_BUTTON, self.onBrowser)


        menuBar.Append(Imagen1Button,'Operaciones Imagen 1')
        menuBar.Append(Imagen2Button,'Operaciones Imagen 2')

        #Agregamos a la ventana
        self.SetMenuBar(menuBar)

        #Bind sirve para lanzar evento
        #Imagen 1
        #self.Bind(wx.EVT_MENU,self.Rotar_90,rotar90_Im1,id=rotar90_Im1.GetId())
        self.Bind(wx.EVT_MENU,self.Rotar_90,rotar90_Im1)

        self.Bind(wx.EVT_MENU,self.Rotar_M_90,rotar_Menos_90_Im1)
        self.Bind(wx.EVT_MENU,self.Rotar_Libre,rotar_Libre_1)
        #Imagen 2
        self.Bind(wx.EVT_MENU,self.Rotar_90,rotar90_Im2)
        self.Bind(wx.EVT_MENU,self.Rotar_M_90,rotar_Menos_90_Im2)
        self.Bind(wx.EVT_MENU,self.Rotar_Libre,rotar_Libre_2)
        self.Bind(wx.EVT_MENU,self.Histograma,histograma_Im1)
        self.Bind(wx.EVT_MENU,self.Histograma,histograma_Im2)


        self.Show(True)


    def Rotar_90(self,event):
        #Comprueba si la hay una imagen abierta
        item = self.GetMenuBar().FindItemById(event.GetId())
        text = item.GetHelp()
        #print text
        imagen_abierta = self.Comprobacion(text)
        if(imagen_abierta == True):
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
            img = img.Scale(400,400)
            if(text=="Rota la Primera Imagen +90 Grados"):
                    #Le decimos que ira hacia al primer imagrCtrl
                self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
                self.Refresh()
            else:
                    #Le decimos que ira hacia el segundo imagrCtrl_2
                self.imageCtrl_2.SetBitmap(wx.BitmapFromImage(img))
                self.Refresh()


    def Rotar_M_90(self,event):

        item = self.GetMenuBar().FindItemById(event.GetId())
        text = item.GetHelp()
        imagen_Abierta= self.Comprobacion(text)
        if(imagen_Abierta):
            filepath = self.photoTxt.GetValue()
            #Rotaremos la imagen con opencv
            #Abrimos la Imagen y obtenemos el tamano
            image_cv = cv2.imread(filepath)
            (h,w)= image_cv.shape[:2]
            #Calculamos el centro de la rotacion y rotamos 90
            center = (w/2,h/2)
            M = cv2.getRotationMatrix2D(center, -90, 1.0)
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
            img = img.Scale(400,400)
            if(text=="Rota la Primera Imagen -90 Grados"):
                #Le decimos que ira hacia al primer imagrCtrl
                self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
                self.Refresh()
            else:
                #Le decimos que ira hacia el segundo imagrCtrl_2
                self.imageCtrl_2.SetBitmap(wx.BitmapFromImage(img))
                self.Refresh()


    def Rotar_Libre(self,event):
        imagen_Abierta= self.Comprobacion()
        if(imagen_Abierta):
            dlg = wx.TextEntryDialog(None,'Angulo de Rotacion','Rotacion Libre', '90')
            ret = dlg.ShowModal()
            if ret == wx.ID_OK:
                valor = dlg.GetValue()
                print(valor)
            else:
                print('You don\'t know')
            dlg.Destroy()
            item = self.GetMenuBar().FindItemById(event.GetId())
            text = item.GetHelp()
            print text
            filepath = self.photoTxt.GetValue()
            #Rotaremos la imagen con opencv
            #Abrimos la Imagen y obtenemos el tamano
            image_cv = cv2.imread(filepath)
            (h,w)= image_cv.shape[:2]
            #Calculamos el centro de la rotacion y rotamos 90
            center = (w/2,h/2)
            M = cv2.getRotationMatrix2D(center, float(valor), 1.0)
            rotated = cv2.warpAffine(image_cv, M, (w, h))
            cv2.imwrite(filepath,rotated)
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
            W = img.GetWidth()
            H =img.GetHeight()
            if W < H :
                NewW = self.PhotoMaxSize
                NewH = self.PhotoMaxSize * (H/0.2) / W
            else:
                NewH = self.PhotoMaxSize
                NewW = self.PhotoMaxSize * (W/0.2) / H
            img = img.Scale(400,400)
            if(text=="Rotacion Libre de la Primera Imagen"):
                #Le decimos que ira hacia al primer imagrCtrl
                self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
                self.Refresh()
            else:
                #Le decimos que ira hacia el segundo imagrCtrl_2
                self.imageCtrl_2.SetBitmap(wx.BitmapFromImage(img))
                self.Refresh()

    #Obtencion del Histograma
    def Histograma(self,event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        text = item.GetHelp()
        print text
        imagenes_abiertas = self.Comprobacion_Doble()
        if(imagenes_abiertas):
            if(text == "Restar 1 menos 2"):
                print("Primer Caso")
                print "Foto Uno" + self.name_Photo_1
                print "Foto Dos" + self.name_Photo_2

                diff1= cv2.imread(self.name_Photo_1)
                diff2= cv2.imread(self.name_Photo_2)

                image_dif= cv2.absdiff(diff1,diff2)
                image_dif = cv2.cvtColor(image_dif, cv2.COLOR_BGR2GRAY)
                ret,thresh1 = cv2.threshold(image_dif,127,255,cv2.THRESH_BINARY)
                plt.hist(image_dif.ravel(),256,[0,256]); plt.show()
                print ("OK")
            else:
                print("Segundo Caso")
                print "Foto Uno" + self.name_Photo_1
                print "Foto Dos" + self.name_Photo_2

                diff1= cv2.imread(self.name_Photo_1)
                diff2= cv2.imread(self.name_Photo_2)

                image_dif= cv2.absdiff(diff2,diff1)
                image_dif = cv2.cvtColor(image_dif, cv2.COLOR_BGR2GRAY)
                ret,thresh1 = cv2.threshold(image_dif,127,255,cv2.THRESH_BINARY)
                plt.hist(image_dif.ravel(),256,[0,256]); plt.show()


    #Navegador para Seleccionar Imagen
    def onBrowser(self,event):
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
        print(id_b)
        self.onView(id_b)

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
        img = img.Scale(400,400)
        if(id_i=="Abrir Primera Radiografia"):
            self.name_Photo_1 = filepath
            #Le decimos que ira hacia al primer imagrCtrl
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
            self.Refresh()
        else:
            self.name_Photo_2 = filepath
            #Le decimos que ira hacia el segundo imagrCtrl_2
            self.imageCtrl_2.SetBitmap(wx.BitmapFromImage(img))
            self.Refresh()
            #self.Fit(self)
    #Comprobacion de Rotacion si imagen esta abierta

    def Comprobacion(self,event):
        print event
        if( event == "Rota la Primera Imagen +90 Grados"):
            if ( self.name_Photo_1!= "No Definido" ):
                return True
            else:
                wx.MessageBox("Por Favor Abra una Imagen", "Error" ,wx.OK | wx.ICON_INFORMATION)
                return False
        else:
            if(self.name_Photo_2 != "No Definido"):
                 return True
            else:
                wx.MessageBox("Por Favor Abra una Imagen", "Error" ,wx.OK | wx.ICON_INFORMATION)
                return False


    def Comprobacion_Doble(self):
        if (self.name_Photo_1 != "No Definido" and self.name_Photo_2 != "No Definido"):
            return True
        else:
            wx.MessageBox("Se Necesitan 2 Imagenes para esta Operacion", "Error" ,wx.OK | wx.ICON_INFORMATION)
            return False





def main():
    app = wx.App()
    windowClass(None)
    app.MainLoop()


main()
