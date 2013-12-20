##  Credit to Stacked for the original plugin.
##  Thanks to toastcutter for save passwords patch

import urllib
import urllib2
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import StorageServer
import json
from BeautifulSoup import BeautifulSoup

addon = xbmcaddon.Addon('plugin.video.jtv.archives')
addon_version = addon.getAddonInfo('version')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
home = xbmc.translatePath(addon.getAddonInfo('path'))
ICON = os.path.join(home, 'icon.png')
fanart = os.path.join(home, 'fanart.jpg')
next_png = os.path.join(home, 'resources', 'icons','next.png')
debug = addon.getSetting('debug')
j_nick = addon.getSetting('nickname')
j_pass = addon.getSetting('password')
cache = StorageServer.StorageServer("Jtv_Archives", 24)
profile_dir = xbmcvfs.exists(profile)
if not profile_dir:
    profile_dir = xbmcvfs.mkdir(profile)
search_queries = os.path.join(profile, 'search_queries')
passwords_file = os.path.join(profile, 'passwords')
blacklist = os.path.join(profile, 'blacklist')
favorites = os.path.join(profile, 'favorites')
try:
    FAV = open(favorites).read()
except:
    FAV = None
try:
    SEARCH_LIST = open(search_queries).read()
except:
    SEARCH_LIST = None
try:
    BLACKLIST = json.loads(open(blacklist).read())
except:
    BLACKLIST = ''
if debug == 'true':
    cache.dbg = True

LANGUAGES = {
    "sq" : "Albanian",
    "ar" : "Arabic",
    "hy" : "Belarusian",
    "bs" : "Bosnian",
    "bg" : "Bulgarian",
    "ca" : "Catalan",
    "zh" : "Chinese",
    "zh-tw" : "ChineseTW",
    "tl" : "Tagalog",
    "hr" : "Croatian",
    "cs" : "Czech",
    "da" : "Danish",
    "nl" : "Dutch",
    "en" : "English",
    "et" : "Estonian",
    "fa" : "Persian",
    "fi" : "Finnish",
    "fr" : "French",
    "de" : "German",
    "el" : "Greek",
    "he" : "Hebrew",
    "iw" : "Hebrew",
    "hi" : "Hindi",
    "hu" : "Hungarian",
    "is" : "Icelandic",
    "id" : "Indonesian",
    "it" : "Italian",
    "ja" : "Japanese",
    "ko" : "Korean",
    "lv" : "Latvian",
    "lt" : "Lithuanian",
    "mk" : "Macedonian",
    "no" : "Norwegian",
    "pl" : "Polish",
    "pt" : "Portuguese",
    "pt-br" : "PortugueseBrazil",
    "ro" : "Romanian",
    "ru" : "Russian",
    "sr" : "Serbian",
    "sk" : "Slovak",
    "sl" : "Slovenian",
    "es" : "Spanish",
    "sv" : "Swedish",
    "th" : "Thai",
    "tr" : "Turkish",
    "uk" : "Ukrainian",
    "vi" : "Vietnamese",
    "fa" : "Farsi",
    "pb" : "Portuguese",
    "pb" : "Brazilian"
    }


def addon_log(string):
        if debug == 'true':
            xbmc.log("[addon.Jtv-%s]: %s" %(addon_version, string.encode('utf-8', 'ignore')))


def get_request(url, headers=None, get_url=False):
        addon_log('Request: '+url)
        try:
            if headers is None:
                headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0',
                           'Referer' : 'http://www.justin.tv/'}
            req = urllib2.Request(url,None,headers)
            response = urllib2.urlopen(req)
            if get_url:
                data = response.geturl()
            else:
                data = response.read()
            # addon_log(str(response.info()))
            response.close()
        except urllib2.URLError, e:
            data = None
            errorStr = str(e.read())
            addon_log('We failed to open "%s".' %url)
            if hasattr(e, 'reason'):
                addon_log('We failed to reach a server.')
                addon_log('Reason: %s' %e.reason)
            if hasattr(e, 'code'):
                if 'archive' in url:
                    # if the channel does not have archives we expect a 403
                    if str(e.code) == '403':
                        data = '403'
                else:
                    # xbmc.executebuiltin("XBMC.Notification(Jtv,HTTP ERROR: "+str(e.code)+",5000,"+ICON+")")
                    addon_log('We failed with error code - %s.' %e.code)
        return data


def getLanguageCode(language):
        for i in LANGUAGES.items():
            if i[1] == language:
                lang_code = i[0]
                return lang_code


def get_json():
        url = 'http://api.justin.tv/api/category/list.json'
        data = get_request(url)
        return data


def Categories():
        if not FAV is None:
            addDir('Favorites','',5,os.path.join(home, 'resources', 'icons','fav.png'),'','','')
        j_user = addon.getSetting('j_user')
        if not j_user == "":
            addDir(j_user+' Favorites / Follows',j_user,11,os.path.join(home, 'resources', 'icons','jfav.png'),'','','')
        addDir('All', '', 1, os.path.join(home, 'resources', 'icons','all.png'),'','',1)
        result = cache.cacheFunction(get_json)
        # check for cache returning a tuple from version 0.3.6
        if isinstance(result, tuple):
            result = result[0]
        data = json.loads(result)
        for i in data.keys():
            catId = i
            icon = os.path.join(home, 'resources', 'icons', data[i]['icon'].split('/')[-1])
            name = data[i]['name']
            addDir(name, '', 6, icon,catId,'','')
        addDir('Enter Channel Name', '', 4, os.path.join(home, 'resources', 'icons','all.png'),'','','')
        if addon.getSetting('enable_search') == 'true':
            addDir('Search','',3,os.path.join(home, 'resources', 'icons', 'search.png'),'','','')
        return endOfDir()


def getSubcategories(catId, iconimage):
        addDir('All', '', 1, iconimage,catId,'',1)
        result = cache.cacheFunction(get_json)
        # check for cache returning a tuple from version 0.3.6
        if isinstance(result, tuple):
            result = result[0]
        data = json.loads(result)
        for i in data[catId]['subcategories'].keys():
            name = data[catId]['subcategories'][i]['name']
            addDir(name, '', 1, iconimage, catId, i, 1)
        return endOfDir()


def getLiveData(subCat,catId,page):
        url = 'http://api.justin.tv/api/stream/list.json?'
        if not catId == '':
            url += 'category='+catId
            if not subCat == '':
                url +='&subcategory='+subCat
        if not addon.getSetting('lang') == "None":
            url += '&language='+getLanguageCode(addon.getSetting('lang'))
            if not addon.getSetting('lang1') == "None":
                url += ','+getLanguageCode(addon.getSetting('lang1'))
        if not page is None or page == '':
            url += '&limit=20&offset='+str((page -1) * 20)
        addon_log('LiveData URL: '+url)
        data = get_request(url)
        if data:
            return index(data, subCat, catId, page)


def getUser(s_user):
        url = 'http://api.justin.tv/api/user/show/%s.json' %s_user
        data = get_request(url)
        addon_log('User Data: %s' %data)
        return data


def getUserFavorites(j_user):
        url = 'http://api.justin.tv/api/user/favorites/'+j_user+'.json?limit=100'
        if addon.getSetting('live_only') == "true":
            url += '&live=true'
        data = get_request(url)
        if data:
            return index(data, '', '', None)


def index(data, subCat, catId, page):
        data = json.loads(data)
        addon_log('json data:')
        addon_log(str(data))
        addon_log('Len Data = '+str(len(data)))
        addon_log('page = '+str(page))
        search_ids = ['users','live']

        if catId not in search_ids:
            if len(data) == 20:
                if not page is None:
                    addPage = page + 1
                else: addPage = 1
            else: addPage = None

        for i in data:
            mode = 2
            if catId in search_ids:
                mode = 4
            try:
                name = i['channel']['login']
                if name is None or name == '': raise
            except:
                try:
                    name = i['login']
                    if name is None or name == '': raise
                except:
                    try:
                        name =  i['name'].split('user_')[-1]
                        if name is None or name == '': raise
                    except:
                        name = str(i['image_url_medium']).split('/')[-1].split('-')[0]
            if name in BLACKLIST:
                addon_log('Channel: %s - Blacklisted' %name)
                continue
            try:
                subcat = i['channel']['subcategory_title']
                if subcat is None or subcat == '': raise
            except:
                try:
                    subcat = i['subcategory']
                    if subcat is None: raise
                except: subcat = ''
            try:
                title = i['channel']['status']
                if title is None or title == '': raise
            except:
                try:
                    title = i['channel']['title']
                    if title is None or title == '': raise
                except:
                    try:
                        title = i['title']
                        if title is None or title == '': raise
                    except: title = name
            try: timezone = i['channel']['timezone']
            except: timezone = ''
            try: bitrate = str(i['video_bitrate']).split('.')[0]
            except: bitrate = ''
            try: views = i['channel']['views_count']
            except:
                try: views = i['channel_view_count']
                except: views = ''
            try: lang = LANGUAGES[i['language']]
            except: lang = ''

            if addon.getSetting('fanart') == "true":
                try:
                    fanart = i['channel']['image_url_huge']
                except:
                    try: fanart = i['image_url_huge']
                    except: fanart = os.path.join(home, 'fanart.jpg')
                if addon.getSetting('use_channel_icon') == "0":
                    thumb = fanart
                else:
                    try: thumb = i['channel']['screen_cap_url_medium']
                    except:
                        try: thumb = i['screen_cap_url_medium']
                        except:
                            try: thumb = i['image_url_medium']
                            except: thumb = ''
            else:
                fanart = os.path.join(home, 'fanart.jpg')
                if addon.getSetting('use_channel_icon') == "0":
                    try: thumb = i['channel']['image_url_medium']
                    except:
                        try: thumb = i['image_url_medium']
                        except: thumb = ''
                else:
                    try: thumb = i['channel']['screen_cap_url_medium']
                    except:
                        try: thumb = i['screen_cap_url_medium']
                        except: thumb = ''

            if catId in search_ids or catId == 'channel':
                description = ''
                try:
                    if i['name'] is None: raise
                    description += '\n Name: %s' %i['name']
                except:
                    pass
                try:
                    if i['favorite_quotes'] is None: raise
                    description += '\n %s' %i['favorite_quotes']
                except:
                    pass
                try:
                    if i['login'] is None: raise
                    description += '\n Channel: %s' %i['login']
                except:
                    pass
                try:
                    if i['broadcaster'] is None: raise
                    description += '\n Broadcaster: %s' %i['broadcaster']
                except:
                    pass
                try:
                    if i['location'] is None: raise
                    description += '\n Location: %s' %i['location']
                except:
                    pass
            else:
                try: description = i['channel']['title'].encode('utf-8', 'ignore')
                except:
                    try: description = i['title'].encode('utf-8', 'ignore')
                    except: description = ''
                try: description += '\n Channel Name: '+name.encode('utf-8', 'ignore')
                except: pass
                try: description += '\n Timezone: '+timezone
                except: pass
                try: description += '\n Subcategory: '+subcat
                except: pass
                try: description += '\n Bitrate: '+bitrate
                except: pass
                try: description += '\n Language: '+lang
                except: pass
                try: description += '\n Views: '+views
                except: pass
            addLiveLink(name, title, '', mode, thumb, fanart, description)
        if not catId in search_ids:
            if not addPage is None:
                if addPage > page:
                    addDir('Next Page', '', 1, next_png, catId, subCat, addPage)
        else:
            if page:
                addDir('Next Page', page, 12, next_png, '', 'users', True)
        return endOfDir()


def getVideos(name, url=None, page=None):
        if url is None:
            url = 'http://api.justin.tv/api/channel/archives/'+name+'.json'

        request = get_request(url)
        if request is not None and request != '403':
            data = json.loads(request)
            for i in data:
                try:
                    title = i['title']
                except KeyError:
                    addon_log('--- KeyError ---')
                    title = ''
                video_url = i['video_file_url']
                part = 'Part: '+i['broadcast_part']
                if 'last_part' in i.keys():
                    if i['last_part'] == 'true':
                        part += ' - Last Part'
                started = i['start_time']
                created = i['created_on']
                thumb = i['image_url_medium']
                try:
                    length = i['length']
                    duration = str(int(length)/60)
                except:
                    duration = ''
                desc = part+'\nStarted: '+started+'\nCreated: '+created
                title += ' - '+part

                u=sys.argv[0]+"?url="+urllib.quote_plus(video_url)+"&mode=10"
                liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                liz.setInfo( type="Video", infoLabels={ "Title": title, "Plot": desc, "Duration": duration })
                liz.setProperty( "Fanart_Image", fanart)
                liz.setProperty('IsPlayable', 'true')
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

            if len(data) == 20:
                if page is None:
                    page = 1
                else:
                    page += 1
                url = url.split('?')[0]+'?offset='+str(page*20)
                addDir('Next Page', url, 7, next_png, '', '', str(page))

        elif request == '403':
            xbmc.executebuiltin("XBMC.Notification(Jtv,No archives found for channel: "+name+",5000,"+ICON+")")
        return endOfDir()


def playLive(channel_name, play=False, password=None):
        base_url = 'http://www.justin.tv/widgets/live_embed_player.swf?channel=%s' %channel_name
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0',
                   'Referer': 'http://www.justin.tv/%s' %channel_name}
        swf_url = get_request(base_url, headers, True)
        headers.update({'Referer': swf_url})
        url = 'http://usher.justin.tv/find/'+channel_name+'.json?type=any&group=&channel_subscription='
        if not password is None:
            url += '&private_code='+urllib.quote(password)
        request = get_request(url, headers)
        if request is None:
            return setUrl('', False)
        data = json.loads(request)
        if data == []:
            addon_log('No Data, jtv.find')
            return get_hls_stream(channel_name)
        
        stream = getQuality(data)
        if not stream:
            return setUrl('', False)
        if stream.endswith('private'):
            if password is None:
                password = getPassword(channel_name)
                if password is None:
                    password = ''
            url += '&private_code='+urllib.quote(password)
            request = get_request(url,headers)
            if request is None:
                return setUrl('', False)
            stream = getQuality(json.loads(request), True)
            if stream == 'Bad Password':
                addon_log('Bad Password')
                return setUrl('', False)
        if stream.startswith('rtmp_key_error'):
            addon_log('rtmp_key_error')
            return setUrl('', False)
        addon_log('Stream: %s' %stream)
        swf = ' swfUrl=%s swfVfy=1 live=1' % swf_url
        Pageurl = ' Pageurl=http://www.justin.tv/'+channel_name
        url = stream+swf+Pageurl
        if play == True:
            info = xbmcgui.ListItem(channel_name)
            playlist = xbmc.PlayList(1)
            playlist.clear()
            playlist.add(url, info)
            xbmc.executebuiltin('playlist.playoffset(video,0)')
        else:
            return setUrl(url, True)

            
def get_hls_stream(channel_name):
    url = 'https://api.twitch.tv/api/channels/%s/access_token?as3=t' %channel_name
    data = json.loads(get_request(url))
    if not data:
        xbmc.executebuiltin("XBMC.Notification(Jtv,Live Data Not Found,5000,"+ICON+")")
        return setUrl('', False)

    params = [
        'nauthsig=%s' %data['sig'],
        'player=jtvweb',
        'private_code=null',
        'type=any',
        'nauth=%s' %urllib2.quote(data['token']),
        'allow_source=true',
            ]
    stream_url = 'http://usher.twitch.tv/select/%s.json?' %channel_name + '&'.join(params)
    return setUrl(stream_url, True)
    
            

def setUrl(path, succeeded):
        item = xbmcgui.ListItem(path=path)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), succeeded, item)


def getQuality(data, password=False):
        s_type = {'0' : 'live',
                  '1' : '720p',
                  '2' : '480p',
                  '3' : '360p',
                  '4' : '240p',
                  '5' : 'iphonehigh',
                  '6' : 'iphonelow'}
        q_type = s_type[addon.getSetting('stream_quality')]
        streams = []
        for i in data:
            token = None
            try:
                token = ' jtv='+i['token'].replace('\\','\\5c').replace(' ','\\20').replace('"','\\22')
            except KeyError:
                needed_info = None
                try:
                    addon_log('Needed Info: %s' %i['needed_info'])
                    needed_info = i['needed_info']
                except KeyError:
                    pass
                if not password:
                    if 'private' in needed_info:
                            token = 'private'
                else:
                    try:
                        if i['error'] == 'Bad Password':
                            xbmc.executebuiltin("XBMC.Notification(Jtv,Bad Password,5000,"+ICON+")")
                            return 'Bad Password'
                        else:
                            addon_log('--- Error: %s ---' %i['error'])
                            pass
                    except KeyError:
                        addon_log('No error mesg.')
                        pass
            try:
                rtmp = i['connect']+'/'+i['play']
            except KeyError:
                rtmp = 'rtmp_key_error'
                addon_log('--- rtmp exception ---')
            if token is not None:
                if q_type == i['type']:
                    addon_log('---- Stream Type: %s ----' %i['type'])
                    return rtmp+token
                else:
                    streams.append((i['type'], rtmp, token))

        if len(streams) < 1:
            addon_log('----- Token Error ------')
            return None
        elif len(streams) == 1:
            addon_log('---- Stream Type: %s ----' %streams[0][0])
            return streams[0][1]+streams[0][2]
        else:
            path = None
            for i in range(len(s_type)):
                quality = s_type[str(i)]
                for q in streams:
                    if q[0] == quality:
                        addon_log('---- Stream Type: %s ----' %q[0])
                        path = q[1]+q[2]
                        break
                if path:
                    break
            return path


def loadPasswords():
        passwords = {}
        if addon.getSetting('save_passwords') == 'true':
            if xbmcvfs.exists(passwords_file):
                passwords = json.loads(open(passwords_file).read())
        return passwords


def savePasswords(passwords):
        if addon.getSetting('save_passwords') == 'true':
            f = open(passwords_file, "w")
            f.write(json.dumps(passwords))
            f.close()


def getPassword(name):
        passwords = loadPasswords()
        password = ''
        if name in passwords:
            password = passwords[name]
        keyboard = xbmc.Keyboard(password,'Enter Password')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        password = keyboard.getText()
        passwords[name] = password
        savePasswords(passwords)
        if len(password) == 0:
            return None
        else:
            return password


def search(search_q, url=None):
        def chooseSearchType():
                dialog = xbmcgui.Dialog()
                ret = dialog.select('Choose a sherch type.', ['User', 'Live'])
                if ret == 0:
                    return 'users'
                else:
                    return 'live'

        s_type = None

        if search_q == 'Previous Search Queries':
            search_list = json.loads(open(search_queries).read())
            for i in search_list:
                # check for tuple, prior to 3.7 only the query string was saved
                if isinstance(i, tuple) or isinstance(i, list):
                    title = i[0]
                    url = 'http://www.justin.tv/search?q=%s&sort-by=relevance&only=%s' %(urllib.quote_plus(i[0]), i[1])
                else:
                    title = i
                    url = 'saved_search_query'
                addDir(title,url,12,os.path.join(home, 'resources', 'icons', 'search.png'),'','','',True)
            return endOfDir()

        elif search_q == 'New Search':
            searchStr = ''
            keyboard = xbmc.Keyboard(searchStr,'Search')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            search_q = keyboard.getText()
            if len(search_q) == 0:
                return
            s_type = chooseSearchType()
            if addon.getSetting('save_search') == 'true':
                search_file = xbmcvfs.exists(search_queries)
                if not search_file:
                    search_file = xbmc.makeLegalFilename(search_queries)
                    search_list = []
                else:
                    search_list = json.loads(open(search_queries).read())
                search_list.append((search_q, s_type))
                a = open(search_queries, "w")
                a.write(json.dumps(search_list))
                a.close()
            url = 'http://www.justin.tv/search?q=%s&sort-by=relevance&only=%s' %(urllib.quote_plus(search_q), s_type)

        if url == 'saved_search_query':
            s_type = chooseSearchType()
            url = 'http://www.justin.tv/search?q=%s&sort-by=relevance&only=%s' %(urllib.quote_plus(search_q), s_type)

        if s_type is None:
            if 'only=live' in url:
                s_type = 'live'
            else:
                s_type = 'users'

        addon_log('Search URL: '+url)
        page = None
        data = get_request(url)
        soup = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
        items = soup.findAll('span', attrs={'class': 'small black'})
        user_list = []
        for i in items:
            user = None
            title = None
            try:
                title = i.findPrevious('a', attrs={'class': 'title broadcast-title'}).string
            except:
                pass
            try:
                user = json.loads(getUser(i.string))
            except:
                addon_log('getUser excemption: %s' %i.string)
            if user is None:
                user = {'login': i.string}
            if title:
                user.update({'title': title})
            user_list.append(user)
            xbmc.sleep(200)

        if soup.find('span', attrs={'class': "prev_next next"}):
            try:
                page = soup.find('span', attrs={'class': "prev_next next"}).a['href']
            except:
                pass
            if page:
                if 'page=1' in page:
                    page = None
                else:
                    if ('only=%s' %s_type) in page:
                        page = 'http://www.justin.tv'+page
                    else:
                        addon_log('page does not match search type ???')
                        page = ('http://www.justin.tv'+page.replace('only=all', 'only=%s' %s_type)
                                .replace('only=live', 'only=%s' %s_type).replace('only=users', 'only=%s' %s_type))
        if len(user_list) > 0:
            return index(json.dumps(user_list), '', s_type, page)
        else:
            return xbmc.executebuiltin("XBMC.Notification(Jtv,No Results for: "+search_q+",5000,"+ICON+")")


def remove_search(name):
        search_list = json.loads(open(search_queries).read())
        for index in range(len(search_list)):
            if name in search_list[index]:
                del search_list[index]
                a = open(search_queries, "w")
                a.write(json.dumps(search_list))
                a.close()
                return xbmc.executebuiltin('Container.Refresh')


def get_search():
        search_file = xbmcvfs.exists(search_queries)
        if search_file:
            addDir('New Search','',12,os.path.join(home, 'resources', 'icons', 'search.png'),'','','')
            addDir('Previous Search Queries','',12,os.path.join(home, 'resources', 'icons', 'search.png'),'','','')
            return endOfDir()
        else:
            return search('New Search')


def enterChannel(channel_name):
        if name == 'Enter Channel Name':
            searchStr = ''
            keyboard = xbmc.Keyboard(searchStr,'Channel Name')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            channel_name = keyboard.getText()
            if len(channel_name) == 0:
                return
            user_data = getUser(channel_name)
            if user_data:
                s_user = json.loads(user_data)
                return index(json.dumps([s_user]), None, 'channel', None)
            else:
                return xbmc.executebuiltin("XBMC.Notification(Jtv,Did not find channel: "+channel_name+",5000,"+ICON+")")

        url = 'http://api.justin.tv/api/stream/list.json?channel='+channel_name
        data = get_request(url)
        if data is None or data == '[]':
            xbmc.executebuiltin("XBMC.Notification(Jtv,No live stream found for "+channel_name+",5000,"+ICON+")")
            xbmc.sleep(3000)
            return getVideos(channel_name)
        else:
            return index(data, None, None, None)


def getFavorites():
        for i in json.loads(FAV):
            name = i[0]
            thumb = i[1]
            title = i[2]
            addLiveLink(name,title,'',2,thumb,thumb,'')
        return endOfDir()


def addFavorite(name,thumb,title):
        keyboard = xbmc.Keyboard(title,'Rename?')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        newTitle = keyboard.getText()
        if len(newTitle) == 0:
            return
        else:
            title = newTitle
        if not FAV is None:
            data = json.loads(FAV)
            data.append((name,thumb,title))
            a = open(favorites, "w")
            a.write(json.dumps(data))
            a.close()
        else:
            favorites_file = xbmcvfs.exists(favorites)
            if not favorites_file:
                favorites_file = xbmc.makeLegalFilename(favorites)
            fav_list = []
            fav_list.append((name,thumb,title))
            a = open(favorites, "w")
            a.write(json.dumps(fav_list))
            a.close()


def rmFavorite(name):
        data = json.loads(FAV)
        for index in range(len(data)):
            if data[index][0]==name:
                del data[index]
                a = open(favorites, "w")
                a.write(json.dumps(data))
                a.close()
                return xbmc.executebuiltin('Container.Refresh')


def addToBlacklist(name):
        blacklist_ = xbmcvfs.exists(blacklist)
        if not blacklist_:
            blacklist_file = xbmc.makeLegalFilename(blacklist)
            black_list = []
        else:
            black_list = json.loads(open(blacklist, "r").read())
        black_list.append(name)
        f = open(blacklist, "w")
        f.write(json.dumps(black_list))
        f.close
        return xbmc.executebuiltin('Container.Refresh')


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


def addDir(name,url,mode,iconimage,catId,subCat,page,showcontext=False):
        u=(sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&page="+str(page)+
           "&name="+urllib.quote_plus(name)+"&catId="+urllib.quote_plus(catId)+"&subCat="+urllib.quote_plus(subCat)+
           "&iconimage="+urllib.quote_plus(iconimage))
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        if showcontext:
            if name in SEARCH_LIST:
                contextMenu = [('Remove','XBMC.Container.Update(%s?mode=13&name=%s)' %(sys.argv[0], urllib.quote_plus(name)))]
                liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addLiveLink(name,title,url,mode,iconimage,fanart,description,showcontext=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": title, "Plot": description})
        liz.setProperty("Fanart_Image", fanart)
        liz.setProperty('IsPlayable', 'true')
        contextMenu = []
        if showcontext:
            if FAV:
                if name in FAV:
                    contextMenu.append(('Remove from Jtv Favorites','XBMC.RunPlugin(%s?mode=9&name=%s)'
                                        %(sys.argv[0], urllib.quote_plus(name))))
                else:
                    contextMenu.append(('Add to Jtv Favorites','XBMC.RunPlugin(%s?mode=8&name=%s&iconimage=%s&title=%s)'
                                        %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(fanart),
                                        urllib.quote_plus(title.encode('utf-8','ignore')))))
            else:
                contextMenu.append(('Add to Jtv Favorites','XBMC.RunPlugin(%s?mode=8&name=%s&iconimage=%s&title=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(fanart),
                                    urllib.quote_plus(title.encode('utf-8','ignore')))))
            contextMenu.append(('Get Channel Archives','XBMC.Container.Update(%s?mode=7&name=%s)'
                %(sys.argv[0], urllib.quote_plus(name))))
            contextMenu.append(('Run IrcChat', "RunScript(script.ircchat,"
                "run_irc=True&nickname=%s&username=%s&password=%s&host=%s&channel=%s)"
                %(j_nick, j_nick, j_pass, name+'.jtvirc.com', name)))
            contextMenu.append(('Blacklist Channel','XBMC.RunPlugin(%s?mode=14&name=%s)' %(sys.argv[0], urllib.quote_plus(name))))
        liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def setViewMode():
        if not addon.getSetting('view_mode') == "0":
            try:
            # if (xbmc.getSkinDir() == "skin.confluence"):
                if addon.getSetting('view_mode') == "1": # List
                    xbmc.executebuiltin('Container.SetViewMode(502)')
                elif addon.getSetting('view_mode') == "2": # Big List
                    xbmc.executebuiltin('Container.SetViewMode(51)')
                elif addon.getSetting('view_mode') == "3": # Thumbnails
                    xbmc.executebuiltin('Container.SetViewMode(500)')
                elif addon.getSetting('view_mode') == "4": # Poster Wrap
                    xbmc.executebuiltin('Container.SetViewMode(501)')
                elif addon.getSetting('view_mode') == "5": # Fanart
                    xbmc.executebuiltin('Container.SetViewMode(508)')
                elif addon.getSetting('view_mode') == "6":  # Media info
                    xbmc.executebuiltin('Container.SetViewMode(504)')
                elif addon.getSetting('view_mode') == "7": # Media info 2
                    xbmc.executebuiltin('Container.SetViewMode(503)')
                elif addon.getSetting('view_mode') == "8": # Media info 3
                    xbmc.executebuiltin('Container.SetViewMode(515)')
            except:
                addon_log("SetViewMode Failed: "+addon.getSetting('view_mode'))
                addon_log("Skin: "+xbmc.getSkinDir())

def endOfDir():
        try:
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
        except:
            pass
        try:
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        except:
            pass
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


params=get_params()

url=None
name=None
mode=None
catId=''
subCat=''
page=None
play=False
password=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    title=urllib.unquote_plus(params["title"])
except:
    pass
try:
    catId=urllib.unquote_plus(params["catId"])
except:
    pass
try:
    subCat=urllib.unquote_plus(params["subCat"])
except:
    pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    page=int(params["page"])
except:
    pass
try:
    play=eval(params["play"])
except:
    pass
try:
    password=params["password"]
except:
    pass

addon_log("Mode: "+str(mode))
addon_log("URL: "+str(url))
addon_log("Name: "+str(name))

if mode==None:
    Categories()

elif mode==1:
    getLiveData(subCat,catId,page)
    setViewMode()

elif mode==2:
    playLive(name, play, password)
    xbmc.sleep(3000)
    if addon.getSetting('run_chat') == 'true':
        xbmc.executebuiltin(
            "RunScript(script.ircchat,"
            "run_irc=True&nickname=%s&username=%s&password=%s&host=%s&channel=%s)"
            %(j_nick, j_nick, j_pass, name+'.jtvirc.com', name))

elif mode==3:
    get_search()

elif mode==4:
    enterChannel(name)

elif mode==5:
    getFavorites()
    setViewMode()

elif mode==6:
    getSubcategories(catId, iconimage)

elif mode==7:
    getVideos(name, url, page)
    setViewMode()

elif mode==8:
    addFavorite(name,iconimage,title)

elif mode==9:
    rmFavorite(name)

elif mode==10:
    setUrl(url, True)

elif mode==11:
    getUserFavorites(url)
    setViewMode()

elif mode==12:
    search(name, url)
    setViewMode()

elif mode==13:
    remove_search(name)

elif mode==14:
    addToBlacklist(name)
