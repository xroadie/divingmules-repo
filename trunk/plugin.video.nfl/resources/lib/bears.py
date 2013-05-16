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
fanart = common.teams_['CHI']['fanart']
icon = common.teams_['CHI']['thumb']
headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
           'Referer' : 'http://www.chicagobears.com/'}


def _categories():
        common.addDir('Most Recent','http://www.chicagobears.com/multimedia/MostRecentArchives.asp',41,icon,fanart)
        common.addDir('CBTV','http://www.chicagobears.com/multimedia/CBTVArchives.asp',41,icon,fanart)
        common.addDir('Game Highlights','http://www.chicagobears.com/multimedia/HighlightsArchives.asp',41,icon,fanart)
        common.addDir('Features','http://www.chicagobears.com/multimedia/FeaturesArchives.asp',41,icon,fanart)
        common.addDir('Press Conferences','http://www.chicagobears.com/multimedia/PressArchives.asp',41,icon,fanart)
        common.addDir('Bears History','http://www.chicagobears.com/multimedia/BearsArchives.asp',41,icon,fanart)
        common.addDir('Staley','http://www.chicagobears.com/multimedia/StaleyArchives.asp',41,icon,fanart)
        common.addDir('Community','http://www.chicagobears.com/multimedia/CommunityArchives.asp',41,icon,fanart)
        common.addDir('CB Network','http://www.chicagobears.com/multimedia/CBNetworkArchive.asp',41,icon,fanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def _index(url):
        soup = BeautifulSoup(common.make_request(url, headers))
        videos = soup.find('ul', attrs={'class' : "list_mod"})('li')
        for video in videos:
            name = video('a')[0].string
            url = video('a')[0]['href'].split('=')[1].split('&')[0]
            date = video('span')[0].string
            thumb = 'http://assets.chicagobears.com/uploads/multimedia/stills/teasers/'+url+'.jpg'
            common.addLink(name+' - '+date,url,thumb,'',date,42,fanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def _getVideoUrl(url):
        url = 'http://www.chicagobears.com/includes/ajax/10_multimedia_details.asp?mm_file_id='+url
        soup = BeautifulSoup(common.make_request(url, headers))
        item = soup('input', attrs={'id' : 'embed_code'})[0]['value']
        Playpath = ' Playpath=mp4:'+BeautifulSoup(item)('param', attrs={'name' : 'flashvars'})[0]['value'].split('featureVideo=mp4:')[1].split('&')[0]
        pageUrl  = ' pageUrl=http://www.chicagobears.com/multimedia/'
        swfUrl = ' swfUrl='+BeautifulSoup(item)('param', attrs={'name' : 'movie'})[0]['value']
        tcUrl = 'rtmp://69.31.132.207:1935/ondemand?_fcs_vhost=cp52544.edgefcs.net'
        url = tcUrl+swfUrl+Playpath+pageUrl
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)