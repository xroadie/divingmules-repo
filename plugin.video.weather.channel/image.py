try:
    import json
except:
    import simplejson as json
    
images = eval(sys.argv[1].replace('!!', ', '))
    
        
def slideshow_check():
        get_players = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}'))
        pic_player = False
        for i in get_players['result']:
            if i['type'] == 'picture':
                pic_player = True
            else: continue
        return pic_player
        
        
clear_playlist = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Clear", "params": {"playlistid":2}, "id": 1}')
items = []
for i in images:
    item = '{ "jsonrpc": "2.0", "method": "Playlist.Add", "params": { "playlistid": 2 , "item": {"file": "%s"} }, "id": 1 }' %i
    add_item = items.append(str(item))
add_playlist = xbmc.executeJSONRPC(str(items).replace("'",""))
get_playlist = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.GetItems", "params": {"playlistid":2}, "id": 1}'))
play = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.Open","params":{"item":{"playlistid":2}} }')
xbmc.sleep(4000)
while True:
    slideshow_check()
    xbmc.sleep(1000)
    if not slideshow_check():
        break
xbmc.executebuiltin('XBMC.RunAddon(plugin.video.weather.channel)')