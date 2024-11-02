import schedule
import time
import os

print('Scheduler initialised')
schedule.every(1).minutes.do(lambda: os.system('scrapy crawl yahoo_finance -o results.json'))
print('Next job is set to run at: ' + str(schedule.next_run()))

while True:
    schedule.run_pending()
    time.sleep(1)
