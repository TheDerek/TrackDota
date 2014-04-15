import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import operator
import gosuapi
import time
import threading


class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
                             style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL)
        ListCtrlAutoWidthMixin.__init__(self)


    def getSelectedIndices(self, state=wx.LIST_STATE_SELECTED):
        indices = []
        lastFound = -1
        while True:
            index = self.GetNextItem(
                lastFound,
                wx.LIST_NEXT_ALL,
                state,
            )
            if index == -1:
                break
            else:
                lastFound = index
                indices.append(index)
        return indices


def list_refresh(function, interval):
    previous_time = time.clock()
    while True:
        current_time = time.clock()
        if current_time - previous_time > interval:
            function()
            previous_time = time.clock()


class ListTeams(wx.Panel):
    def __init__(self, parent, team_list, game_list, pinned_teams):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.team_list = team_list
        self.pinned_teams = pinned_teams
        self.game_list = game_list
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scroll_position = 0

        self.list = AutoWidthListCtrl(self)
        self.list.InsertColumn(0, "Following")
        self.list.InsertColumn(1, "Rank", format=wx.LIST_FORMAT_RIGHT)
        self.list.InsertColumn(2, "Country")
        self.list.InsertColumn(3, "Team Name")
        self.list.InsertColumn(4, "Status")

        self.populate_list()
        #threading.Thread(target=list_refresh, args=(self.populate_list, 5)).start()

        self.list.Show(True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, self.list)

        self.sizer.Add(self.list, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(self.sizer)

    def on_select(self, event):
        row = event.GetIndex()
        selected_team = self.team_list[len(self.team_list) - 1 - event.GetIndex()]
        self.list.SetItemState(event.GetIndex(), 0, wx.LIST_STATE_SELECTED)
        # self.list.SetItemState(event.GetIndex(), 0, wx.LIST_STATE_FOCUSED)

        if selected_team in self.pinned_teams:
            self.pinned_teams.remove(selected_team)
            self.list.SetStringItem(row, 0, "")
            if self.pinned_teams is self.team_list:
                self.list.DeleteItem(row)

        else:
            self.pinned_teams.append(selected_team)
            self.list.SetStringItem(row, 0, "Following")

    def populate_list(self):
        self.list.DeleteAllItems()

        if len(self.team_list) > 0:
            self.pinned_teams.sort(key=operator.itemgetter('irank'))
            self.pinned_teams.reverse()

            for team in self.team_list:
                pinned = ""

                if team in self.pinned_teams:
                    pinned = "Following"

                pos = self.list.InsertStringItem(0, pinned)
                self.list.SetStringItem(pos, 1, team["rank"])
                self.list.SetStringItem(pos, 2, team["country"])
                self.list.SetStringItem(pos, 3, team["name"])

                next_match = gosuapi.get_next_match(team["name"], self.team_list, self.game_list)
                against = None
                string = "No scheduled matches"
                if next_match is not None:

                    against = next_match['team2']
                    if next_match['team1'] != team["name"]:
                        against = next_match['team1']

                    string = "Playing against " + against + " in " + next_match["time"]
                    if next_match["time"] == "Now":
                        string = "Playing against " + against + " " + next_match["time"]

                self.list.SetStringItem(pos, 4, string)


            # Have to set width after items have been added
            self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
            self.list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
            self.list.SetColumnWidth(3, wx.LIST_AUTOSIZE)
            self.sizer.RecalcSizes()

    def on_open(self):
        self.populate_list()
        self.set_scroll_pos(self.scroll_position)

    def on_exit(self):
        self.scroll_position = self.get_scroll_pos()

    def get_scroll_pos(self):
        list_total = self.list.GetItemCount()
        list_top = self.list.GetTopItem()
        list_pp = self.list.GetCountPerPage()
        list_bottom = min(list_top + list_pp, list_total - 1)
        return list_bottom

    def set_scroll_pos(self, pos):
        self.list.EnsureVisible((pos - 1))


class ListGames(wx.Panel):
    def __init__(self, parent, team_list, game_list, pinned_games, pinned_teams):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.team_list = team_list
        self.game_list = game_list
        self.pinned_games = pinned_games
        self.pinned_teams = pinned_teams
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scroll_position = 0

        self.list = AutoWidthListCtrl(self)
        self.list.InsertColumn(0, "Following")
        self.list.InsertColumn(1, "Time")
        self.list.InsertColumn(2, "Team 1")
        self.list.InsertColumn(3, "     ", format=wx.LIST_FORMAT_CENTRE) # for the "Vs."
        self.list.InsertColumn(4, "Team 2")
        self.populate_list()
        self.list.Show(True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, self.list)

        self.sizer.Add(self.list, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(self.sizer)

    def on_select(self, event):
        row = event.GetIndex()
        selected_game = self.game_list[len(self.game_list) - 1 - event.GetIndex()]
        self.list.SetItemState(event.GetIndex(), 0, wx.LIST_STATE_SELECTED)
        # self.list.SetItemState(event.GetIndex(), 0, wx.LIST_STATE_FOCUSED)

        if selected_game in self.pinned_games:
            self.pinned_games.remove(selected_game)
            self.list.SetStringItem(row, 0, "")
            if self.pinned_games is self.game_list:
                self.list.DeleteItem(row)

        else:
            self.pinned_games.append(selected_game)
            self.list.SetStringItem(row, 0, "Following")

    def populate_list(self):
        self.list.DeleteAllItems()

        if len(self.game_list) > 0:
            #self.pinned_games.sort(key=operator.itemgetter('rank'))

            self.game_list.sort(key=operator.itemgetter('position'))
            self.game_list.reverse()


            for game in self.game_list:
                pinned = ""

                if self.game_list != self.pinned_games:
                    if gosuapi.get_team(game["team1"], self.team_list) in self.pinned_teams:
                        self.pinned_games.append(game)

                    if gosuapi.get_team(game["team2"], self.team_list) in self.pinned_teams:
                        self.pinned_games.append(game)

                if game in self.pinned_games:
                    pinned = "Following"

                pos = self.list.InsertStringItem(0, pinned)
                self.list.SetStringItem(pos, 1, game["time"])
                self.list.SetStringItem(pos, 2, game["team1"])
                self.list.SetStringItem(pos, 3, "Vs.")
                self.list.SetStringItem(pos, 4, game["team2"])

            # Have to set width after items have been added
            self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
            self.list.SetColumnWidth(3, wx.LIST_AUTOSIZE)
            self.sizer.RecalcSizes()




    def on_open(self):
        self.populate_list()
        self.set_scroll_pos(self.scroll_position)

    def on_exit(self):
        self.scroll_position = self.get_scroll_pos()

    def get_scroll_pos(self):
        list_total = self.list.GetItemCount()
        list_top = self.list.GetTopItem()
        list_pp = self.list.GetCountPerPage()
        list_bottom = min(list_top + list_pp, list_total - 1)
        return list_bottom

    def set_scroll_pos(self, pos):
        self.list.EnsureVisible((pos - 1))


