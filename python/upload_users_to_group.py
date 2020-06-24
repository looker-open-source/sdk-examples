import looker_sdk
import csv


import exceptions
####Initialize API/SDK for more info go here: https://pypi.org/project/looker-sdk/
from looker_sdk import methods31, models
sdk = looker_sdk.init31()  # or init40() for v4.0 API
me = sdk.me()
#print(me)

#### GO TO ADMIN --> GROUPS AND FIND THE GROUP ID YOU WANT TO ADD THE PEOPLE TO. ADD IT BELOW
group = 28
data = []
i=0
with open('~/file.csv') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        data.append(str(row[i]))

### loops through list and searches user
### grabs user id and passes that through add user to group        
try:
    for email in data:
        for user in sdk.search_users(email=email):
            sdk.add_group_user(group_id=group, body=models.GroupIdForGroupUserInclusion(user_id= user.id))
except KeyError:
    print('Key error \n')
    print(email)
    pass
except TypeError:
    print('Key error \n')
    print(email)
    pass
except IndexError:
    print('Index error \n')
    print(email)
    pass
