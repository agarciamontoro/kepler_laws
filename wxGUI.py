import wx

from datetime import *


planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn',
           'Uranus', 'Neptune']

draw_planets = {"Mercury": True,
                "Venus": True,
                "Earth": True,
                "Mars": True,
                "Jupiter": True,
                "Saturn": True,
                "Uranus": True,
                "Neptune": True}

current_date = datetime.today()


class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(1600, 250),
                           style=wx.DEFAULT_DIALOG_STYLE)

        # Complete Panel
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        vbox0 = wx.BoxSizer(wx.VERTICAL)

        pnl3 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        vbox0.Add(pnl3, 1, wx.EXPAND | wx.ALL, 3)

        # CheckBoxes
        checkbox = wx.BoxSizer(wx.VERTICAL)

        self.cb = {}

        for planet in planets:
            self.cb[planet] = wx.CheckBox(pnl3, -1, planet)
            self.Bind(wx.EVT_CHECKBOX, self.SetVal, id=self.cb[planet].GetId())
            self.cb[planet].SetValue(True)
            checkbox.Add(self.cb[planet], 0, wx.ALIGN_LEFT | wx.TOP, 6)

        pnl3.SetSizer(checkbox)

        # Center Panel
        vbox1 = wx.BoxSizer(wx.VERTICAL)

        pnl1 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        pnl2 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)

        vbox1.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        vbox1.Add(pnl2, 1, wx.EXPAND | wx.ALL, 3)

        # Date Panel
        self.tc_date_dd = wx.SpinCtrl(pnl1, -1, '15', (55, 90), (60, -1),
                                      min=1, max=31)
        self.tc_date_mm = wx.SpinCtrl(pnl1, -1, '12', (55, 90), (60, -1),
                                      min=1, max=12)
        self.tc_date_yy = wx.SpinCtrl(pnl1, -1, '2015', (55, 90), (60, -1),
                                      min=1, max=9999)
        self.main_calc_but = wx.Button(pnl1, -1, 'Calculate by date')

        self.tc_days = wx.TextCtrl(pnl1, -1)
        self.days_calc_but = wx.Button(pnl1, -1, 'Calculate by days')

        grid1 = wx.GridSizer(3, 4, 0, 0)
        grid1.AddMany([(wx.StaticText(pnl1, -1, 'Date'), 0, wx.ALIGN_CENTER),
                        (self.tc_date_dd, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),
                        (self.tc_date_mm, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),
                        (self.tc_date_yy, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),
                        (wx.StaticText(pnl1, -1, 'Days'), 0, wx.ALIGN_CENTER),
                        (self.tc_days, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),(0, 0),(0, 0),(0, 0),
                        (self.main_calc_but, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER),
                        (self.days_calc_but, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)])

        pnl1.SetSizer(grid1)
        self.Bind(wx.EVT_BUTTON, self.OnCalculate,
                  id=self.main_calc_but.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnCalculateDays,
                  id=self.days_calc_but.GetId())

        # Ecc panel
        self.tc_ecc = wx.TextCtrl(pnl2, -1)
        self.combo = wx.ComboBox(pnl2, -1, choices=planets,
                                 style=wx.CB_READONLY)
        self.result = wx.StaticText(pnl2, -1, '')
        self.main_calc_date_but = wx.Button(pnl2, -1, 'Calculate date')

        grid2 = wx.GridSizer(2, 3, 0, 0)
        grid2.AddMany([(wx.StaticText(pnl2, -1, 'Ecc. anomaly'), 0,
                        wx.ALIGN_CENTER),
                       (self.tc_ecc, 0,
                        wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),
                       (self.combo, 0,
                        wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),
                       (self.main_calc_date_but, 0,
                        wx.ALIGN_CENTER | wx.BOTTOM),
                       (self.result, 0,
                        wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)])

        pnl2.SetSizer(grid2)
        self.Bind(wx.EVT_BUTTON, self.OnCalculateDate,
                  id=self.main_calc_date_but.GetId())

        # Rigth Panel

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        # List control
        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.InsertColumn(0, 'Planet')
        self.lc.InsertColumn(1, 'Anomaly for t')
        self.lc.InsertColumn(2, 'Energy')
        self.lc.InsertColumn(3, 'Momentum')
        self.lc.InsertColumn(4, 'Semi_major_axis')
        self.lc.InsertColumn(5, 'Semi-minor-axis')
        self.lc.InsertColumn(6, 'Period')
        self.lc.InsertColumn(7, 'T_0')
        self.lc.SetColumnWidth(1, 120)
        self.lc.SetColumnWidth(2, 150)
        self.lc.SetColumnWidth(3, 150)
        self.lc.SetColumnWidth(4, 120)
        self.lc.SetColumnWidth(5, 150)
        self.lc.SetColumnWidth(6, 120)
        self.lc.SetColumnWidth(7, 150)

        vbox2.Add(self.lc, 1, wx.EXPAND | wx.ALL, 3)

        hbox.Add(vbox0, 1, wx.EXPAND)
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

        self.lc.DeleteAllItems()

        day = int(str_day)
        month = int(str_month)
        year = int(str_year)

        current_date = datetime(year, month, day, hour=0, minute=0, second=0)

        import universe

        universe.processFrame()

        num_row = 0
        for planet in universe.planets:
            if draw_planets[planet.name]:
                self.lc.InsertStringItem(num_row, planet.name)
                info_list = planet.getInfo()

                num_col = 0
                for info in info_list:
                    self.lc.SetStringItem(num_row, num_col, info)
                    num_col += 1

                num_row += 1

    def OnCalculateDays(self, event):
        global current_date

        str_days = self.tc_days.GetValue()

        if not (str_days):
            return

        self.lc.DeleteAllItems()

        days = int(str_days)

        import universe

        num_row = 0
        for planet in universe.planets:
            if draw_planets[planet.name]:
                self.lc.InsertStringItem(num_row, planet.name)
                info_list = planet.getInfoDays(days)

                num_col = 0
                for info in info_list:
                    self.lc.SetStringItem(num_row, num_col, info)
                    num_col += 1

                num_row += 1

    def OnCalculateDate(self, event):
        import universe

        str_anomaly = self.tc_ecc.GetValue()
        str_planet = self.combo.GetValue()

        if not (str_anomaly and str_planet):
            self.result.SetLabel('')
            return

        anomaly = float(str_anomaly)

        for planet in universe.planets:
            if planet.name == str_planet:
                date, delta = planet.getDate(anomaly)
                break


        # self.result.SetLabel(str(date))
        if date.year < 1900:
            self.result.SetLabel(date.isoformat()+" ("+str(delta)+")")
        else:
            self.result.SetLabel(date.strftime("%d %B, %Y")+" ("+str(delta)+")")

    def OnRemove(self, event):
        index = self.lc.GetFocusedItem()
        self.lc.DeleteItem(index)

    def OnClose(self, event):
        self.Close()

    def OnClear(self, event):
        self.lc.DeleteAllItems()

    def SetVal(self, event):
        for planet in planets:
            draw_planets[planet] = self.cb[planet].GetValue()


class MyApp(wx.App):
    def OnInit(self):
        dia = MyDialog(None, -1, 'Solar System')
        dia.Show(True)
        return True
