import wx

from datetime import *

draw_planets = {"Mercury" : True,
                "Venus" : True,
                "Earth" : True,
                "Mars" : True,
                "Jupiter" : True,
                "Saturn" : True,
                "Uranus" : True,
                "Neptune" : True}

current_date = datetime.today()

class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(900,500), style=wx.DEFAULT_DIALOG_STYLE)

        #Complete Panel
        hbox  = wx.BoxSizer(wx.HORIZONTAL)

        #Left Panel
        vbox1 = wx.BoxSizer(wx.VERTICAL)


        pnl1 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        pnl2 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        pnl3 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        vbox1.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        vbox1.Add(pnl2, 1, wx.EXPAND | wx.ALL, 3)
        vbox1.Add(pnl3, 1, wx.EXPAND | wx.ALL, 3)


        #Date Panel
        self.tc_date_dd = wx.SpinCtrl(pnl1, -1, '15', (55,90), (60,-1), min=1, max=31)
        self.tc_date_mm = wx.SpinCtrl(pnl1, -1, '12', (55,90), (60,-1), min=1, max=12)
        self.tc_date_yy = wx.SpinCtrl(pnl1, -1, '2015', (55,90), (60,-1), min=1, max=9999)
        self.main_calc_but = wx.Button(pnl1, 10, 'Calculate')

        grid1 = wx.GridSizer(2,4,0,0)
        grid1.AddMany([ (wx.StaticText(pnl1, -1, 'Date'),0, wx.ALIGN_CENTER),
                        (self.tc_date_dd, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL),
                        (self.tc_date_mm, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL),
                        (self.tc_date_yy, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL),(0,0),
                        (self.main_calc_but,   0, wx.ALIGN_CENTER| wx.BOTTOM)])

        pnl1.SetSizer(grid1)
        self.Bind(wx.EVT_BUTTON, self.OnCalculate, id=self.main_calc_but.GetId())



        #Panel del medio
        planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus','Neptune']

        self.tc_ecc = wx.TextCtrl(pnl2, -1)
        self.combo = wx.ComboBox(pnl2, -1, choices=planets, style=wx.CB_READONLY)
        self.result =  wx.StaticText(pnl2, -1, '')
        self.main_calc_date_but = wx.Button(pnl2, 10, 'CalculateDate')

        grid2 = wx.GridSizer(2,4,0,0)
        grid2.AddMany([ (wx.StaticText(pnl2, -1, 'Ecc. anomaly'),0, wx.ALIGN_CENTER),
                        (self.tc_ecc, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL),
                        (wx.StaticText(pnl2, -1, 'for'),0, wx.ALIGN_CENTER),
                        (self.combo, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL),
                        (self.main_calc_date_but, 0, wx.ALIGN_CENTER| wx.BOTTOM),(0,0),
                        (self.result, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)])

        pnl2.SetSizer(grid2)
        self.Bind(wx.EVT_BUTTON, self.OnCalculateDate, id=self.main_calc_date_but.GetId())


        #Rigth Panel

        #CheckBoxes
        checkbox = wx.BoxSizer(wx.VERTICAL)
        self.rb1 = wx.CheckBox(pnl3, -1, 'Mercury')
        self.rb2 = wx.CheckBox(pnl3, -1, 'Venus')
        self.rb3 = wx.CheckBox(pnl3, -1, 'Earth')
        self.rb4 = wx.CheckBox(pnl3, -1, 'Mars')
        self.rb5 = wx.CheckBox(pnl3, -1, 'Jupiter')
        self.rb6 = wx.CheckBox(pnl3, -1, 'Saturn')
        self.rb7 = wx.CheckBox(pnl3, -1, 'Uranus')
        self.rb8 = wx.CheckBox(pnl3, -1, 'Neptune')
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

        checkbox.Add(self.rb1, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        checkbox.Add(self.rb2, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        checkbox.Add(self.rb3, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        checkbox.Add(self.rb4, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        checkbox.Add(self.rb5, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        checkbox.Add(self.rb6, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        checkbox.Add(self.rb7, 0, wx.ALIGN_LEFT| wx.TOP, 6)
        checkbox.Add(self.rb8, 0, wx.ALIGN_LEFT| wx.TOP, 6)

        pnl3.SetSizer(checkbox)



        vbox2 = wx.BoxSizer(wx.VERTICAL)

        #List control
        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.InsertColumn(0, 'Planet')
        self.lc.InsertColumn(1, 'Anomaly for t')
        self.lc.InsertColumn(2, 'Energy')
        self.lc.InsertColumn(3, 'Momentum')
        #self.lc.SetColumnWidth(0, 140)

        vbox2.Add(self.lc, 1, wx.EXPAND | wx.ALL, 3)



        hbox.Add(vbox1, 1, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND)
        self.SetSizer(hbox)

    def OnCalculate(self, event):
        global current_date

        str_day = self.tc_date_dd.GetValue()
        str_month = self.tc_date_mm.GetValue()
        str_year = self.tc_date_yy.GetValue()

        if not (str_day and str_month and str_year):
            return

        day = int(str_day)
        month = int(str_month)
        year = int(str_year)

        current_date =  datetime(year, month, day)

    def OnCalculateDate(self,event):
        date = 15
        self.result.SetLabel(str(date))


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
