import urllib
import urllib2
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
from BeautifulSoup import BeautifulSoup

__settings__ = xbmcaddon.Addon(id='plugin.video.espn.go')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'resources/next.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
bitrate = __settings__.getSetting('bitrate')
base_url = ('http://espn.go.com/video/format/libraryPlaylist?categoryid=%s&pageNum=0&sortBy='
            '&assetURL=http://assets.espn.go.com&module=LibraryPlaylist&pagename=vhub_index')

def Categories():
        addPlaylist('Play The Latest', base_url %'2378529', icon, 4)
        addDir('The Latest', base_url %'2378529', '', 1)
        addDir('Sports Center', base_url %'5595394', icon, 1)
        addDir('NFL', base_url %'2459789', icon, 1)
        addDir('College Football', base_url %'2564308', icon, 1)
        addDir('MLB', base_url %'2521705', icon, 1)
        addDir('NBA', base_url %'2459788', icon, 1)
        addDir('NASCAR ', base_url %'2492290', icon, 1)
        addDir('Golf', base_url %'2630020', icon, 1)
        addDir('NHL', base_url %'2459791', icon, 1)
        addDir('MMA', base_url %'2881270', icon, 1)
        addDir('Boxing', base_url %'2491554', icon, 1)
        addDir('Racing', base_url %'2755879', icon, 1)
        addDir('College Hoops', base_url %'2459792', icon, 1)
        addDir("Women's Basketball", base_url %'3414465', icon, 1)
        addDir('Shows', '', icon, 3)


def Shows():
        addDir('E:60', base_url %'3060647', icon, 1)
        addDir('The Next Round', base_url %'5037484', icon, 1)
        addDir('SportsNation', base_url %'5092967', icon, 1)
        addDir('Homecoming ', base_url %'4083827', icon, 1)
        addDir('Mike and Mike', base_url %'2850689', icon, 1)
        addDir('Outside the Lines', base_url %'3286128', icon, 1)
        addDir('Road Trip', base_url %'3619786', icon, 1)
        addDir('Page 2', base_url %'2494144', icon, 1)
        addDir('ESPNU', base_url %'2491548', icon, 1)


def make_request(url):
        try:
            headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                       'Referer' : 'http://espn.go.com/video/'}
            req = urllib2.Request(url,None,headers)
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            return data
        except urllib2.URLError, e:
            print 'We failed to open "%s".' % url
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code


def getVideos(url, play=False):
        soup = BeautifulSoup(make_request(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        videos = soup.findAll('div', attrs={'class' : "video-cell"})
        if play:
            playlist = xbmc.PlayList(1)
            playlist.clear()
        for video in videos:
            name = video.h5.string
            Pageurl = video.a['href']
            thumb = video.img['src']
            item = thumb.split('/')[-1].split('_thumdnail')[0].replace('.jpg','')
            link = ('http://vod.espn.go.com/motion/%s/%s/%s.smil?FLVPlaybackVersion=2.1'
            %(thumb.split('/')[-3], thumb.split('/')[-2], item))
            if play:
                try:
                    v_url = getSmil(link)
                    info = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                    playlist.add(v_url, info)
                except:
                    print '--- smil error ----'
                    continue
            else:
                addLink(name,link,thumb,2)
        try:
            page_string = soup('div', attrs={'class' : "page-numbers"})[0].string
            if (not int(page_string.split(' ')[0]) >= int(page_string.split(' ')[-1])):
                next_page = 'pageNum=%s&' %str(int(url.split('pageNum=')[1].split('&')[0]) + 1)
                page_url = url.split('pageNum=')[0]+next_page+url.split('pageNum=')[-1].split('&', 1)[1]
                if play:
                    mode = 4
                else:
                    mode = 1
                addDir('Next Page', page_url, nexticon, mode)
        except:
            pass
        if play:
            xbmc.Player().play(playlist)


def getSmil(url):
        soup = BeautifulSoup(make_request(url))
        if bitrate == "448k":
            url = soup.meta['base']+soup('video')[0]['src'].replace('mp4:','')
        if bitrate == "948k":
            url = soup.meta['base']+soup('video')[1]['src'].replace('mp4:','')
        if bitrate == "1464k":
            url = soup.meta['base']+soup('video')[2]['src'].replace('mp4:','')
        if bitrate == "2096k":
            url = soup.meta['base']+soup('video')[3]['src'].replace('mp4:','')
        if bitrate == "2896k":
            url = soup.meta['base']+soup('video')[4]['src'].replace('mp4:','')
        return url


def setUrl(url):
        try:
            url = getSmil(url)
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        except:
            print '--- smil error ----'


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]
        return param


def addLink(name,url,iconimage,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty( "Fanart_Image", fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDir(name,url,iconimage,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart)
        contextMenu = [('Play All','XBMC.Container.Update(%s?url=%s&mode=4)' %(sys.argv[0], urllib.quote_plus(url)))]
        liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addPlaylist(name,url,iconimage,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


params=get_params()
url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None:
    print ""
    Categories()

if mode==1:
    print""
    getVideos(url)

if mode==2:
    print""
    setUrl(url)

if mode==3:
    print""
    Shows()

if mode==4:
    print""
    getVideos(url, True)

xbmcplugin.endOfDirectory(int(sys.argv[1]))