import wx

draw_planets = {"Mercury" : True,
                "Venus" : True,
                "Earth" : True,
                "Mars" : True,
                "Jupiter" : True,
                "Saturn" : True,
                "Uranus" : True,
                "Neptune" : True}

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.Point(1050,300), wx.Size(150, 200))
        panel = wx.Panel(self, -1)
        self.rb1 = wx.CheckBox(panel, -1, 'Mercury',(10, 10))
        self.rb2 = wx.CheckBox(panel, -1, 'Venus',  (10, 30))
        self.rb3 = wx.CheckBox(panel, -1, 'Earth',  (10, 50))
        self.rb4 = wx.CheckBox(panel, -1, 'Mars',   (10, 70))
        self.rb5 = wx.CheckBox(panel, -1, 'Jupiter',(10, 90))
        self.rb6 = wx.CheckBox(panel, -1, 'Saturn', (10, 110))
        self.rb7 = wx.CheckBox(panel, -1, 'Uranus', (10, 130))
        self.rb8 = wx.CheckBox(panel, -1, 'Neptune',(10, 150))
        self.Bind(wx.EVT_CHECKBOX, self.SetVal, id=self.rb1.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetVal, id=self.rb2.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetVal, id=self.rb3.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetVal, id=self.rb4.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetVal, id=self.rb5.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetVal, id=self.rb6.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetVal, id=self.rb7.GetId())
        self.Bind(wx.EVT_CHECKBOX, self.SetVal, id=self.rb8.GetId())

        self.rb1.SetValue(True)
        self.rb2.SetValue(True)
        self.rb3.SetValue(True)
        self.rb4.SetValue(True)
        self.rb5.SetValue(True)
        self.rb6.SetValue(True)
        self.rb7.SetValue(True)
        self.rb8.SetValue(True)

    def SetVal(self, event):
        draw_planets["Mercury"] = self.rb1.GetValue()
        draw_planets["Venus"] = self.rb2.GetValue()
        draw_planets["Earth"] = self.rb3.GetValue()
        draw_planets["Mars"] = self.rb4.GetValue()
        draw_planets["Jupiter"] = self.rb5.GetValue()
        draw_planets["Saturn"] = self.rb6.GetValue()
        draw_planets["Uranus"] = self.rb7.GetValue()
        draw_planets["Neptune"] = self.rb8.GetValue()

    def onClose(self, event):
        self.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Choose the planets you want to see.')
        frame.Show(True)
        #frame.Left()
        return True
