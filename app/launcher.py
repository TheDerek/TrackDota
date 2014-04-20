#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import listings
import gosuapi
import threading
import multiprocessing


def on_open(event):
    nb.CurrentPage.on_open()


def on_exit(event):
    nb.CurrentPage.on_exit()


def get_teams_games(teams, games, pages):
    print "Getting games + teams"
    gosuapi.get_teams(teams)
    gosuapi.get_games(teams, games)
    print "Games and teams got"

    for page in pages.values():
        page.refresh_data()


def get_games(teams, games, pages):
    print "Getting Games"
    gosuapi.get_games(teams, games)
    print "Games Got"
    for page in pages.values():
        page.refresh_data()


def on_reload(event):
    threading.Thread(target=get_games, args=(teams, games, pages)).start()



def on_quit(event):
    frame.Close()

if __name__ == "__main__":
    app = wx.App(False)

    frame = wx.Frame(None, title="Track Dota")
    frame.Center()
    frame.SetSize((800, 400))

    pinned_teams = []
    pinned_games = []
    teams = []
    games = []

    #Adding a toolbar
    toolbar = frame.CreateToolBar()
    refresh_tool = toolbar.AddLabelTool(wx.ID_REFRESH, 'Reload', wx.Bitmap('../assests/reload.png'))
    quit_tool = toolbar.AddLabelTool(wx.ID_EXIT, 'Quit', wx.Bitmap('../assests/exit.png'))
    toolbar.Realize()

    nb = wx.Notebook(frame)
    pages = {}
    pages["teams"] = listings.ListTeams(nb, teams, games, pinned_teams, pages)
    pages["teams_pinned"] = listings.ListTeams(nb, pinned_teams, games, pinned_teams, pages)
    pages["games"] = listings.ListGames(nb, teams, games, pinned_games, pinned_teams, pages)
    pages["games_pinned"] = listings.ListGames(nb, teams, pinned_games, pinned_games, pinned_teams, pages)

    nb.AddPage(pages["teams"], "All Teams")
    nb.AddPage(pages["teams_pinned"], "Pinned Teams")
    nb.AddPage(pages["games"], "Games")
    nb.AddPage(pages["games_pinned"], "Pinned Games")

    frame.Bind(wx.EVT_TOOL, on_quit, quit_tool)
    frame.Bind(wx.EVT_TOOL, on_reload, refresh_tool)
    nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, on_open)
    nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, on_exit)

    threading.Thread(target=get_teams_games, args=(teams, games, pages)).start()

    frame.Center()
    frame.Show()
    app.MainLoop()




