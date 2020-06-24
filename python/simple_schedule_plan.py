import looker_sdk

# from typing import cast, MutableSequence, Sequence

####Initialize API/SDK for more info go here: https://pypi.org/project/looker-sdk/
from looker_sdk import methods31, models
sdk = looker_sdk.init31()  # or init40() for v4.0 API
me = sdk.me()


### DEFINE VALUES HERE ####
# DASHBOARDID = VALUE
# USERID = VALUE
# SCHEDULETITLE = VALUE
# EMAIL = VALUE

#Simple Create schedule plan example
## For more information on the Params accepted https://github.com/looker-open-source/sdk-codegen/blob/master/python/looker_sdk/sdk/api31/methods.py#L2144
### And for schedule destination go: https://github.com/looker-open-source/sdk-codegen/blob/master/python/looker_sdk/sdk/api31/models.py#L4601
schedule = sdk.create_scheduled_plan(body=models.WriteScheduledPlan(name=SCHEDULETITLE, dashboard_id=DASHBOARDID, user_id=USERID, run_as_recipient= True, crontab="0 1 * * *", scheduled_plan_destination = [models.ScheduledPlanDestination(format="csv_zip", apply_formatting=True, apply_vis=True, address=EMAIL,  type="email", message="Aloha!")]))
