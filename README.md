TrackDota
=========

An application for following your favourite Dota 2 professional teams and getting notified of their upcoming matches.

![](http://i.imgur.com/r0cqzSq.png)

Features
--------
At the moment Track Dota allows you to:
* Follow your favorite Dota 2 teams.
* Follow upcomming Dota 2 matches.
* Add any upcomming matches your followed teams are playing in to your followed matches que.

Download
--------
At the moment there is no packaged download or binaries. If you wish to try Track Dota in its current state you will need to use `git clone https://github.com/TheDerek/TrackDota.git` to download this repository and then run `python launcher.py`. See the requirements section below for more detail.

Requirements
------------
In order to run this program from source you will need to have the following installed:
* Python 2.7
* wxPython
* Beautiful Soup

TODO
----
Track Dota is in heavy in devolpment, and has major features to be added. These are as follows:
* Automatic saving of followed teams + matches.
* Notifications of when a followed game or team has started playing.
  * Links to watch said game.
  * Inbuilt [LiveStreamer](https://github.com/chrippa/livestreamer) support.
* Ability to follow Leagues and Tournaments .
