import urllib
import urllib2
import re
import os
import sys
import xbmcplugin
import xbmcgui
import xbmcaddon
from BeautifulSoup import BeautifulSoup
import resources.lib.common as common

__settings__ = xbmcaddon.Addon(id='plugin.video.nfl')
home = __settings__.getAddonInfo('path')
fanart = common.teams_['BAL']['fanart']
icon = common.teams_['BAL']['thumb']


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

        
def _categories():
        common.addDir('All Videos','http://www.baltimoreravens.com/Media/Video_Landing.aspx',36,icon,fanart)
        common.addDir('Game Day','http://www.baltimoreravens.com/Media/Video_Landing.aspx?q=Game+Day',36,icon,fanart)
        common.addDir('2010','http://www.baltimoreravens.com/Media/Video_Landing.aspx?q=2010',36,icon,fanart)
        common.addDir('Regular Season','http://www.baltimoreravens.com/Media/Video_Landing.aspx?q=Regular+Season',36,icon,fanart)
        common.addDir('NFL Network','http://www.baltimoreravens.com/Media/Video_Landing.aspx?q=NFL+Network',36,icon,fanart)
        common.addDir('Rave TV','http://www.baltimoreravens.com/Media/Video_Landing.aspx?q=Rave+TV',36,icon,fanart)
        
        
def _index(url):
        req = urllib2.Request(url)
        req.addheaders = [('Referer', 'http://www.baltimoreravens.com/Media/Video_Landing.aspx'),
                    ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, convertEntities=BeautifulSoup.HTML_ENTITIES)
        videos = soup.findAll('div', attrs={'class' : "videoThumbInfo"})
        for video in videos:
            name = video('a')[0]['title']
            thumb = video('img')[0]['src']
            url = thumb.replace('.tmb.jpg','.mp4')
            addLink(name,url,thumb)
            