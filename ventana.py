import wx

app = wx.PySimpleApp()
frame1 = wx.Frame(None, title="Type Here...", pos=(0,0), size=(300,300))
frame2 = wx.Frame(None, title="...to get value here", pos=(310,0), size=(300,300))

tc1 = wx.TextCtrl(frame1)
tc2 = wx.TextCtrl(frame2)

def textChange(event):
    tc2.SetValue(tc1.GetValue())

tc1.Bind(wx.EVT_TEXT, textChange)

app.SetTopWindow(frame1)
frame1.Show()
frame2.Show()

app.MainLoop()