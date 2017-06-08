import wx

class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "My Frame", size=(3000, 3000))
        self.panel = wx.Panel(self,-1)
        #self.panel.Bind(wx.EVT_MOTION,  self.OnMove)
        wx.StaticText(self.panel, -1, "What are the values of X", pos=(10, 12))
        #self.posCtrl = wx.TextCtrl(self.panel, -1, "", pos=(100, 10))
        wx.CheckBox(self.panel, -1, "Apples", (20,100), (160,-1))
        wx.CheckBox(self.panel, -1, "Mango", (20,150), (160,-1))
        wx.CheckBox(self.panel, -1, "Banana", (20,200), (160,-1))
        wx.CheckBox(self.panel, -1, "Orange", (20,250), (160,-1))
        button=wx.Button(self.panel,label="OK",pos=(800, 400), size = (50,50))
        self.Bind(wx.EVT_BUTTON, self.newwindow, button)

    # def OnMove(self, event):
        # pos = event.GetPosition()
        # self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))


    def newwindow(self, event):
        secondWindow = window2(parent=self.panel)
        secondWindow.Show()


class window2(wx.Frame):

    title = "new Window"

    def __init__(self,parent):
        wx.Frame.__init__(self,parent, -1,'Window2', size=(1000,700))
        panel=wx.Panel(self, -1)

        self.SetBackgroundColour(wx.Colour(100,100,100))
        self.Centre()
        self.Show()

app = wx.App(False)
frame = MyFrame()
frame.Show(True)
app.MainLoop()