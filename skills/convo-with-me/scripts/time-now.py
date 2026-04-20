#! python
# print the date and time in format 202604151121

from datetime import datetime
now = datetime.now()
print(now.strftime("%Y%m%d%H%M"))