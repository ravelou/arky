import os, re



date = re.compile('.*([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9]):([0-9][0-9]):([0-9][0-9]).*')

last_forged = os.popen("cat /home/ark/ark-node/logs/ark.log | grep Forged | tail -n 1").read().strip()
server_time = os.popen("date --rfc-3339=seconds").read().strip()

tuple1 = date.match(server_time).groups()
tuple2 = date.match(last_forged).groups()
date1 = datetime.datetime(*(int(e) for e in tuple1))
date2 = datetime.datetime(*(int(e) for e in tuple2))
delta = date2 - date1
delay = abs(delta.total_seconds())/60

if delay > 20:
	# update node and restart
	pass
