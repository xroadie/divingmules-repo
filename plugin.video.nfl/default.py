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
import resources.lib.common as common
import resources.lib.ravens as ravens
import resources.lib.bears as bears
import resources.lib.teams as teams

__settings__ = xbmcaddon.Addon(id='plugin.video.nfl')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
cdn = __settings__.getSetting('cdn')
bitrate = __settings__.getSetting('bitrate')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
next = xbmc.translatePath( os.path.join( home, 'resources','icons','next.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )


def categories():
        common.addDir('All Videos','http://www.nfl.com/videos/nfl-videos',1,icon, fanart)
        common.addDir('Game Highlights','http://www.nfl.com/videos/nfl-game-highlights',1,icon, fanart)
        common.addDir('Shows','',2,icon, fanart)
        common.addDir('Teams','',2,icon, fanart)
        common.addDir('Channels','',2,icon, fanart)
        common.addDir('Events','',2,icon, fanart)
        common.addDir('Search','',14,xbmc.translatePath( os.path.join( home, 'resources','icons','search.png' ) ), fanart)
        common.addDir('Team Sites','',6,icon, fanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        		

def teamSite():
        for i in common.teams_.keys():
            if not common.teams_[i]['mode'] == '':
                title = '%s %s' %(common.teams_[i]['city'], common.teams_[i]['nickname'])
                common.addDir(title,'',common.teams_[i]['mode'],common.teams_[i]['thumb'],fanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def getSubCategories(name):
        shows = {'NFL AM' : 'http://www.nfl.com/videos/nfl-am',
                 'NFL Total Access' : 'http://www.nfl.com/videos/nfl-network-total-access',
                 'NFL GameDay' : 'http://www.nfl.com/videos/nfl-network-gameday',
                 'Playbook' : 'http://www.nfl.com/videos/nfl-network-playbook',
                 'NFL Top Ten' : 'http://www.nfl.com/videos/nfl-network-top-ten',
                 'Around the League' : 'http://www.nfl.com/videos/nfl-network-around-the-league',
                 'Fantasy' : 'http://www.nfl.com/videos/nfl-fantasy',
                 'FantasyTeam Previews' : 'http://www.nfl.com/videos/nfl-fantasy-team-by-team',
                 'NFL RedZone' : 'http://www.nfl.com/videos/nfl-redzone-videos',
                 'A Football Life' : 'http://www.nfl.com/videos/a-football-life',
                 'The Coaches' : 'http://www.nfl.com/videos/nfl-network-the-coaches',
                 'Game of the Week' : 'http://www.nfl.com/videos/nfl-films-game-of-the-week',
                 "America's Game" : 'http://www.nfl.com/videos/nfl-films-americas-game',
                 # 'Top 100 Players of' : 'http://www.nfl.com/videos/nfl-top100-2012',
                 'No Huddle': 'http://www.nfl.com/videos/nfl-network-no-huddle',
                 'NFL Films Presents' : 'http://www.nfl.com/videos/nfl-films-presents',
                 'Sound FX' : 'http://www.nfl.com/videos/nfl-films-sound-efx',
                 'Anatomy of a Play' : 'http://www.nfl.com/videos/nfl-films-anatomy-of-a-play',
                 'Hard Knocks' : 'http://www.nfl.com/videos/nfl-network-hard-knocks',
                 'Path to the Draft' : 'http://www.nfl.com/videos/nfl-network-path-to-the-draft'}


        channels = {'Countdowns' : 'http://www.nfl.com/videos/nfl-countdowns',
                    'Top 5 Catches' : 'http://www.nfl.com/videos/nfl-top-5-catches',
                    "Can't-Miss Plays" : 'http://www.nfl.com/videos/nfl-cant-miss-plays',
                    'Drive Of The Week' : 'http://www.nfl.com/videos/nfl-drive-of-the-week',
                    'The Season' : 'http://www.nfl.com/videos/nfl-the-season',
                    'Interviews' : 'http://www.nfl.com/videos/nfl-player-interviews',
                    'Game Previews' : 'http://www.nfl.com/videos/nfl-game-previews',
                    'Video Diaries' : 'http://www.nfl.com/videos/nfl-video-diaries',
                    'Never Say Never' : 'http://www.nfl.com/videos/never-say-never-training-camp',
                    'Rookie Spotlight' : 'http://www.nfl.com/videos/nfl-rookie-of-the-week',
                    'Air & Ground NF' : 'http://www.nfl.com/videos/nfl-air-and-ground-players-of-the-week',
                    'X-Factors' : 'http://www.nfl.com/videos/nfl-playoff-x-factors',
                    'Hunger Stories' : 'http://www.nfl.com/videos/hunger-stories',
                    'Pepsi Audible' : 'http://www.nfl.com/videos/nfl-pepsi-audible',
                    'Locker Room MVPs' : 'http://www.nfl.com/videos/nfl-locker-room-mvps',
                    'Everything to Prove' : 'http://www.nfl.com/videos/nfl-everything-to-prove',
                    'The Shame Report' : 'http://www.nfl.com/videos/the-shame-report',
                    'On The Beat' : 'http://www.nfl.com/videos/nfl-on-the-beat',
                    'Movie Trailers' : 'http://www.nfl.com/videos/movie-trailers',
                    'Ultimate Audio' : 'http://www.nfl.com/videos/nfl-ultimate-audio',
                    'Tools for Victory' : 'http://www.nfl.com/videos/tools-for-victory',
                    'First Draft' : 'http://www.nfl.com/videos/nfl-first-draft',
                    'All-Access Facility' : 'http://www.nfl.com/videos/nfl-facility-tours',
                    'NFL Rush' : 'http://www.nfl.com/videos/nfl-rush',
                    'NFL Gives Back' : 'http://www.nfl.com/videos/nfl-gives-back'}

        events = {'Draft' : 'http://www.nfl.com/videos/nfl-draft',
                  'Minicamps' : 'http://www.nfl.com/videos/nfl-mini-camps',
                  '2012 Super Bowl Commercials' : 'http://www.nfl.com/videos/nfl-super-bowl-commercials',
                  'Training Camps' : 'http://www.nfl.com/videos/nfl-training-camps',
                  'Hall of Fame' : 'http://www.nfl.com/videos/nfl-hall-of-fame',
                  'Preseason' : 'http://www.nfl.com/videos/nfl-preseason',
                  'Kickoff' : 'http://www.nfl.com/videos/nfl-kickoff',
                  'Thanksgiving' : 'http://www.nfl.com/videos/nfl-thanksgiving',
                  'Thursday Night Football' : 'http://www.nfl.com/videos/nfl-thursday-night-football',
                  'Playoffs' : 'http://www.nfl.com/videos/nfl-playoffs',
                  'Super Bowl' : 'http://www.nfl.com/videos/nfl-super-bowl',
                  'Pro Bowl' : 'http://www.nfl.com/videos/nfl-pro-bowl',
                  'Free Agency' : 'http://www.nfl.com/videos/nfl-free-agency',
                  'Combine' : 'http://www.nfl.com/videos/nfl-combine',
                  'Senior Bowl' : 'http://www.nfl.com/videos/nfl-senior-bowl',
                  'International Series' : 'http://www.nfl.com/videos/nfl-international-series',
                  'Rookie Symposium' : 'http://www.nfl.com/videos/nfl-rookie-symposium',
                  'NFL Honors' : 'http://www.nfl.com/videos/nfl-honors'}

        if name == 'Shows':
            for i in shows.keys():
                common.addDir(i, shows[i], 1, icon, fanart)
        elif name == 'Channels':
            for i in channels.keys():
                common.addDir(i, channels[i], 1, icon, fanart)
        elif name == 'Events':
            for i in events.keys():
                common.addDir(i, events[i], 1, icon, fanart)
        elif name == 'Teams':
            for i in common.teams_.keys():
                title = '%s %s' %(common.teams_[i]['city'], common.teams_[i]['nickname'])
                url = 'http://www.nfl.com/videos/'+title.replace('.','').replace(' ', '-').lower()
                thumb = common.teams_[i]['thumb']
                common.addDir(title, url, 1, thumb, fanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def index(url,name):
        if not name=='All Videos':
            if not re.search('page=', url):
                common.addPlaylist('Play Featured Videos',url,4,'',fanart)

        soup = BeautifulSoup(common.make_request(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        videos = soup.find('ul', attrs={'id' : "video-list-items"})('li')
        for video in videos:
            name = video('h3')[0]('a')[0].string
            link = video('h3')[0]('a')[0]['href'].split('/')[3]
            thumb = video('img')[0]['src'].split('_video_thumbnail_')[0]+'_video_rhr_210.jpg'
            try:
                desc = video('p')[1].string+' \n  '+video('p')[0].string
            except:
                desc = video('p')[0].string
            duration = video('div')[-1].string.replace('\n','').replace('\t','')
            common.addLink(name,link,thumb,duration,desc,3,fanart)
        try:
            page = soup.find('div', attrs={'id' : "video-list-pagination"})('a')[-1]['href']
            if not page == '?page=3':
                common.addDir('Next Page',url.split('?')[0]+page,1,next,fanart)
            else:
                common.addDir('Next Page','http://www.nfl.com/ajax/videos/v2?batchNum=1&channelId='+url.split('/')[-1].split('?')[0],5,next,fanart)
        except:
            pass
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def getPage3(url):
        data = json.loads(common.make_request(url))
        videos = data['videos']
        for video in videos:
            url = video['videoCMSID']
            name = video['briefHeadline']
            thumb = video['xSmallImage'].split('_video_thumbnail_')[0]+'_video_rhr_210.jpg'
            desc = video['captionBlurb']
            duration = video['runTime'][:-3]
            common.addLink(name,url,thumb,duration,desc,3,fanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def getFeaturedVideos(url):
        soup = BeautifulSoup(common.make_request(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        try:
            videos = soup.find('div', attrs={'id' : "featured-videos-carousel"})('ul')[0]('h3')
        except:
            videos = soup.findAll('ul', attrs={'class' : "list-items"})[0]('h3')
        playlist = xbmc.PlayList(1)
        playlist.clear()
        for video in videos:
            name = video('a')[0].string
            url = video('a')[0]['href'].split('/')[3]
            print'URL: '+url
            url = getVideoUrl(url)
            info = xbmcgui.ListItem(name)
            playlist.add(url, info)
        play=xbmc.Player().play(playlist)


def search():
        searchStr = ''
        keyboard = xbmc.Keyboard(searchStr,'Search')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        newStr = keyboard.getText().replace(' ','+')
        if len(newStr) == 0:
            return
        url = 'http://search.nfl.com/videos/search-results?quickSearch='+newStr
        soup = BeautifulSoup(common.make_request(url))
        videos = soup('li')
        for video in videos:
            try:
                name = video('a')[0]['title']
                url = video('a')[0]['href'].split('id=')[1]
                thumb = video('a')[0]('img')[0]['src'].split('_video_thumbnail_')[0]+'_video_rhr_210.jpg'
                desc = video('p')[0].string
                duration = video('p')[1].string
                common.addLink(name,url,thumb,duration,desc,3,fanart)
            except:
                pass
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def getVideoUrl(url):
        url = 'http://www.nfl.com/static/embeddablevideo/'+url+'.json'
        data = json.loads(common.make_request(url))
        bitrate = __settings__.getSetting('bitrate')
        if data['status'] == 'EXPIRED':
            xbmc.executebuiltin("XBMC.Notification(NFL,Sorry this video is expired.,5000,"+icon+")")
            return
        if len(data['cdnData']['bitrateInfo']) > 0:
            for i in data['cdnData']['bitrateInfo']:
                if bitrate in i['path']:
                    uri = i['path']
                    break
                else: uri = None
            if uri is None:
                uri = data['cdnData']['bitrateInfo'][-1]['path']
        else:
            print '--- No bitrateInfo ---'
            class HeadRequest(urllib2.Request):
                    def get_method(self):
                        return "HEAD"
            # print data
            cdn_ = 'http://l.video.nfl.com/'
            uri = data['cdnData']['uri']
            if bitrate == "3200k":
                uri = uri.replace(uri.split('_', -1)[-1], '3200k.mp4')
                try:
                    response = urllib2.urlopen(HeadRequest(cdn_+uri))
                    print response.info()
                except:
                    bitrate = "2000k"
                    uri = None
                    print '-- trying lower bitrate --'
            if bitrate == "2000k":
                uri = uri.replace(uri.split('_', -1)[-1], '2000k.mp4')
                try:
                    response = urllib2.urlopen(HeadRequest(cdn_+uri))
                    print response.info()
                except:
                    bitrate = "1200k"
                    uri = None
                    print '-- trying lower bitrate --'
            if bitrate == "1200k":
                uri = uri.replace(uri.split('_', -1)[-1], '1200k.mp4')
                try:
                    response = urllib2.urlopen(HeadRequest(cdn_+uri))
                    print response.info()
                except:
                    bitrate = "700k"
                    uri = None
                    print '-- trying lower bitrate --'
            # elif bitrate == "700k":
                # uri = uri.replace(uri.split('_', -1)[-1], '700k.mp4')
            if uri is None:
                uri = data['cdnData']['uri']
        if uri.startswith('/'):
            uri = uri[1:]

        cdn0 = 'http://l.video.nfl.com/'           #limelightProg 700k only
        cdn1 ='http://vod.hstream.video.nfl.com/'  #akamaiHTTP  streams seem to end early
        cdn2 = 'http://a.video.nfl.com/'           #akamaiProg
        cdn3 = 'rtmp://cp86372.edgefcs.net/ondemand'    #pathprefix="vod/gallery/" akamaiRTMP
        cdn4 = 'rtmp://nfl.fcod.llnwd.net/a2290 app=a2290'  # seems to only work at 700k   #pathprefix="vod/"  limelightRTMP
        liveCDN = 'rtmp://cp37426.live.edgefcs.net/live'
        
        swf_url = ' swfUrl=http://i.nflcdn.com/static/video/latest/js/nfl-video-swf/assets/player.swf?v=2f6649c'
        if  __settings__.getSetting('cdn') == "limelight-RTMP 700k only":
            if not re.search('.mp4', uri):
                playpath = ' Playpath=vod/'
            else:
                playpath = ' Playpath=mp4:vod/'
            url = cdn4+playpath+uri+swf_url
        # cdn3 "RTMP_ReadPacket, failed to read RTMP packet header"
        elif  __settings__.getSetting('cdn') == "akamai-RTMP":
            if not re.search('.mp4', uri):
                playpath = ' Playpath=vod/'
            else:
                playpath = ' Playpath=mp4:vod/'
                swf_url +=' swfVfy=1'
            url = cdn3+playpath+uri+swf_url
        elif  __settings__.getSetting('cdn') == "limelightProg-HTTP 700k only":
            url = cdn0+uri
        elif  __settings__.getSetting('cdn') == "akamai-HTTP":
            values = {'700k': '1',
                      '1200k': '2',
                      '2000k': '3',
                      '3200k': '4'}
            url = '%s%s_,50,70,120,200,320,0k.mp4.csmil/bitrate=%s?v=2.7.6&seek=0' %(cdn1, uri.rsplit('_', 1)[0], values[bitrate])
        # ERROR: CCurlFile::CReadState::Open, didn't get any data from stream
        elif  __settings__.getSetting('cdn') == "akamaiProg-HTTP":
            url = cdn2+uri
        print "Resolved URL -----> "+url
        return url


def setUrl(url):
        url = getVideoUrl(url)
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


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
try:
    fanart=urllib.unquote_plus(params["fanart"])
except:
    pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
    print ""
    categories()

elif mode==1:
    index(url,name)

elif mode==2:
    getSubCategories(name)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

elif mode==3:
    setUrl(url)

elif mode==4:
    getFeaturedVideos(url)

elif mode==5:
    getPage3(url)

elif mode==6:
    teamSite()
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

elif mode==7:
    common._index(url,fanart)

elif mode==8:
    common._getVideoUrl(url)

elif mode==9:
    teams.cardinals()

elif mode==10:
    teams.bengals()

elif mode==11:
    teams.buccaneers()

elif mode==12:
    teams.browns()

elif mode==13:
    teams.chargers()

elif mode==14:
    search()

elif mode==15:
    pass

elif mode==16:
    pass

elif mode==17:
    pass

elif mode==18:
    teams.lions()

elif mode==19:
    teams.fortyniners()

elif mode==20:
    teams.giants()

elif mode==21:
    teams.texans()

elif mode==22:
    teams.chiefs()

elif mode==23:
    teams.jets()

elif mode==24:
    teams.saints()

elif mode==25:
    teams.packers()

elif mode==26:
    teams.panthers()

elif mode==27:
    teams.patriots()

elif mode==28:
    teams.eagles()

elif mode==29:
    teams.raiders()

elif mode==30:
    teams.redskins()

elif mode==31:
    teams.cowboys()

elif mode==32:
    teams.rams()

elif mode==33:
    teams.titans()

elif mode==34:
    teams.vikings()

elif mode==35:
    ravens._categories()

elif mode==36:
    ravens._index(url)

elif mode==37:
    teams.colts()

elif mode==38:
    teams.dolphins()

elif mode==39:
    pass

elif mode==40:
    bears._categories()

elif mode==41:
    bears._index(url)

elif mode==42:
    bears._getVideoUrl(url)

elif mode==43:
    teams.broncos()

elif mode==44:
    teams.steelers()

elif mode==45:
    teams.jaguars()

elif mode==46:
    pass

elif mode==47:
    pass

elif mode==48:
    teams.bills()

# xbmcplugin.endOfDirectory(int(sys.argv[1]))