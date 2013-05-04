import os
import re
import sys
import xbmc
import xbmcgui
from mlb_common import addon_log
from traceback import format_exc, print_exc
from subprocess import Popen, PIPE, STDOUT


class MlbPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        addon_log('Player created')
        self.state = False
        
    def onPlayBackStarted(self):
        addon_log('- Playback Started -')
        self.state = 'Started'
        
    def get_time(self):
        return self.getTime()
    
    def onPlayBackEnded(self):
        addon_log('-Playback Ended-')
        self.state = 'Ended'
        
    def onPlayBackStopped(self):
        addon_log('- Playback Stopped -')
        self.state = 'Stopped'
        
    def player_state(self):
        return self.state
        
        
def check_subprocess():
    s = Popen('ps -A|grep mlb', shell=True, stdout=PIPE)
    for i in s.stdout:
        if re.search('mlbhls', i):
            addon_log('MLB-HLS is Running: %s' %i)
            return True
        addon_log('MLB-HLS is not running.')
        return False

def stop_subprocess():
    addon_log('- killing mlbhls -')
    os.system('pkill mlbhls')
    os.remove(filename)
    os.rmdir(dir)
    
def start_player(seektime=None):
    state = False
    player.play(filename)
    if seektime:
        player.seekTime(seektime)
    addon_log('Player Returned')
    while player.isPlaying():
        for i in range(0, 10):
            state = player.player_state()
            if not state:
                xbmc.sleep(1000)
                addon_log('waiting on player_state: %s' %i)
            else:
                break
        if state:
            addon_log('PlayerState: %s' %state)
            return player_monitor()
        else:
            addon_log('PlayerState: IS BROKEN')
        break
        
    if not state:
        if player.isPlaying():
            return player_monitor()
            
def player_monitor():
    addon_log('starting player_monitor')
    global player
    p_time = None
    state = None
    while not xbmc.abortRequested:
        state = player.player_state()
        if not state:
            addon_log('player state is broken!')
            if player.isPlaying():
                state = 'Started'
        if state == 'Started':
            t = player.get_time()
            if not t is None:
                p_time = t
            xbmc.sleep(2000)
        else:
            break
            
    addon_log('Player is not playing anymore.')
    state = player.player_state()
    addon_log('PlayerState: %s' %state)
    addon_log('PlayerTime: %s' %p_time)
    subprocess = check_subprocess()
    dialog = xbmcgui.Dialog()
    if subprocess:
        if state == 'Stopped':
            stop_subprocess()
        else:
            ret = dialog.yesno('MLBMC', 'MLB-HLS is running. Restart the player?')
            addon_log('Returned: %s' %ret)
            if ret:
                del player
                player = MlbPlayer()
                return start_player(p_time)
            else:
                stop_subprocess()
    else:
        if state == 'Stopped':
            stop_subprocess()
        else:
            ret = dialog.yesno('MLBMC', 'MLB-HLS is not running. Restart the player?')
            addon_log('Returned: %s' %ret)
            if ret:
                stop_subprocess()
                return xbmc.executebuiltin("XBMC.RunPlugin(plugin://plugin.video.mlbmc.hls/?mode=7&event=%s)" %event)
    subprocess = check_subprocess()
    
filename = sys.argv[1]
dir = sys.argv[2]
event = sys.argv[3]
player = MlbPlayer()
addon_log('Starting Player Script')
start_player()
del player
if check_subprocess():
    stop_subprocess()
addon_log('Script Finished')