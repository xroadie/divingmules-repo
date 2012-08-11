import urllib,urllib2,re,os
import xbmcplugin,xbmcgui,xbmcaddon
from BeautifulSoup import BeautifulSoup
try:
    import json
except:
    import simplejson as json
import resources.lib.common as common
import resources.lib.dallas as dallas
import resources.lib.ravens as ravens
import resources.lib.bears as bears
import resources.lib.jaguars as jaguars
import resources.lib.teams as teams

__settings__ = xbmcaddon.Addon(id='plugin.video.nfl')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
cdn = __settings__.getSetting('cdn')
bitrate = __settings__.getSetting('bitrate')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
next = xbmc.translatePath( os.path.join( home, 'resources','icons','next.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

teams_ = {
        "BUF" : { "url" : "http://www.buffalobills.com/", "videoPage":"/teams/buffalobills/profile?team=BUF", "city" : "Buffalo", "nickname" : "Bills" },
        "MIA" : { "url" : "http://www.miamidolphins.com/", "videoPage":"/teams/miamidolphins/profile?team=MIA", "city" : "Miami", "nickname" : "Dolphins" },
        "NE" : { "url" : "http://www.patriots.com/", "videoPage":"/teams/newenglandpatriots/profile?team=NE", "city" : "New England", "nickname" : "Patriots" },
        "NYJ" : { "url" : "http://www.newyorkjets.com/", "videoPage":"/teams/newyorkjets/profile?team=NYJ", "city" : "New York", "nickname" : "Jets" },
        "BAL" : { "url" : "http://www.baltimoreravens.com/", "videoPage":"/teams/baltimoreravens/profile?team=BAL", "city" : "Baltimore", "nickname" : "Ravens" },
        "CIN" : { "url" : "http://www.bengals.com/", "videoPage":"/teams/cincinnatibengals/profile?team=CIN", "city" : "Cincinnati", "nickname" : "Bengals" },
        "CLE" : { "url" : "http://www.clevelandbrowns.com/", "videoPage":"/teams/clevelandbrowns/profile?team=CLE", "city" : "Cleveland", "nickname" : "Browns" },
        "PIT" : { "url" : "http://www.steelers.com/", "videoPage":"/teams/pittsburghsteelers/profile?team=PIT", "city" : "Pittsburgh", "nickname" : "Steelers" },
        "HOU" : { "url" : "http://www.houstontexans.com/", "videoPage":"/teams/houstontexans/profile?team=HOU", "city" : "Houston", "nickname" : "Texans" },
        "IND" : { "url" : "http://www.colts.com/", "videoPage":"/teams/indianapoliscolts/profile?team=IND", "city" : "Indianapolis", "nickname" : "Colts" },
        "JAC" : { "url" : "http://www.jaguars.com/", "videoPage":"/teams/jacksonvillejaguars/profile?team=JAC", "city" : "Jacksonville", "nickname" : "Jaguars" },
        "TEN" : { "url" : "http://www.titansonline.com/", "videoPage":"/teams/tennesseetitans/profile?team=TEN", "city" : "Tennessee", "nickname" : "Titans" },
        "DEN" : { "url" : "http://www.denverbroncos.com/", "videoPage":"/teams/denverbroncos/profile?team=DEN", "city" : "Denver", "nickname" : "Broncos" },
        "KC" : { "url" : "http://www.kcchiefs.com/", "videoPage":"/teams/kansascitychiefs/profile?team=KC", "city" : "Kansas City", "nickname" : "Chiefs" },
        "OAK" : { "url" : "http://www.raiders.com/", "videoPage":"/teams/oaklandraiders/profile?team=OAK", "city" : "Oakland", "nickname" : "Raiders" },
        "SD" : { "url" : "http://www.chargers.com/", "videoPage":"/teams/sandiegochargers/profile?team=SD", "city" : "San Diego", "nickname" : "Chargers" },
        "DAL" : { "url" : "http://www.dallascowboys.com/", "videoPage":"/teams/dallascowboys/profile?team=DAL", "city" : "Dallas", "nickname" : "Cowboys" },
        "NYG" : { "url" : "http://www.giants.com/", "videoPage":"/teams/newyorkgiants/profile?team=NYG", "city" : "New York", "nickname" : "Giants" },
        "PHI" : { "url" : "http://www.philadelphiaeagles.com/", "videoPage":"/teams/philadelphiaeagles/profile?team=PHI", "city" : "Philadelphia", "nickname" : "Eagles" },
        "WAS" : { "url" : "http://www.redskins.com/", "videoPage":"/teams/washingtonredskins/profile?team=WAS", "city" : "Washington", "nickname" : "Redskins" },
        "CHI" : { "url" : "http://www.chicagobears.com/", "videoPage":"/teams/chicagobears/profile?team=CHI", "city" : "Chicago", "nickname" : "Bears" },
        "DET" : { "url" : "http://www.detroitlions.com/", "videoPage":"/teams/detroitlions/profile?team=DET", "city" : "Detroit", "nickname" : "Lions" },
        "GB" : { "url" : "http://www.packers.com/", "videoPage":"/teams/greenbaypackers/profile?team=GB", "city" : "Green Bay", "nickname" : "Packers" },
        "MIN" : { "url" : "http://www.vikings.com/", "videoPage":"/teams/minnesotavikings/profile?team=MIN", "city" : "Minnesota", "nickname" : "Vikings" },
        "ATL" : { "url" : "http://www.atlantafalcons.com/", "videoPage":"/teams/atlantafalcons/profile?team=ATL", "city" : "Atlanta", "nickname" : "Falcons" },
        "CAR" : { "url" : "http://www.panthers.com/", "videoPage":"/teams/carolinapanthers/profile?team=CAR", "city" : "Carolina", "nickname" : "Panthers" },
        "NO" : { "url" : "http://www.neworleanssaints.com/", "videoPage":"/teams/neworleanssaints/profile?team=NO", "city" : "New Orleans", "nickname" : "Saints" },
        "TB" : { "url" : "http://www.buccaneers.com/", "videoPage":"/teams/tampabaybuccaneers/profile?team=TB", "city" : "Tampa Bay", "nickname" : "Buccaneers" },
        "ARI" : { "url" : "http://www.azcardinals.com/", "videoPage":"/teams/arizonacardinals/profile?team=ARI", "city" : "Arizona", "nickname" : "Cardinals" },
        "STL" : { "url" : "http://www.stlouisrams.com/", "videoPage":"/teams/st.louisrams/profile?team=STL", "city" : "St. Louis", "nickname" : "Rams" },
        "SF" : { "url" : "http://www.sf49ers.com/", "videoPage":"/teams/sanfrancisco49ers/profile?team=SF", "city" : "San Francisco", "nickname" : "49ers" },
        "SEA" : { "url" : "http://www.seahawks.com/", "videoPage":"/teams/seattleseahawks/profile?team=SEA", "city" : "Seattle", "nickname" : "Seahawks" }
      }

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
         'Top 100 Players of' : 'http://www.nfl.com/videos/nfl-top100-2012',
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
      
      
def make_request(url, headers=None):
        try:
            if headers is None:
                headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                           'Referer' : 'http://www.nfl.com/'}
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
                xbmc.executebuiltin("XBMC.Notification(NFL.com,HTTP ERROR: "+str(e.code)+",5000,"+icon+")")
      

def categories():
        addDir('All Videos','http://www.nfl.com/videos/nfl-videos',1,icon)
        addDir('Game Highlights','http://www.nfl.com/videos/nfl-game-highlights',1,icon)
        addDir('Shows','',2,icon)
        addDir('Teams','',2,icon)
        addDir('Channels','',2,icon)
        addDir('Events','',2,icon)
        addDir('Search','',14,xbmc.translatePath( os.path.join( home, 'resources','icons','search.png' ) ))
        addDir('Team Sites','',6,icon)
        		

def teamSite():
        addDir('Az Cardinals.com','',9,'http://farm7.static.flickr.com/6001/5984449229_fbed0e5147_m.jpg')
        addDir('Baltimore Ravens.com','',35,'http://farm7.static.flickr.com/6121/6009301002_16eaf2f9b4_m.jpg')
        addDir('Bengals.com','',10,'http://farm7.static.flickr.com/6011/6009300352_4f1f19b3bc_m.jpg')
        addDir('Buccaneers.com','',11,'http://farm7.static.flickr.com/6130/6009473824_9015669a7c_m.jpg')
        addDir('Buffalo Bills.com','',48,'http://farm7.static.flickr.com/6138/5999411169_486330a2f4_m.jpg')
        addDir('Cleveland Browns.com','',12,'http://farm7.static.flickr.com/6127/6009299438_1f1dd2bec7_m.jpg')
        addDir('Chargers.com','',13,'http://farm7.static.flickr.com/6022/5983336472_98c373d130_m.jpg')
        addDir('Chicago Bears.com','',40,'http://farm7.static.flickr.com/6021/5987940049_a057f154d0_m.jpg')
        addDir('Colts.com','',37,'http://farm7.static.flickr.com/6014/5994129657_d872d7f4c5_m.jpg')
        addDir('Dallas Cowboys.com','',15,'http://farm7.static.flickr.com/6021/5995834962_9e0a38569b_m.jpg')
        addDir('Denver Broncos.com','',43,'http://farm7.static.flickr.com/6150/5982775071_230da3cce1_m.jpg')
        addDir('Detroit Lions.com','',18,'http://farm7.static.flickr.com/6008/5988506040_a546c4983b_m.jpg')
        addDir('49ers.com','',19,'http://farm7.static.flickr.com/6140/5985014424_c9817f5c82_m.jpg')
        addDir('Giants.com','',20,'http://farm7.static.flickr.com/6123/5995276331_5b335c77de_m.jpg')
        addDir('Houston Texans.com','',21,'http://farm7.static.flickr.com/6010/5994131823_c86dca0c96_m.jpg')
        addDir('Jaguars.com','',45,'http://farm7.static.flickr.com/6007/5994132885_27f73cafed_m.jpg')
        addDir('KC Chiefs.com','',22,'http://farm7.static.flickr.com/6135/5982773393_53a393e5e1_m.jpg')
        addDir('New York Jets.com','',23,'http://farm7.static.flickr.com/6127/5999958596_84ff270f61_m.jpg')
        addDir('New Orleans Saints.com','',24,'http://farm7.static.flickr.com/6125/6008924973_75bf096d30_m.jpg')
        addDir('Packers.com','',25,'http://farm7.static.flickr.com/6125/5987940779_50243f0567_m.jpg')
        addDir('Panthers.com','',26,'http://farm7.static.flickr.com/6012/6009472252_8492f9d7b2_m.jpg')
        addDir('Patriots.com','',27,'http://farm7.static.flickr.com/6133/5999408997_9dd8533670_m.jpg')
        addDir('Philadelphia Eagles.com','',28,'http://farm7.static.flickr.com/6140/5995277769_fd13323507_m.jpg')
        addDir('Raiders.com','',29,'http://farm7.static.flickr.com/6145/5982772583_6131581422_m.jpg')
        addDir('Redskins.com.com','',30,'http://farm7.static.flickr.com/6148/5995833826_2bb2981de1_m.jpg')
        addDir("Seahawks.com",'',31,'http://farm7.static.flickr.com/6002/5984451637_4f7bb3b46f_m.jpg')
        addDir('St Louis Rams.com','',32,'http://farm7.static.flickr.com/6012/5985015330_814587c665_m.jpg')
        addDir('Steelers.com','',44,'http://farm7.static.flickr.com/6125/6008751079_ef6123e945_m.jpg')
        addDir('Titans Online.com','',33,'http://farm7.static.flickr.com/6014/5994130863_839e1e630b_m.jpg')
        addDir('Vikings.com','',34,'http://farm7.static.flickr.com/6016/5988505154_0749939588_m.jpg')


def getSubCategories(name):
        if name == 'Shows':
            for i in shows.keys():
                addDir(i, shows[i], 1, icon)
        elif name == 'Channels':
            for i in channels.keys():
                addDir(i, channels[i], 1, icon)
        elif name == 'Events':
            for i in events.keys():
                addDir(i, events[i], 1, icon)
        elif name == 'Teams':
            for i in teams_.keys():
                title = '%s %s' %(teams_[i]['city'], teams_[i]['nickname'])
                url = 'http://www.nfl.com/videos/'+title.replace('.','').replace(' ', '-').lower()
                addDir(title, url, 1, '')


def index(url,name):
        if not name=='All Videos':
            if not re.search('page=', url):
                addPlaylist('Play Featured Videos',url,4,'')

        soup = BeautifulSoup(make_request(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
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
            addLink(name,link,thumb,duration,desc,3)
        try:
            page = soup.find('div', attrs={'id' : "video-list-pagination"})('a')[-1]['href']
            if not page == '?page=3':
                addDir('Next Page',url.split('?')[0]+page,1,next)
            else:
                addDir('Next Page','http://www.nfl.com/ajax/videos/v2?batchNum=1&channelId='+url.split('/')[-1].split('?')[0],5,next)
        except:
            pass


def getPage3(url):
        data = json.loads(make_request(url))
        videos = data['videos']
        for video in videos:
            url = video['videoCMSID']
            name = video['briefHeadline']
            thumb = video['xSmallImage'].split('_video_thumbnail_')[0]+'_video_rhr_210.jpg'
            desc = video['captionBlurb']
            duration = video['runTime'][:-3]
            addLink(name,url,thumb,duration,desc,3)


def getFeaturedVideos(url):
        soup = BeautifulSoup(make_request(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
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
        soup = BeautifulSoup(make_request(url))
        videos = soup('li')
        for video in videos:
            try:
                name = video('a')[0]['title']
                url = video('a')[0]['href'].split('id=')[1]
                thumb = video('a')[0]('img')[0]['src'].split('_video_thumbnail_')[0]+'_video_rhr_210.jpg'
                desc = video('p')[0].string
                duration = video('p')[1].string
                addLink(name,url,thumb,duration,desc,3)
            except:
                pass


def getVideoUrl(url):
        url = 'http://www.nfl.com/static/embeddablevideo/'+url+'.json'
        data = json.loads(make_request(url))
        bitrate = __settings__.getSetting('bitrate')
        if data['status'] == 'EXPIRED':
            xbmc.executebuiltin("XBMC.Notification(NFL,Sorry this video is expired.,5000,"+icon+")")
            return
        if len(data['cdnData']['bitrateInfo']) > 0:
            if bitrate == "3200k":
                try:
                    url = data['cdnData']['bitrateInfo'][4]['path']
                except:
                    try:
                        url = data['cdnData']['bitrateInfo'][3]['path']
                    except:
                        try:
                            url = data['cdnData']['bitrateInfo'][2]['path']
                        except:
                            try:
                                url = data['cdnData']['bitrateInfo'][1]['path']
                            except:
                                url = data['cdnData']['bitrateInfo'][0]['path']
            elif bitrate == "2000k":
                try:
                    url = data['cdnData']['bitrateInfo'][3]['path']
                except:
                    try:
                        url = data['cdnData']['bitrateInfo'][2]['path']
                    except:
                        try:
                            url = data['cdnData']['bitrateInfo'][1]['path']
                        except:
                            url = data['cdnData']['bitrateInfo'][0]['path']
            elif bitrate == "1200k":
                try:
                    url = data['cdnData']['bitrateInfo'][2]['path']
                except:
                    try:
                        url = data['cdnData']['bitrateInfo'][1]['path']
                    except:
                        url = data['cdnData']['bitrateInfo'][0]['path']
            elif bitrate == "700k":
                try:
                    url = data['cdnData']['bitrateInfo'][1]['path']
                except:
                    url = data['cdnData']['bitrateInfo'][0]['path']
            else:
                url = data['cdnData']['bitrateInfo'][0]['path']
        else:
            print '--- No bitrateInfo ---'
            class HeadRequest(urllib2.Request):
                    def get_method(self):
                        return "HEAD"
            print data
            cdn_ = 'http://a.video.nfl.com/'
            uri = data['cdnData']['uri']
            url = None
            if bitrate == "3200k":
                url = uri.replace(uri.split('_', -1)[-1], '3200k.mp4')
                try:
                    response = urllib2.urlopen(HeadRequest(cdn_+url))
                    print response.info()
                except:
                    bitrate = "2000k"
                    url = None
                    print '-- trying lower bitrate --'
            if bitrate == "2000k":
                url = uri.replace(uri.split('_', -1)[-1], '2000k.mp4')
                try:
                    response = urllib2.urlopen(HeadRequest(cdn_+url))
                    print response.info()
                except:
                    bitrate = "1200k"
                    url = None
                    print '-- trying lower bitrate --'
            if bitrate == "1200k":
                url = uri.replace(uri.split('_', -1)[-1], '1200k.mp4')
                try:
                    response = urllib2.urlopen(HeadRequest(cdn_+url))
                    print response.info()
                except:
                    bitrate = "700k"
                    url = None
                    print '-- trying lower bitrate --'
            # elif bitrate == "700k":
                # url = uri.replace(uri.split('_', -1)[-1], '700k.mp4')
            if url is None:
                url = uri
        if url.startswith('/'):
            url = url[1:]
            #cdn = 'rtmp://nfl.fcod.llnwd.net/a2290 app=a2290 swfUrl=http://flash.static.nfl.com/static/site/3.5/flash/video/video-detail-player.swf Playpath=vod/'
            #return cdn+url
        cdn0 = 'http://l.video.nfl.com/'           #limelightProg 700k only
        cdn1 ='http://vod.hstream.video.nfl.com/'  #akamaiHTTP  streams seem to end early
        cdn2 = 'http://a.video.nfl.com/'           #akamaiProg
        cdn3 = 'rtmp://cp86372.edgefcs.net/ondemand swfUrl=http://flash.static.nfl.com/static/site/4.3/flash/video/video-detail-player.swf'   #pathprefix="vod/gallery/" akamaiRTMP
        cdn4 = 'rtmp://nfl.fcod.llnwd.net/a2290 app=a2290 swfUrl=http://flash.static.nfl.com/static/site/4.3/flash/video/video-detail-player.swf'  # seems to only work at 700k   #pathprefix="vod/"  limelightRTMP
        liveCDN = 'rtmp://cp37426.live.edgefcs.net/live'

        if  __settings__.getSetting('cdn') == "limelight-RTMP 700k only":
            if not re.search('.mp4', url):
                playpath = ' Playpath=vod/'
            else:
                playpath = ' Playpath=mp4:vod/'
            cdn = cdn4+playpath
        elif  __settings__.getSetting('cdn') == "akamai-RTMP":
            if not re.search('.mp4', url):
                playpath = ' Playpath=vod/'
            else:
                playpath = ' Playpath=mp4:vod/'
            cdn = cdn3+playpath
        elif  __settings__.getSetting('cdn') == "limelightProg-HTTP 700k only":
            cdn = cdn0
        elif  __settings__.getSetting('cdn') == "akamai-HTTP":
            cdn = cdn1
        elif  __settings__.getSetting('cdn') == "akamaiProg-HTTP":
            cdn = cdn2
        print "Resolved URL -----> "+cdn+url
        return cdn+url


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


def addLink(name,url,iconimage,duration,description,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "duration": duration, "Plot":description } )
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty( "Fanart_Image", fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart)
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
        print ""+url
        index(url,name)

elif mode==2:
        print ""+url
        getSubCategories(name)

elif mode==3:
        print ""+url
        setUrl(url)

elif mode==4:
        print ""+url
        getFeaturedVideos(url)

elif mode==5:
        print ""+url
        getPage3(url)

elif mode==6:
        print ""
        teamSite()

elif mode==7:
        print ""
        common._index(url,fanart)

elif mode==8:
        print ""
        common._getVideoUrl(url)

elif mode==9:
        print ""
        teams.cardinals()

elif mode==10:
        print ""
        teams.bengals()

elif mode==11:
        print ""
        teams.buccaneers()

elif mode==12:
        print ""
        teams.browns()

elif mode==13:
        print ""
        teams.chargers()

elif mode==14:
        print ""
        search()

elif mode==15:
        print ""
        dallas._categories()

elif mode==16:
        print ""
        dallas._index(url)

elif mode==17:
        print ""
        dallas._getVideoUrl(url)

elif mode==18:
        print ""
        teams.lions()

elif mode==19:
        print ""
        teams.fortyniners()

elif mode==20:
        print ""
        teams.giants()

elif mode==21:
        print ""
        teams.texans()

elif mode==22:
        print ""
        teams.chiefs()

elif mode==23:
        print ""
        teams.jets()

elif mode==24:
        print ""
        teams.saints()

elif mode==25:
        print ""
        teams.packers()

elif mode==26:
        print ""
        teams.panthers()

elif mode==27:
        print ""
        teams.patriots()

elif mode==28:
        print ""
        teams.eagles()

elif mode==29:
        print ""
        teams.raiders()

elif mode==30:
        print ""
        teams.redskins()

elif mode==31:
        print ""
        teams.seahawks()

elif mode==32:
        print ""
        teams.rams()

elif mode==33:
        print ""
        teams.titans()

elif mode==34:
        print ""
        teams.vikings()

elif mode==35:
        print ""
        ravens._categories()

elif mode==36:
        print ""
        ravens._index(url)

elif mode==37:
        print ""
        teams.colts()

elif mode==38:
        print ""
        

elif mode==39:
        print ""
        

elif mode==40:
        print ""
        bears._categories()

elif mode==41:
        print ""
        bears._index(url)

elif mode==42:
        print ""
        bears._getVideoUrl(url)

elif mode==43:
        print ""
        teams.broncos()

elif mode==44:
        print ""
        teams.steelers()

elif mode==45:
        print ""
        jaguars._categories()

elif mode==46:
        print ""
        jaguars._index(url)

elif mode==47:
        print ""
        jaguars._getVideoUrl(url)

elif mode==48:
        print ""
        teams.bills()

xbmcplugin.endOfDirectory(int(sys.argv[1]))