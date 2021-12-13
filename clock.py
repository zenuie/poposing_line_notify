from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler
from poposing_notify import notification
import requests
from time import sleep

big_clock = BackgroundScheduler()
sched = BlockingScheduler()

# 每5秒確認一次是否開台
@sched.scheduled_job('interval', minutes=0.083)
def scan_channel():
    # twitch API設定
    user_id = '41700552'  # poposing user_id
    # test_id = '71092938'
    url = ''  # api_url
    auth = ''
    channel_info = requests.get(url, headers=auth).json().get('data')
    # print('沒開台拉')
    if channel_info:
        channel_title = channel_info[0].get('title')
        channel_game = channel_info[0].get('game_name')
        channel_streamer = channel_info[0].get('user_login')
        print('開台了')
        # poposing notify.py 內之函數送出訊息說開台了
        notification(channel_title, channel_game, channel_streamer)
        # 暫停搜尋是否開台
        sched.pause()
        # 確認是否關台
        while True:
            if not channel_info:
                print('關台了')
                # 確認關台 恢復搜尋是否開台
                sched.resume()


@big_clock.scheduled_job('interval', minutes=20)
def scheduled_job():
    print('欸醒醒 20分鐘了')
    url = 'https://poposing-streaming-notify.herokuapp.com/'
    r = requests.get(url)
    print(r)


big_clock.start()
sched.start()
