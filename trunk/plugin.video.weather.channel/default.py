import urllib
import urllib2
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
from BeautifulSoup import BeautifulSoup
try:
    import json
except:
    import simplejson as json
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

__settings__ = xbmcaddon.Addon(id='plugin.video.weather.channel')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
wc_location = __settings__.getSetting('location')
cache = StorageServer.StorageServer("weather_channel", 24)
try:
    location = xbmc.getInfoLabel("Window(Weather).Property(Location)")
except:
    location = None


def make_request(url):
        try:
            headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                       'Referer' : 'http://www.weather.com'}
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
                
                
def get_location():
        url = 'http://xoap.weather.com/search/search?where=%s' %location
        soup = BeautifulSoup(make_request(url))
        wc_id = soup.loc['id']
        cache.set("location", location+" - "+wc_id)
                

def cache_maps(wc_location):
        url = 'http://www.weather.com/weather/map/%s' %wc_location
        soup = BeautifulSoup(make_request(url))
        maps = []
        for i in soup('option'):
            w_map = (i['value'], i.string)
            maps.append(w_map)
        videos = []
        for i in soup('a', attrs={'id' : 'lid2'}):
            href = i['href']
            name = i.string
            videos.append((href, name))
        cache.set("videos", json.dumps(videos))
        url = 'http://www.weather.com/maps/maptype/currentweatherusnational/usdopplerradar_large.html'
        soup = BeautifulSoup(make_request(url))
        for i in soup('option'):
            w_map = (i['value'], i.string)
            maps.append(w_map)
        cache.set("maps", json.dumps(maps))
    
 
def get_maps():
        for i in json.loads(cache.get("maps"))[1:]:
            url = i[0]
            name = i[1]
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=5&name="+urllib.quote_plus(name)
            liz=xbmcgui.ListItem(name, iconImage="icon", thumbnailImage=icon)
            liz.setInfo( type="Picture", infoLabels={ "Title": name} )
            liz.setProperty( "Fanart_Image", fanart )
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
    

def get_forcast_video():
        for i in json.loads(cache.get("videos")):
            url = i[0]
            name = i[1]
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=6&name="+urllib.quote_plus(name)
            liz=xbmcgui.ListItem(name, iconImage="icon", thumbnailImage=icon)
            liz.setInfo( type="Video", infoLabels={ "Title": name} )
            liz.setProperty( "Fanart_Image", fanart )
            liz.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
    

def categories():
        if not location is None:
            get_forcast_video()
        addDir('Weather Maps','',4,icon)
        addPlaylist('Play Top Stories','',3,icon)
        addDir('News','news',1,icon)
        addDir('Most Popular','popular',1,icon)
        addDir('Forecasts','forcast',1,icon)
        addDir('On TV','tv',1,icon)
        addDir('Living','living',1,icon)
        addDir('Storms','storms',1,icon)

        
def get_subcate(url):
        base_url = 'http://www.weather.com/weather/videos/news-41/top-stories-169/-/'
        soup = BeautifulSoup(make_request(base_url))
        if url == 'news':
            items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[0]('li')
        elif url == 'popular':
            items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[1]('li')
        elif url == 'forcast':
            items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[2]('li')
        elif url == 'tv':
            items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[3]('li')
        elif url == 'living':
            items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[4]('li')
        elif url == 'storms':
            items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[5]('li')
        for item in items:
            name = item('a')[0].string
            url = item('a')[0]['href'].split('-')[-2].split('/')[0]
            addDir(name,url,2,icon)


def index(url, play=False):
        url = ('http://wxdata.weather.com/wxdata/video/get.js?fn=getVideoCollection'
        '&cb=YAHOO.bcps.VideoService._handlePlaylistResponse&subcatid='+url+'&key=e88ca396-a740-102c-bafd-001321203584')
        link = make_request(url)
        data = json.loads(str(link)[48:-1])
        videos = data['clips']
        for video in videos:
            name = video['title']
            #videoId = video['bcVideoId']
            thumb = video['largethumb']
            desc = video['description']
            url = 'http://v.imwx.com/v/wxcom/'+video['sr56']+'.mov'
            if play:
                if play[:-5] in name.lower().replace(' ', '-'):
                    item = xbmcgui.ListItem(path=url)
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
                    return
                else: continue
            else:
                addLink(name,url,desc,thumb)

            
def play_latest():
        url = ('http://wxdata.weather.com/wxdata/video/get.js?fn=getVideoCollection'
        '&cb=YAHOO.bcps.VideoService._handlePlaylistResponse&subcatid=169&key=e88ca396-a740-102c-bafd-001321203584')
        link = make_request(url)
        data = json.loads(str(link)[48:-1])
        videos = data['clips']
        playlist = xbmc.PlayList(1)
        playlist.clear()
        for video in videos:
            name = video['title']
            #videoId = video['bcVideoId']
            thumb = video['largethumb']
            desc = video['description']
            url = 'http://v.imwx.com/v/wxcom/'+video['sr56']+'.mov'
            info = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
            playlist.add(url, info)
        play=xbmc.Player().play(playlist)

        
def get_images(wc_location, mapdest):
        url = 'http://www.weather.com/weather/map/%s?mapdest=%s' %(wc_location, mapdest)
        soup = BeautifulSoup(make_request(url))
        images = []
        try:
            mapregion = soup('a', attrs={'showanimation' : 'yes'})[0]['mapregion']
            for i in range(1, 6):
                img_url = 'http://image.weather.com/looper/archive/%s/%dL.jpg' %(mapregion, i)
                images.append(img_url)
        except:
            print 'No animation'
            try:
                img_url = soup('img', attrs={'name' : 'mapImg'})[0]['src']
                images.append(img_url)
            except:
                print '--- img_url error ---'
        print images
        clear_playlist = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Clear", "params": {"playlistid":2}, "id": 1}')
        items = []
        for i in images:
            item = '{ "jsonrpc": "2.0", "method": "Playlist.Add", "params": { "playlistid": 2 , "item": {"file": "%s"} }, "id": 1 }' %i
            add_item = items.append(str(item))
        add_playlist = xbmc.executeJSONRPC(str(items).replace("'",""))
        get_playlist = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.GetItems", "params": {"playlistid":2}, "id": 1}'))
        play = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.Open","params":{"item":{"playlistid":2}} }')


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


def addLink(name,url,description,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
        
        
def addDir(name,url,mode,iconimage):
        print(name,url,mode,iconimage)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

        
def addPlaylist(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


try:
    l_cache = cache.get("location")
    # check if location is set or has changed
    if (len(l_cache) == 0) or (not location in l_cache):
        print '--- caching location ---'
        get_location()
        # give storageserver a moment to finish
        xbmc.sleep(1000)
        l_cache = cache.get("location")
        wc_location = l_cache.split(' - ')[1]
        cache_maps(wc_location)
        print '---- cached location ----'
        print l_cache
except:
    pass

        
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
    categories()

elif mode==1:
    print ""+url
    get_subcate(url)
        
elif mode==2:
    print ""+url
    index(url)

elif mode==3:
    print ""
    play_latest()
    
elif mode==4:
    get_maps()
    
elif mode==5:
    get_images(wc_location, url)
    
elif mode==6:
    cat_id = url.split('/')[4].split('-')[-1]
    play = url.split('/')[-1][:9]
    index(cat_id, play)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
