import urllib
import urllib2
import os
import sys
import xbmcplugin
import xbmcgui
import xbmcaddon
from BeautifulSoup import BeautifulSoup
try:
    import json
except:
    import simplejson as json

__settings__ = xbmcaddon.Addon(id='plugin.video.nfl')
home = __settings__.getAddonInfo('path')
next = os.path.join( home, 'resources','icons','next.png' )

# Fanart and icon images are from - Hawk Eyes' - http://www.flickr.com/photos/cpardue/sets/72157630500267508/  http://creativecommons.org/licenses/by-nc/2.0/deed.en
teams_ = {
          'MIN': {'url': 'http://www.vikings.com/', 'fanart': 'http://farm9.staticflickr.com/8423/7558109124_71f3d4c358_b.jpg', 'nickname': 'Vikings', 'thumb': u'http://farm9.staticflickr.com/8423/7558109124_71f3d4c358_q.jpg', 'city': 'Minnesota', 'mode': '34'},
          'MIA': {'url': 'http://www.miamidolphins.com/', 'fanart': 'http://farm8.staticflickr.com/7276/7591997376_eb884f884a_b.jpg', 'nickname': 'Dolphins', 'thumb': u'http://farm8.staticflickr.com/7276/7591997376_eb884f884a_q.jpg', 'city': 'Miami', 'mode': '38'},
          'CLE': {'url': 'http://www.clevelandbrowns.com/', 'fanart': 'http://farm8.staticflickr.com/7267/7598013258_116f18168b_b.jpg', 'nickname': 'Browns', 'thumb': u'http://farm8.staticflickr.com/7267/7598013258_116f18168b_q.jpg', 'city': 'Cleveland', 'mode': '12'},
          'ATL': {'url': 'http://www.atlantafalcons.com/', 'fanart': 'http://farm8.staticflickr.com/7137/7639502546_0e0655f0e0_b.jpg', 'nickname': 'Falcons', 'thumb': u'http://farm8.staticflickr.com/7137/7639502546_0e0655f0e0_q.jpg', 'city': 'Atlanta', 'mode': ''},
          'OAK': {'url': 'http://www.raiders.com/', 'fanart': 'http://farm9.staticflickr.com/8167/7553676514_d0b6973f5d_b.jpg', 'nickname': 'Raiders', 'thumb': u'http://farm9.staticflickr.com/8167/7553676514_d0b6973f5d_q.jpg', 'city': 'Oakland', 'mode': '29'},
          'CIN': {'url': 'http://www.bengals.com/', 'fanart': 'http://farm8.staticflickr.com/7130/7598141872_3e6b24d0f7_b.jpg', 'nickname': 'Bengals', 'thumb': u'http://farm8.staticflickr.com/7130/7598141872_3e6b24d0f7_q.jpg', 'city': 'Cincinnati', 'mode': '10'},
          'NYJ': {'url': 'http://www.newyorkjets.com/', 'fanart': 'http://farm8.staticflickr.com/7136/7592237170_ba5268f9af_b.jpg', 'nickname': 'Jets', 'thumb': u'http://farm8.staticflickr.com/7136/7592237170_ba5268f9af_q.jpg', 'city': 'New York', 'mode': '23'},
          'HOU': {'url': 'http://www.houstontexans.com/', 'fanart': 'http://farm9.staticflickr.com/8146/7624141482_83e0d43035_b.jpg', 'nickname': 'Texans', 'thumb': u'http://farm9.staticflickr.com/8146/7624141482_83e0d43035_q.jpg', 'city': 'Houston', 'mode': '21'},
          'GB': {'url': 'http://www.packers.com/', 'fanart': 'http://farm8.staticflickr.com/7125/7558113536_cf01db858c_b.jpg', 'nickname': 'Packers', 'thumb': u'http://farm8.staticflickr.com/7125/7558113536_cf01db858c_q.jpg', 'city': 'Green Bay', 'mode': '25'},
          'DEN': {'url': 'http://www.denverbroncos.com/', 'fanart': 'http://farm9.staticflickr.com/8167/7537419010_a0ed157f00_b.jpg', 'nickname': 'Broncos', 'thumb': u'http://farm9.staticflickr.com/8167/7537419010_a0ed157f00_q.jpg', 'city': 'Denver', 'mode': '43'},
          'CHI': {'url': 'http://www.chicagobears.com/', 'fanart': 'http://farm8.staticflickr.com/7133/7558110734_dc29b8d488_b.jpg', 'nickname': 'Bears', 'thumb': u'http://farm8.staticflickr.com/7133/7558110734_dc29b8d488_q.jpg', 'city': 'Chicago', 'mode': '40'},
          'BAL': {'url': 'http://www.baltimoreravens.com/', 'fanart': 'http://farm8.staticflickr.com/7107/7595573360_c493af2ec7_b.jpg', 'nickname': 'Ravens', 'thumb': u'http://farm8.staticflickr.com/7107/7595573360_c493af2ec7_q.jpg', 'city': 'Baltimore', 'mode': '35'},
          'WAS': {'url': 'http://www.redskins.com/', 'fanart': 'http://farm9.staticflickr.com/8431/7580510332_91c1832eb8_b.jpg', 'nickname': 'Redskins', 'thumb': u'http://farm9.staticflickr.com/8431/7580510332_91c1832eb8_q.jpg', 'city': 'Washington', 'mode': '30'},
          'JAC': {'url': 'http://www.jaguars.com/', 'fanart': 'http://farm9.staticflickr.com/8434/7631506164_81ff560dd4_b.jpg', 'nickname': 'Jaguars', 'thumb': u'http://farm9.staticflickr.com/8434/7631506164_81ff560dd4_q.jpg', 'city': 'Jacksonville', 'mode': '45'},
          'KC': {'url': 'http://www.kcchiefs.com/', 'fanart': 'http://farm9.staticflickr.com/8423/7553547886_fb7cca1f48_b.jpg', 'nickname': 'Chiefs', 'thumb': u'http://farm9.staticflickr.com/8423/7553547886_fb7cca1f48_q.jpg', 'city': 'Kansas City', 'mode': '22'},
          'DET': {'url': 'http://www.detroitlions.com/', 'fanart': 'http://farm8.staticflickr.com/7138/7558112026_17c11bb0b6_b.jpg', 'nickname': 'Lions', 'thumb': u'http://farm8.staticflickr.com/7138/7558112026_17c11bb0b6_q.jpg', 'city': 'Detroit', 'mode': '18'},
          'PHI': {'url': 'http://www.philadelphiaeagles.com/', 'fanart': 'http://farm8.staticflickr.com/7106/7577753160_b737a3f98d_b.jpg', 'nickname': 'Eagles', 'thumb': u'http://farm8.staticflickr.com/7106/7577753160_b737a3f98d_q.jpg', 'city': 'Philadelphia', 'mode': '28'},
          'TEN': {'url': 'http://www.titansonline.com/', 'fanart': 'http://farm9.staticflickr.com/8292/7631504578_156db79e9f_b.jpg', 'nickname': 'Titans', 'thumb': u'http://farm9.staticflickr.com/8292/7631504578_156db79e9f_q.jpg', 'city': 'Tennessee', 'mode': '33'},
          'NO': {'url': 'http://www.neworleanssaints.com/', 'fanart': 'http://farm8.staticflickr.com/7121/7693423688_91d14e2058_b.jpg', 'nickname': 'Saints', 'thumb': u'http://farm8.staticflickr.com/7121/7693423688_91d14e2058_q.jpg', 'city': 'New Orleans', 'mode': '24'},
          'DAL': {'url': 'http://www.dallascowboys.com/', 'fanart': 'http://farm9.staticflickr.com/8006/7580511152_5b3626751d_b.jpg', 'nickname': 'Cowboys', 'thumb': u'http://farm9.staticflickr.com/8006/7580511152_5b3626751d_q.jpg', 'city': 'Dallas', 'mode': '31'},
          'PIT': {'url': 'http://www.steelers.com/', 'fanart': 'http://farm8.staticflickr.com/7260/7706983556_8d69389282_b.jpg', 'nickname': 'Steelers', 'thumb': u'http://farm8.staticflickr.com/7260/7706983556_8d69389282_q.jpg', 'city': 'Pittsburgh', 'mode': '44'},
          'NE': {'url': 'http://www.patriots.com/', 'fanart': 'http://farm9.staticflickr.com/8153/7592236142_2224087cc4_b.jpg', 'nickname': 'Patriots', 'thumb': u'http://farm9.staticflickr.com/8153/7592236142_2224087cc4_q.jpg', 'city': 'New England', 'mode': '27'},
          'NYG': {'url': 'http://www.giants.com/', 'fanart': 'http://farm9.staticflickr.com/8011/7577751600_3a7322d0a7_b.jpg', 'nickname': 'Giants', 'thumb': u'http://farm9.staticflickr.com/8011/7577751600_3a7322d0a7_q.jpg', 'city': 'New York', 'mode': '20'},
          'STL': {'url': 'http://www.stlouisrams.com/', 'fanart': 'http://farm8.staticflickr.com/7266/7707192016_229f74dba1_b.jpg', 'nickname': 'Rams', 'thumb': u'http://farm8.staticflickr.com/7266/7707192016_229f74dba1_q.jpg', 'city': 'St. Louis', 'mode': '32'},
          'BUF': {'url': 'http://www.buffalobills.com/', 'fanart': 'http://farm9.staticflickr.com/8168/7584886332_aef5c77a2f_b.jpg', 'nickname': 'Bills', 'thumb': u'http://farm9.staticflickr.com/8168/7584886332_aef5c77a2f_q.jpg', 'city': 'Buffalo', 'mode': '48'},
          'SEA': {'url': 'http://www.seahawks.com/', 'fanart': 'http://farm9.staticflickr.com/8025/7707189036_f446c44518_b.jpg', 'nickname': 'Seahawks', 'thumb': u'http://farm9.staticflickr.com/8025/7707189036_f446c44518_q.jpg', 'city': 'Seattle', 'mode': ''},
          'CAR': {'url': 'http://www.panthers.com/', 'fanart': 'http://farm9.staticflickr.com/8026/7693427348_c3af79abcc_b.jpg', 'nickname': 'Panthers', 'thumb': u'http://farm9.staticflickr.com/8026/7693427348_c3af79abcc_q.jpg', 'city': 'Carolina', 'mode': '26'},
          'IND': {'url': 'http://www.colts.com/', 'fanart': 'http://farm8.staticflickr.com/7249/7624268924_e942b5ce81_b.jpg', 'nickname': 'Colts', 'thumb': u'http://farm8.staticflickr.com/7249/7624268924_e942b5ce81_q.jpg', 'city': 'Indianapolis', 'mode': '37'},
          'ARI': {'url': 'http://www.azcardinals.com/', 'fanart': 'http://farm9.staticflickr.com/8020/7707191042_4dd39ffc36_b.jpg', 'nickname': 'Cardinals', 'thumb': u'http://farm9.staticflickr.com/8020/7707191042_4dd39ffc36_q.jpg', 'city': 'Arizona', 'mode': '9'},
          'TB': {'url': 'http://www.buccaneers.com/', 'fanart': 'http://farm9.staticflickr.com/8160/7693428210_188f1d5303_b.jpg', 'nickname': 'Buccaneers', 'thumb': u'http://farm9.staticflickr.com/8160/7693428210_188f1d5303_q.jpg', 'city': 'Tampa Bay', 'mode': '11'},
          'SF': {'url': 'http://www.sf49ers.com/', 'fanart': 'http://farm9.staticflickr.com/8293/7707189862_f739aae819_b.jpg', 'nickname': '49ers', 'thumb': u'http://farm9.staticflickr.com/8293/7707189862_f739aae819_q.jpg', 'city': 'San Francisco', 'mode': '19'},
          'SD': {'url': 'http://www.chargers.com/', 'fanart': 'http://farm8.staticflickr.com/7250/7548210338_02e01f2981_b.jpg', 'nickname': 'Chargers', 'thumb': u'http://farm8.staticflickr.com/7250/7548210338_02e01f2981_q.jpg', 'city': 'San Diego', 'mode': '13'},
          }


def make_request(url, headers=None):
        try:
            if headers is None:
                headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
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


def _index(url,fanart):
        soup = BeautifulSoup(make_request(url))
        videos = soup.findAll('div', attrs={'class' : 'bd'})[0]('ul')[0]('li')
        for video in videos:
            title = video('a')[0]['title']
            link = video('a')[0]['href'].split('/')[-1]
            thumb = video('img')[0]['src']
            try:
                duration = video('span')[3].string.replace('(','').replace(')','')
                if not video('span')[4].string==None:
                    desc = video('span')[4].string
                else:
                    desc = video('span')[5].string
            except:
                duration =''
                try:
                    desc = video('span')[-1].string
                except:
                    desc =''
            try:
                addLink(title+' - '+desc,url.split('cda')[0]+'cda-web/audio-video-module.htm?dataMode=singleMediaContent&id='+link,thumb,duration,'',8,fanart)
            except:
                pass
        page = int(url[-1])
        url = url[:-1]+str(page+1)
        addDir('Next Page',url,7,next,fanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def _getVideoUrl(url):
        req = urllib2.Request(url)
        req.addheaders = [('Referer', url.split('cda')[0]),
                    ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        data = json.loads(link)
        print data
        if not data['MediaPlayList'][0]['cdnData'][0]['paths']['high']=='':
            url = data['MediaPlayList'][0]['cdnData'][0]['paths']['high']
        elif not data['MediaPlayList'][0]['cdnData'][0]['paths']['medium']=='':
            url = data['MediaPlayList'][0]['cdnData'][0]['paths']['medium']
        else:
            url = data['MediaPlayList'][0]['cdnData'][0]['paths']['low']
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def addLink(name,url,iconimage,duration,description,mode,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "duration": duration, "Plot":description } )
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty( "Fanart_Image", fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addPlaylist(name,url,mode,iconimage,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
