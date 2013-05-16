import urllib,urllib2,re,os,sys
import xbmcplugin,xbmcgui,xbmcaddon
import resources.lib.common as common

__settings__ = xbmcaddon.Addon(id='plugin.video.nfl')
home = __settings__.getAddonInfo('path')


def get_sub_categories(names, urlA, urlB, urlC, icon, fanart):
        n = names.split(',')
        for i in range(len(n)):
            name = urllib.unquote(n[i]).replace(' - Video','').replace('Video - ','').replace('Videos - ','').replace('Video: ','')
            if not urlC == '':
                url = urlA+urllib.quote(name)+urlB+n[i]+urlC
            else:
                url = urlA+n[i]+urlB
            common.addDir(name, url, 7, icon, fanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def bengals():
        fanart = common.teams_['CIN']['fanart']
        icon = common.teams_['CIN']['thumb']
        urlA = 'http://www.bengals.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&sortField=DATE&contentType=AUDIO,VIDEO&showRelatedToContent=Yes&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showViewCount=Yes&showRSS=No&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'All%20Videos,Press%20Conference%20-%20Video,In%20the%20Locker%20Room%20-%20Video,Minicamp-OTAs%20-%20Video,Game%20Highlights%20-%20Video,Bengals%20Weekly%20Marvin%20Lewis%20-%20Video,NFL%20Network%20-%20Video,Game%20Previews%20-%20Video,Rookie%20Minicamp%20-%20Video,NFL%20Draft%20-%20Video,Training%20Camp%20-%20Video,NFL%20Scouting%20Combine%20-%20Video,Miscellaneous%20-%20Video'
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def browns():
        fanart = common.teams_['CLE']['fanart']
        icon = common.teams_['CLE']['thumb']
        urlA = 'http://www.clevelandbrowns.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=Yes&relatedClubs=CLE&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%20-%20Cleveland%20Browns%20Report,Video%20-%20Draft,Video%20-%20Features,Video%20-%20History,Video%20-%20Interviews,Video%20-%20Off%20the%20Field,Video%20-%20Press%20Conferences'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def buccaneers():
        fanart = common.teams_['TB']['fanart']
        icon = common.teams_['TB']['thumb']
        urlA = 'http://www.buccaneers.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=Yes&relatedClubs=TB&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=No&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Videos%3A%20Video%20Archive,Videos%3A%20Cheerleaders,Videos%3A%20Community'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def broncos():
        fanart = common.teams_['DEN']['fanart']
        icon = common.teams_['DEN']['thumb']
        urlA = 'http://www.denverbroncos.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=Yes&relatedClubs=DEN&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=No&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%20-%20Broncos%20TV,Video%20-%20Press%20Conferences,Video%20-%20Locker%20Room,Video%20-%20Events,Video%20-%20NFL%20Network,Video%20-%20Community,Video%20-%20Cheerleaders'
        common.addDir('Most Recent',urlA+'Most%20Recent'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def bills():
        fanart = common.teams_['BUF']['fanart']
        icon = common.teams_['BUF']['thumb']
        url = 'http://www.buffalobills.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName=All%20Videos&numberOfResults=10000&sortField=DATE&contentType=VIDEO&clubRelatedTerms=Game%20Highlights,Fans%20Videos,Bills%20Focus,Bills%20Roundup,NFL%20Network,Press%20Conferences,History%20Videos,Thurman%20Thomas%20Show,Bills%20All%20Access&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=No&showCount=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        common._index(url,fanart)


def cardinals():
        fanart = common.teams_['ARI']['fanart']
        icon = common.teams_['ARI']['thumb']
        urlA = 'http://www.azcardinals.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&sortField=DATE&contentType=VIDEO&relatedClubs=ARI&clubRelatedTerms='
        urlC = '&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=No&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Videos%20-%20Press%20Conferences,Videos%20-%20AzCardinals.com%20TV,Videos%20-%20Highlights,Videos%20-%20Maximum%20Cardinals'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def chiefs():
        fanart = common.teams_['KC']['fanart']
        icon = common.teams_['KC']['thumb']
        urlA = 'http://www.kcchiefs.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%20-%20Press%20Conferences,Video%20-%20Inside%20the%20Locker%20Room,Video%20-%20Game%20Highlights,Video%20-%20Cheerleaders,Video%20-%20Arrowhead%20Updates,Video%20-%20Community,Video%20-%20Training%20Camp,Video%20-%202%20Minutes%20with%20Mitch,Video%20-%20Turning%20Point,Video%20-%20Insider%20Game%20Reports,Video%20-%20NFL%20Network,Video%20-%20Chiefs%20Live,Video%20-%20History,Video%20-%20Fans'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def chargers():
        fanart = common.teams_['SD']['fanart']
        icon = common.teams_['SD']['thumb']
        urlA = 'http://www.chargers.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&sortField=DATE&contentType=VIDEO&relatedClubs=SD&clubRelatedTerms='
        urlC = '&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showRSS=No&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%3A%20Charger%20Girls,Video%3A%20Features,Video%3A%20Game%20Highlights,Video%3A%20Press%20Conference,Video%3A%20Sights%20and%20Sounds,Video%3A%20USA%20Football'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def colts():
        fanart = common.teams_['IND']['fanart']
        icon = common.teams_['IND']['thumb']
        urlA = 'http://www.colts.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&sortField=DATE&contentType=VIDEO&showRelatedToContent=No&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showViewCount=No&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%20-%20Press%20Conference,Video%20-%20Gameday,Video%20-%20Sounds%20of%20the%20Game,Video%20-%20Up%20Close%20Online,Video%20-%20NFL%20Network,Video%20-%20Cheerleaders,Video%20-%20Community,Video%20-%20Football,Video%20-%20Blue,Video%20-%20Features,Video%20-%20Post%20Game%20Coach%20Comments,Video%20-%20Post%20Game%20Locker%20Room,Video%20-%20Pre-Game%20Report,Video%20-%20Preps%20Pro%20Combine,Video%20-%20NFL%20Draft'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)
        
        
def cowboys():
        fanart = common.teams_['DAL']['fanart']
        icon = common.teams_['DAL']['thumb']
        urlA = 'http://www.dallascowboys.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&=undefined&contentListType=internal&sortField=DATE&contentType=VIDEO&showRelatedToContent=No&clubRelatedTerms='
        urlB = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showViewCount=No&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=20&pageno=1'
        names = 'Video%20-%20Players,Video%20-%20Game-Highlights,Video%20-%20Coaches-Executives,Video%20-%20NFL'
        common.addDir('All Videos',urlA.replace('&clubRelatedTerms=','')+urlB,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, '', icon, fanart)


def dolphins():
        fanart = common.teams_['MIA']['fanart']
        icon = common.teams_['MIA']['thumb']
        urlA = 'http://www.miamidolphins.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&sortField=DATE&contentType=VIDEO&numberOfResults=100&showRelatedToContent=Yes&relatedClubs=MIA&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showViewCount=No&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%3A%20Game%20Day,Video%3A%20Players,Video%3A%20Coach%20Sparano,Video%3A%20Cheerleaders,Video%3A%20Draft,Video%3A%20FinsidersTV,Video%3A%20Official%20Shows,Video%3A%20NFL%20Network,Video%3A%20Community,Video%3A%20Camp%20Dolphins,Video%3A%20Combine,Video%3A%20Finatics,Video%3A%20History%20and%20Alumni,Video%3A%20Espanol'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def eagles():
        fanart = common.teams_['PHI']['fanart']
        icon = common.teams_['PHI']['thumb']
        urlA = 'http://www.philadelphiaeagles.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=Yes&relatedClubs=PHI&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=No&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%20-%20Cheerleaders,Video%20-%20Eaglemania,Video%20-%20Eagles%20Confidential,Video%20-%20Eagles%20TV,Video%20-%20Fandemonium,Video%20-%20Features,Video%20-%20Football%20News,Video%20-%20Gameday%20Coverage,Video%20-%20NFL%20Network,Video%20-%20Off%20The%20Field,Video%20-%20The%20Players%20Show,Video%20-%20Training%20Camp,Video%20-%20Webcast'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def fortyniners():
        fanart = common.teams_['SF']['fanart']
        icon = common.teams_['SF']['thumb']
        urlA = 'http://www.49ers.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&sortField=DATE&contentType=VIDEO&showRelatedToContent=No&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showViewCount=No&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=15&pageno=1'  #&page=1&_=1312500804172
        names = 'Video%20-%20TV49,Video%20-%20Up%20Close,Video%20-%20Spencer%20for%20Hire,Video%20-%20Know%20Your%20Teammates,Video%20-%20Gold%20Rush,Video%20-%20Game%20Highlights,Video%20-%20NFL%20Network,Video%20-%20Youth%20Football,Video%20-%20Fans,Video%20-%20Beat%20the%20Clock,Video%20-%20Super%20Bowl,Video%20-%20Pro%20Bowl,Video%20-%20Scouting%20Combine,Video%20-%2049ers%20%20Total%20Access,Video%20-%20Total%20Access%20for%20Kids,Video%20-%2049ers%20Press%20Pass,Video%20-%20The%20Joe%20Show,Video%20-%20Hall%20of%20Fame,Video%20-%20Community,Video%20-%20Training%20Camp,Video%20-%20Draft,Video%20-%20Senior%20Bowl,Video%20-%20Spikes%20TV'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def giants():
        fanart = common.teams_['NYG']['fanart']
        icon = common.teams_['NYG']['thumb']
        urlA = 'http://www.giants.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&sortField=DATE&contentType=VIDEO&showRelatedToContent=Yes&relatedClubs=NYG&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showViewCount=No&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%20-%20Big%20Blue%20Kickoff,Video%20-%20Web%20Shows,Videos%20-%20Press%20Conferences,Video%20-%20Interviews,Videos%20-%20Gameday,Videos%20-%20Game%20Highlights,Videos%20-%20Features,Videos%20-%20TV%20Shows'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB.replace('&clubRelatedTerms=','')+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)
        
        
def jaguars():
        fanart = common.teams_['JAC']['fanart']
        icon = common.teams_['JAC']['thumb']
        urlA = 'http://www.jaguars.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&sortField=DATE&contentType=VIDEO&showRelatedToContent=No&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showViewCount=No&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Videos%20-%20Interviews,Videos%20-%20Special%20Features,Videos%20-%20Gameday,Videos%20-%20NFL%20Network,Videos%20-%20Training%20Camp,Videos%20-%20Draft,Videos%20-%20Teal%20Team,Videos%20-%20Community'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB.replace('&clubRelatedTerms=','')+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)
        

def jets():
        fanart = common.teams_['NYJ']['fanart']
        icon = common.teams_['NYJ']['thumb']
        urlA = 'http://www.newyorkjets.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=Yes&relatedClubs=NYJ&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=No&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'  #&page=1&_=1312466526529'
        names = 'Video%20-%20Features%2FInterviews,Video%20-%20Press%20Conferences,Video%20-%20Gameday%20Highlights,Video%20-%20Historical,Video%20-%20Flight%20Crew,Video%20-%20In%20the%20Community,Video%20-%20New%20Stadium,Video%20-%20Generation%20Jets,Video%20-%20Four%20Quarters,Video%20-%20Draft%2FCombine'
        n = names.split(',')
        common.addDir('All Videos',urlA+'Most%20Recent%20(All)'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def lions():
        fanart = common.teams_['DET']['fanart']
        icon = common.teams_['DET']['thumb']
        urlA = 'http://www.detroitlions.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&sortField=DATE&contentType=VIDEO&relatedClubs=DET&clubRelatedTerms='
        urlC = '&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=No&showCount=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%20-%20Ford%20Lions%20Report,Video%20-%20Game%20Highlights,Video%20-%20Locker%20Room,Video%20-%20Media%20Session,Video%20-%20Postgame,Video%20-%20Press%20Conferences,Video%20-%20Schwartz,Video%20-%20Season%20Review,Video%20-%20Training%20Camp,Video%20-%202011%20Combine,Video%20-%20Video%20Clips'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def packers():
        fanart = common.teams_['GB']['fanart']
        icon = common.teams_['GB']['thumb']
        urlA = 'http://prod.www.packers.clubs.nfl.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&sortField=DATE&contentType=VIDEO&showRelatedToContent=Yes&relatedClubs=GB&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showViewCount=Yes&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Videos%3A%20Ask%20Vic,Videos%3A%20Community,Videos%3A%20Draft,Videos%3A%20Exclusives,Videos%3A%20Fit%20Kids,Videos%3A%20Game%20Highlights,Videos%3A%20Hall%20of%20Fame,Videos%3A%20Inside%20Lambeau,Videos%3A%20Larry%20McCarren%27s%20Locker%20Room,Videos%3A%20Locker%20Room%20Interviews,Videos%3A%20Mike%20McCarthy%20Show,Videos%3A%20NFL%20Network,Videos%3A%20OTAs,Videos%3A%20Press%20Conference,Videos%3A%20Super%20Bowl%20XLV,Videos%3A%20Training%20Camp'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def panthers():
        fanart = common.teams_['CAR']['fanart']
        icon = common.teams_['CAR']['thumb']
        urlA = 'http://www.panthers.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&sortField=DATE&contentType=VIDEO&relatedClubs=CAR&clubRelatedTerms='
        urlC = '&showImage=Yes&showDescription=No&showByline=No&showPublicationDate=Yes&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=No&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Videos%20-%20Panthers.com%20TV,Videos%20-%20Panthers%20Gameday,Videos%20-%20Panthers%20Huddle,Videos%20-%20TopCats,Videos%20-%20Sir%20Purr,Videos%20-%20Community,Videos%20-%20NFL%20Network,Videos%20-%20Motorola'
        common.addDir('All Videos',urlA+'ALL%20VIDEOS'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def patriots():
        fanart = common.teams_['NE']['fanart']
        icon = common.teams_['NE']['thumb']
        urlA = 'http://www.patriots.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=Yes&relatedClubs=NE&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showCount=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=15&pageno=1'    #&page=1&_=1312484799972
        names = 'Video%20-%20General,Video%20-%20All%20Access,Video%20-%20Belichick%20Breakdowns,Video%20-%20Interviews,Video%20-%20From%20the%20NFL,Video%20-%20Patriots%20Today,Video%20-%20Locker%20Room%20Uncut,Video%20-%20PFW%20TV,Video%20-%20Press%20Conference,Video%20-%20Cheerleaders,Video%20-%20Super%20Bowl,Video%20-%20NFL,Video%20-%20Patriots%20Today%3A%20Locker%20Room%20Uncut'
        common.addDir('Latest Viedos',urlA+'Latest%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def raiders():
        fanart = common.teams_['OAK']['fanart']
        icon = common.teams_['OAK']['thumb']
        urlA = 'http://www.raiders.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=No&relatedClubs=OAK&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Videos%20-%20Press%20Conferences,Videos%20-%20Behind%20the%20Shield,Videos%20-%20Historical%20Highlights,Videos%20-%20Game%20Highlights,Videos%20-%20NFL%20Network,Videos%20-%20Raiderettes,Videos%20-%20Raiders%20Report,Videos%20-%20Silver%20and%20Black,Videos%20-%20Draft'
        common.addDir('All Videos',urlA+'ALL%20VIDEOS'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def redskins():
        fanart = common.teams_['WAS']['fanart']
        icon = common.teams_['WAS']['thumb']
        url = 'http://www.redskins.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&=undefined&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=Yes&relatedClubs=WAS&clubRelatedTerms=Video%20-%20Comcast%20SportsNet,Video%20-%20Press%20Conferences,Video%20-%20Cheerleaders,Video%20-%20Health%20and%20Wellness,Video%20-%20News%20and%20Highlights,Video%20-%20NFL%20Films,Video%20-%20Player%20and%20Coach%20Profiles,Video%20-%20Post%20Game,Video%20-%20Redskins%20Park%20Action,Video%20-%20Redskins%20Rule,Video%20-%20En%20Espanol&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=Yes&showContentType=Yes&showFilterType=No&showPagination=Yes&showPagerStatus=Yes&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        common._index(url,fanart)


def rams():
        fanart = common.teams_['STL']['fanart']
        icon = common.teams_['STL']['thumb']
        urlA = 'http://www.stlouisrams.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=No&relatedClubs=STL&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%20-%20Press%20Conferences,Video%20-%20Interviews,Video%20-%20Highlights,Video%20-%20Community,Video%20-%20Cheerleaders,Video%20-%20NFL%20Networks,Video%20-%20Shows,Video%20-%20NFL%20Draft,Video%20-%20Kids,Video%20-%20Schnucks,Video%20-%20My%20Ride,Video%20-%20Thats%20My%20Dog,Video%20-%20Inside%20Look,Video%20-%20The%20Sports%20Nook,Video%20-%20Wired,Video%20-%20Features,Video%20-%20History,Video%20-%20Live%20Video,Video%20-%20Inside%20the%20Game'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)

# broken
def seahawks():
        fanart = common.teams_['SEA']['fanart']
        icon = common.teams_['SEA']['thumb']
        url = 'http://www.seahawks.com/cda-web/av-dynamic-browser-module.htm?adSlot=1&advertisingStartingPoint=1&channelKey=Seahawks%20Daily^Seahawks%20Insider^Seahawks%20All-Access^Press%20Conferences^News%20Releases^Highlights^Seahawks%201-on-1^Coach%27s%20Show^Seahawks%20on%20NFL.com^Community^Sea%20Gals^12th%20MAN%20Flag&channelName=Seahawks%20Daily^Seahawks%20Insider^Seahawks%20All-Access^Press%20Conferences^News%20Releases^Highlights^Seahawks%201-on-1^Coach%27s%20Show^Seahawks%20on%20NFL.com^Community^Sea%20Gals^12th%20MAN%20Flag%20Raisers&companionAdSize=300x60&dartAdvertisingZone1=medialounge&dartAdvertisingZone2=videos&numberOfRecordsPerPage=10&preRollAdSize=640x360&showByline=No&showChannel=Yes^Yes^Yes^Yes^Yes^Yes^Yes^Yes^Yes^Yes^Yes^Yes&showDescription=No&showDuration=Yes&showImage=Yes&showPublicationDate=Yes&showRecent=Yes&showTitle=Yes&sortField=DATE&type=VIDEO&currentChannelName=Recent&pageno=1'
        # url = 'http://www.seahawks.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName=All%20Videos%20Archive&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=No&relatedClubs=SEA&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=No&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showCount=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=7&pageno=1'
        common.addDir('All Videos',url,7,icon,fanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def saints():
        fanart = common.teams_['NO']['fanart']
        icon = common.teams_['NO']['thumb']
        urlA = 'http://www.neworleanssaints.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=Yes&relatedClubs=NO&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showCount=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%20-%20Gameday,Video%20-%20Draft,Video%20-%20Community,Video%20-%20NFL%20Network,Video%20-%20Path%20to%20the%20Draft,Video%20-%20Youth%20Programs,Video%20-%20Training%20Camp'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def steelers():
        fanart = common.teams_['PIT']['fanart']
        icon = common.teams_['PIT']['thumb']
        urlA = 'http://www.steelers.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&cssID=videos&contentListType=internal&sortField=DATE&contentType=VIDEO&showRelatedToContent=No&relatedClubs=PIT&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showViewCount=No&showRSS=Yes&showContentType=Yes&showFilterType=month&showPagination=Yes&showPagerStatus=Yes&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Video%20-%20News%20Conferences,Video%20-%20Draft,Video%20-%20Chalk%20Talk,Video%20-%201st%20and%2010,Video%20-%20Training%20Camp,Video%20-%20Gameday,Video%20-%20Features,Video%20-%20Shows,Video%20-%20Interviews,Video%20-%20Off%20the%20Field,Video%20-%20Lifestyle'
        common.addDir('Recent Videos',urlA+'Recent%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def texans():
        fanart = common.teams_['HOU']['fanart']
        icon = common.teams_['HOU']['thumb']
        urlA = 'http://www.houstontexans.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&contentListType=internal&contentType=VIDEO&sortField=DATE&showRelatedToContent=No&relatedClubs=HOU&clubRelatedTerms='
        urlC = '&relatedToId=&showImage=Yes&showDescription=Yes&showByline=Yes&showPublicationDate=Yes&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=No&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=15&pageno=1'
        names = 'Videos%20-%20Football,Videos%20-%20Special%20Segments,Videos%20-%20Press%20Conferences,Videos%20-%20Community,Videos%20-%20Gameday,Videos%20-%20Cheerleaders,Videos%20-%20Season%20Highlights,Videos%20-%20Texans%20Huddle,Videos%20-%20Inside%20the%20Locker,Videos%20-%20Teammate%20Trivia,Videos%20-%20NFL%20Films%20Highlights'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def titans():
        fanart = common.teams_['TEN']['fanart']
        icon = common.teams_['TEN']['thumb']
        urlA='http://www.titansonline.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB='&sortField=DATE&contentType=VIDEO&relatedClubs=TEN&clubRelatedTerms='
        urlC='&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showRSS=Yes&showContentType=No&showFilterType=month&showPagination=Yes&showPagerStatus=No&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = '2010%20NFL%20Draft,Videos%3A%20Cheerleader,Videos%3A%20Community,Videos%3A%20Game%20Highlights,Videos%3A%20NFL%20Network%20Features,Videos%3A%20Player%20Interviews,Videos%3A%20Press%20Conference,Videos%3A%20Titans%20All%20Access,Videos%3A%20T-RAC'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)


def vikings():
        fanart = common.teams_['MIN']['fanart']
        icon = common.teams_['MIN']['thumb']
        urlA = 'http://www.vikings.com/cda-web/content-list-dynamic-module-paginated.htm?previewMode=false&displayName='
        urlB = '&numberOfResults=100&sortField=DATE&contentType=VIDEO&relatedClubs=MIN&clubRelatedTerms='
        urlC = '&showImage=Yes&showDescription=Yes&showByline=No&showPublicationDate=Yes&showRSS=Yes&showContentType=Yes&showFilterType=No&showPagination=Yes&showPagerStatus=No&showCount=No&showTitleStyle=Yes&view=content-list-variation-2&month=&year=&numberPerPage=10&pageno=1'
        names = 'Videos%20-%20Press%20Conferences,Videos%20-%20NFL%20Network,Videos%20-%20VEN,Videos%20-%20Stadium,Videos%20-%20Vikings%20Weekly,Videos%20-%20Game%20Day,Videos%20-%20Cheerleaders,Videos%20-%20Jared%20Allen%20Street%20Meet,Videos%20-%20Outreach,Videos%20-%20Vikings%20Wired,Videos%20-%20Viktor%20the%20Viking,Videos%20-%20Vikings%20GamePlan,Videos%20-%20Training%20Camp'
        common.addDir('All Videos',urlA+'All%20Videos'+urlB+names+urlC,7,icon,fanart)
        get_sub_categories(names, urlA, urlB, urlC, icon, fanart)