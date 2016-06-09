from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstore.mongodb import MongoDBJobStore
import apscheduler

import pytz

jobstores = {
	'mongo':MongoDBJobStore()
}

scheduler = BackgroundScheduler(jobstores = jobstores, timezone=pytz.timezone('US/EASTERN'))


scheduler.start()


