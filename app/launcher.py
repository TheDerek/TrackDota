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
    gosuapi.get_teams(teams)
    gosuapi.get_games(teams, games)

    for page in pages:
        page.refresh_data()


if __name__ == "__main__":
    app = wx.App(False)

    frame = wx.Frame(None, title="Track Dota")
    frame.Center()
    frame.SetSize((800, 400))

    pinned_teams = []
    pinned_games = []
    teams = []
    games = []

    nb = wx.Notebook(frame)
    pages = []
    pages.append(listings.ListTeams(nb, teams, games, pinned_teams))
    pages.append(listings.ListTeams(nb, pinned_teams, games, pinned_teams))
    pages.append(listings.ListGames(nb, teams, games, pinned_games, pinned_teams))
    pages.append(listings.ListGames(nb, teams, pinned_games, pinned_games, pinned_teams))

    nb.AddPage(pages[0], "All Teams")
    nb.AddPage(pages[1], "Pinned Teams")
    nb.AddPage(pages[2], "Games")
    nb.AddPage(pages[3], "Pinned Games")

    nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, on_open)
    nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, on_exit)

    threading.Thread(target=get_teams_games, args=(teams, games, pages)).start()

    frame.Show()
    app.MainLoop()