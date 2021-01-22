from __future__ import unicode_literals
from telethon import TelegramClient, events
import youtube_dl
from os import remove, rename, makedirs, path
from re import sub, search
DEFAULT_OUTTMPL = '%(id)s.%(ext)s'
ydl_opts = {'outtmpl': DEFAULT_OUTTMPL}
def callback(current, total):
    print('Uploaded', current, 'out of', total,
          'bytes: {:.2%}'.format(current / total))

def createdir(path):
    try:
        makedirs(path, exist_ok=True)
    except:
        print("File exists:" + path)

api_id = api_id
api_hash = 'api_hash'
client = TelegramClient('anon', api_id, api_hash)
@client.on(events.NewMessage())
async def handler(event):
    channel_id = event.message.peer_id.channel_id
    print(channel_id)
    video = event.message.message
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_dict = ydl.extract_info(video, download=False)
        num = 0
        if 'entries' in playlist_dict.keys():
            folder_path = './' + playlist_dict.get('uploader') + "/" + playlist_dict.get('title')
            createdir(folder_path)       
            for title_entries in playlist_dict['entries']:
                print("test")
                new_filename = folder_path + '/' + str(num) + ' - ' + title_entries.get('title') + '-' + title_entries.get('id') + ".mp4" 
                old_filename = title_entries.get('id') + ".mp4" 
                if path.isfile(new_filename):
                    await client.send_file(channel_id, new_filename, caption=title_entries.get('title'), supports_streaming=True, progress_callback=callback)
                elif path.isfile(new_filename) == False:
                    ydl.download([title_entries.get('webpage_url')])
                    await client.send_file(channel_id, old_filename, caption=title_entries.get('title'), supports_streaming=True, progress_callback=callback)
                    rename(old_filename, new_filename)       
                num = num + 1 
        else:
            folder_path_only_video = './' + playlist_dict.get('uploader') 
            createdir(folder_path_only_video)       
            old_filename = playlist_dict.get('id') + ".mp4" 
            new_filename = folder_path_only_video + '/' + playlist_dict.get('title') + '-' + playlist_dict.get('id') + ".mp4" 
            if path.isfile(new_filename):
                await client.send_file(channel_id, new_filename, caption=playlist_dict.get('title'), supports_streaming=True, progress_callback=callback)
            elif path.isfile(new_filename) == False:
                ydl.download([playlist_dict.get('webpage_url')])
                await client.send_file(channel_id, old_filename, caption=playlist_dict.get('title'), supports_streaming=True, progress_callback=callback)
                rename(old_filename, new_filename)                

client.start()
client.run_until_disconnected()



