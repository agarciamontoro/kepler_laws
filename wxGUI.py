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

#class MyApp(wx.App):
#    def OnInit(self):
#        frame = MyFrame(None, -1, 'Choose the planets you want to see.')
#        frame.Show(True)
#        return True

class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(900,500), style=wx.DEFAULT_DIALOG_STYLE)

        hbox  = wx.BoxSizer(wx.HORIZONTAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.GridSizer(3,2,0,0)
        vbox4 = wx.BoxSizer(wx.VERTICAL)
        pnl1 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        pnl2 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.InsertColumn(0, 'Planet')
        self.lc.InsertColumn(1, 'Date for u')
        self.lc.InsertColumn(2, 'Anomaly for t')
        self.lc.InsertColumn(3, 'Energy')
        self.lc.InsertColumn(4, 'Momentum')
        self.lc.SetColumnWidth(0, 140)
        self.lc.SetColumnWidth(1, 153)
        vbox1.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        vbox1.Add(pnl2, 1, wx.EXPAND | wx.ALL, 3)
        vbox2.Add(self.lc, 1, wx.EXPAND | wx.ALL, 3)
        self.tc1 = wx.TextCtrl(pnl1, -1)
        self.tc2 = wx.TextCtrl(pnl1, -1)
        vbox3.AddMany([ (wx.StaticText(pnl1, -1, 'Date'),0, wx.ALIGN_CENTER),
                        (self.tc1, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL),
                        (wx.StaticText(pnl1, -1, 'Eccentric anomaly'),0, wx.ALIGN_CENTER_HORIZONTAL),
                        (self.tc2,0)])
        vbox3.Add(wx.Button(pnl1, 10, 'Calculate'),   0, wx.ALIGN_CENTER| wx.BOTTOM)
        pnl1.SetSizer(vbox3)


        self.rb1 = wx.CheckBox(pnl2, -1, 'Mercury')
        self.rb2 = wx.CheckBox(pnl2, -1, 'Venus')
        self.rb3 = wx.CheckBox(pnl2, -1, 'Earth')
        self.rb4 = wx.CheckBox(pnl2, -1, 'Mars')
        self.rb5 = wx.CheckBox(pnl2, -1, 'Jupiter')
        self.rb6 = wx.CheckBox(pnl2, -1, 'Saturn')
        self.rb7 = wx.CheckBox(pnl2, -1, 'Uranus')
        self.rb8 = wx.CheckBox(pnl2, -1, 'Neptune')
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

        vbox4.Add(self.rb1, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        vbox4.Add(self.rb2, 0, wx.ALIGN_LEFT|wx.TOP, 6)
        vbox4.Add(self.rb3, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        vbox4.Add(self.rb4, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        vbox4.Add(self.rb5, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        vbox4.Add(self.rb6, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        vbox4.Add(self.rb7, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        vbox4.Add(self.rb8, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        pnl2.SetSizer(vbox4)
        self.Bind (wx.EVT_BUTTON, self.OnAdd, id=10)
        self.Bind (wx.EVT_BUTTON, self.OnRemove, id=11)
        self.Bind (wx.EVT_BUTTON, self.OnClear, id=12)
        self.Bind (wx.EVT_BUTTON, self.OnClose, id=13)
        hbox.Add(vbox1, 1, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND)
        self.SetSizer(hbox)

    def OnAdd(self, event):
        if not self.tc1.GetValue() or not self.tc2.GetValue():
            return
        num_items = self.lc.GetItemCount()
        self.lc.InsertStringItem(num_items, self.tc1.GetValue())
        self.lc.SetStringItem(num_items, 1, self.tc2.GetValue())
        self.tc1.Clear()
        self.tc2.Clear()

    def OnRemove(self, event):
        index = self.lc.GetFocusedItem()
        self.lc.DeleteItem(index)

    def OnClose(self, event):
        self.Close()

    def OnClear(self, event):
        self.lc.DeleteAllItems()

    def SetVal(self, event):
        draw_planets["Mercury"] = self.rb1.GetValue()
        draw_planets["Venus"] = self.rb2.GetValue()
        draw_planets["Earth"] = self.rb3.GetValue()
        draw_planets["Mars"] = self.rb4.GetValue()
        draw_planets["Jupiter"] = self.rb5.GetValue()
        draw_planets["Saturn"] = self.rb6.GetValue()
        draw_planets["Uranus"] = self.rb7.GetValue()
        draw_planets["Neptune"] = self.rb8.GetValue()

class MyApp(wx.App):
    def OnInit(self):
        dia = MyDialog(None, -1, 'Solar System')
        dia.Show(True)
        #dia.ShowModal()
        #dia.Destroy()
        return True
