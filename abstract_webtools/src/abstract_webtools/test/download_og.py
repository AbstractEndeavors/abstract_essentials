import threading
import time
import yt_dlp
YT_COOKIE = 'your_cookie_here'
from abstract_webtools import URLManager,SafeRequest,SoupManager,LinkManager
class VideoDownloader:

    def __init__(self, link):
        self.link = link
        self.video_urls=self.link if isinstance(self.link,list) else [self.link]
        self.output_video = './temp/video.mp4'
        self.starttime = None
        self.downloaded = 0
        self.start()
    def progress_callback(self, d):
        # Check if the 'status' key is present in the dictionary
        if d['status'] == 'downloading':
            # Compute total file size using 'total_bytes' key
            total_size = d.get('total_bytes', 0)
            # Compute bytes downloaded using 'downloaded_bytes' key
            self.downloaded = d.get('downloaded_bytes', 0)
            bytes_remaining = total_size - self.downloaded
            print(bytes_remaining)
    def download(self):
        for video_url in self.video_urls:
            ydl_opts = {
                'external_downloader': 'ffmpeg',
                'outtmpl': f'%(title)s.%(ext)s',
                'noprogress': True,
                # Register the progress_callback
                'progress_hooks': [self.progress_callback]
            }
            self.output_video = ydl_opts['outtmpl']
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.starttime = time.time()
                ydl.extract_info(url=video_url, download=True)

    def monitor(self):
        while True:
            time.sleep(60)  # check every minute

            if self.starttime:
                elapsed_time = time.time() - self.starttime
                percent = self.downloaded / (self.downloaded + elapsed_time)
                downloaded_minutes = elapsed_time / 60
                estimated_download_time = downloaded_minutes / percent - downloaded_minutes

                if estimated_download_time >= 1.5:
                    print("Seems like YouTube is limiting our download speed, restarting the download to mitigate the problem..")
                    # TODO: Find a way to stop the current download and restart. This may not work efficiently since pytube doesn't expose a cancel download method.
                    self.start()  # Restart the download process

    def start(self):
        download_thread = threading.Thread(target=self.download)
        monitor_thread = threading.Thread(target=self.monitor)

        download_thread.start()
        monitor_thread.start()

        download_thread.join()
        monitor_thread.join()

print('hi')        
url = "https://www.pornhub.com/view_video.php?viewkey=ph5e9c962f30314"
url_manager = URLManager(url=url)
request_manager = SafeRequest(url_manager=url_manager)
soup_manager = SoupManager(url_manager=url_manager,request_manager=request_manager)
link_manager = LinkManager(url_manager=url_manager,soup_manager=soup_manager,link_attr_value_desired=['/view_video.php?viewkey='])
print(link_manager.all_desired_links)

VideoDownloader(link=link_manager.all_desired_links)
