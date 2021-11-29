from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')
def scheduled_job():
    url = "https://poposing-streaming-notify.herokuapp.com/"
    call_url = requests.get(url)

    print(call_url)


sched.start()
