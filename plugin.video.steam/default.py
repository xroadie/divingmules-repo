import urllib
import urllib2
import re
import os
import cookielib
import xbmcplugin
import xbmcgui
import xbmcaddon
import StorageServer
from BeautifulSoup import BeautifulSoup

addon = xbmcaddon.Addon(id='plugin.video.steam')
home = xbmc.translatePath(addon.getAddonInfo('path'))
icon = os.path.join(home, 'icon.png')
fanart = 'http://www.deviantart.com/download/245134540/steam_logo_by_thegreatjug-d41y30s.png'
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
cache = StorageServer.StorageServer("Steam", 1)


def make_request(url):
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
                   'Referer' : 'http://store.steampowered.com/freestuff/videos'}
        try:
            req = urllib2.Request(url,None,headers)
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            if response.geturl() != url:
                print 'Redirect URL: %s' %response.geturl()
            return data
        except urllib2.URLError, e:
            print 'We failed to open "%s".' % url
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code


def cache_homepage():
        return make_request('http://store.steampowered.com/freestuff/videos')


def Categories():
        addDir('Newest Videos','',1,icon)
        addDir('By Genre', '', 5, icon)
        addDir('Most Watched (past 48 hours)','',3,icon)
        addDir('Search','',4,os.path.join(home, 'resources', 'search.png' ))


def Index(url):
        if url is None:
            data = cache.cacheFunction(cache_homepage)
            soup = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
        else:
            soup = BeautifulSoup(make_request(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        video_items = soup.findAll('div', attrs={'class' : "tab_video_desc"})
        for i in video_items:
            name = i('a')[0].string.encode('utf-8')
            video_url = i('a')[0]['href']
            video_id = video_url.split('?')[0].split('/')[-1]
            thumb = 'http://cdn.steampowered.com/v/gfx/apps/'+video_id+'/header.jpg'
            desc = i.getText('  ').strip().replace('  ', '\n')
            addLink(name,video_url,desc,thumb)
        page_url = None
        if url is None:
            try:
                page = soup.find('div', attrs={'id' : "tab_NewVideos_next"}).a['href']
                print 'Page: '+page
                navcontext = 'navcontext='+page.split('{')[1].split(':')[-1].split('"')[1]
                start = 'start='+str(int(page.split(',')[1])+10)
                page_url = 'http://store.steampowered.com/search/tab?style=video&'+navcontext+'&tab=NewVideos&'+start+'&count=10'
            except:
                print 'Page Exception'
        else:
            e = url.split('&start')
            start = int(e[1].split('&')[0][1:])+10
            page_url = e[0]+'&start='+str(start)+'&'+e[1].split('&')[1]
        if page_url:
            addDir('Next Page',page_url,1,os.path.join(home, 'resources', 'next.png'))


def mostWatched():
        data = cache.cacheFunction(cache_homepage)
        soup = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
        video_items = soup.findAll('div', attrs={'class' : "top_video_capsule"})
        for i in video_items:
            name = i('a')[1].string.encode('utf-8')
            video_url = i('a')[1]['href']
            video_id = video_url.split('?')[0].split('/')[-1]
            thumb = 'http://cdn.steampowered.com/v/gfx/apps/'+video_id+'/header.jpg'
            desc = i.getText('  ').strip().replace('  ', '\n')
            addLink(name,video_url,desc,thumb)


def getGenres():
        data = cache.cacheFunction(cache_homepage)
        soup = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
        genre_tab = (soup.find('div', attrs={'id': 'genre_flyout'})
                     ('div', attrs={'class': "popup_body popup_menu shadow_content"})[0]('a'))
        for i in genre_tab:
            name = i.string.strip()
            url = 'http://store.steampowered.com/search/?genre=%s&sort_by=&category1=999' %urllib.quote(name)
            addDir(name,url,4,icon)


def getVideos(url ,name):
        if name.startswith('#'):
            name = name.split(' : ' ,1)[1]
        data = make_request(url)
        if re.search('<h2>Please enter your birth date to continue:</h2>', data):
            print 'AGE CHECK'
            data = '/?ageDay=1&ageMonth=January&ageYear=1980&snr=1_agecheck_agecheck__age-gate'
            if '/app/' in url:
                url = url.replace('/app/','/agecheck/app/').split('?')[0]+data
            elif '/video/' in url:
                url = url.replace('/video/','/agecheck/video/').split('?')[0]+data
            data = make_request(url)

        vid_url = None
        filenames = re.findall('FILENAME: "(.+?)"', data)
        url_id = url.split('?')[0].split('/')[-1]
        for i in filenames:
            if url_id in i:
                vid_url = i
                break
        if not vid_url:
            videos = []
            pattern = "showGotSteamModal\('gotSteamModal', 'steam://run/(.+?)', '(.+?)'\)"
            match = re.findall(pattern, data)
            if len(match) > 0:
                for vid_id, title in match:
                    print (title, name)
                    if not title == name:
                        videos.append((vid_id, title))
                    else:
                        for i in filenames:
                            if vid_id in i:
                                vid_url = i
                                break
                    if vid_url:
                        break
            if not vid_url:
                if len(filenames) > 0:
                    print 'No name match, using first found filename'
                    vid_url = filenames[0]
                elif len(videos) > 0:
                    print 'No filenames, using videos[0]_id'
                    vid_url = 'http://media.steampowered.com/steam/apps/%s/movie940.flv' %videos[0][0]
        if not vid_url:
            print 're did not match: '+url
            print 'using url_id'
            vid_url = 'http://media.steampowered.com/steam/apps/%s/movie940.flv' %url_id
        item = xbmcgui.ListItem(path=vid_url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def Search(url):
        if url is None:
            searchStr = ''
            keyboard = xbmc.Keyboard(searchStr,'Search')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            newStr = keyboard.getText()
            if len(newStr) == 0:
                return
            url = 'http://store.steampowered.com/search/?term='+urllib.quote_plus(newStr)

        soup = BeautifulSoup(make_request(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        items = soup.find('div', attrs={'id' : "search_result_container"})('a')
        for i in items:
            if re.search('video', i['href']):
                name = i.h4.string.encode('utf-8')
                video_url = i['href']
                t = i('img')[1]['src']
                thumb = t.rsplit('/', 1)[0]+'/header.jpg'
                desc = i.p.string.strip()
                addLink(name, video_url, desc, thumb)

        page_items = soup.find('div', attrs={'class': "search_pagination_right"})('a')
        for i in page_items:
            if i.string == '>>':
                addDir('Next Page', i['href'], 4, os.path.join(home, 'resources', 'next.png' ))


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


def addLink(name,url,desc,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=2&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
        liz.setProperty("Fanart_Image", fanart)
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setProperty("Fanart_Image", fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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

elif mode==1:
    print ""
    Index(url)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

elif mode==2:
    print ""+url
    getVideos(url, name)

elif mode==3:
    print ""
    mostWatched()
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

elif mode==4:
    print ""
    Search(url)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

elif mode==5:
    print ""
    getGenres()

xbmcplugin.endOfDirectory(int(sys.argv[1]))