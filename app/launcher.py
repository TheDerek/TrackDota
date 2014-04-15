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
    nb.AddPage(listings.ListTeams(nb, teams, games, pinned_teams), "All Teams")
    nb.AddPage(listings.ListTeams(nb, pinned_teams, games, pinned_teams), "Pinned Teams")
    nb.AddPage(listings.ListGames(nb, teams, games, pinned_games, pinned_teams), "Games")
    nb.AddPage(listings.ListGames(nb, teams, pinned_games, pinned_games, pinned_teams), "Pinned Games")

    nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, on_open)
    nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, on_exit)

    frame.Show()
    app.MainLoop()