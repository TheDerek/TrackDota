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

def get_teams_games(teams, games):
    gosuapi.get_teams(teams)
    gosuapi.get_games(teams, games)

if __name__ == "__main__":
    app = wx.App(False)

    frame = wx.Frame(None, title="Track Dota")
    frame.Center()
    frame.SetSize((800, 400))

    pinned_teams = []
    pinned_games = []
    teams = []
    games = []
    threading.Thread(target=get_teams_games, args=(teams, games)).start()


    nb = wx.Notebook(frame)
    list_teams = listings.ListTeams(nb, teams, games, pinned_teams)
    list_pinned_teams = listings.ListTeams(nb, pinned_teams, games, pinned_teams)
    list_games = listings.ListGames(nb, teams, games, pinned_games, pinned_teams)
    list_pinned_games = listings.ListGames(nb, teams, pinned_games, pinned_games, pinned_teams)
    nb.AddPage(list_teams, "All Teams")
    nb.AddPage(list_pinned_teams, "Pinned Teams")
    nb.AddPage(list_games, "Games")
    nb.AddPage(list_pinned_games, "Pinned Games")



    nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, on_open)
    nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, on_exit)

    frame.Show()
    app.MainLoop()