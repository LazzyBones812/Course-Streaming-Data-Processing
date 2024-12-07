import schedule
import time
import os

import confluent_kafka
from confluent_kafka.admin import AdminClient, ConfigResource, NewTopic

conf = {'bootstrap.servers': 'kafka:29092'}
adminClient = AdminClient(conf)
adminClient.create_topics([NewTopic("some_topic", 1, 1)])
adminClient.create_topics([NewTopic("res_topic", 1, 1)])
topic_config = ConfigResource(confluent_kafka.admin.RESOURCE_TOPIC, name='res_topic')
topic_config.set_config('retention.ms', '300000', overwrite=True)
topic_config.set_config('segment.ms', '300000', overwrite=True)
# topic_config.set_config('log.retention.check.interval.ms', '5000', overwrite=True) # Как оказалось, так нельзя делать
adminClient.alter_configs([topic_config])

print('Scheduler initialised')
schedule.every(5).minutes.do(lambda: os.system('scrapy crawl yahoo_finance -o results.json'))
schedule.every(5).minutes.do(lambda: os.system('python consumer_kafka.py'))
print('Next job is set to run at: ' + str(schedule.next_run()))

while True:
    schedule.run_pending()
    time.sleep(1)
