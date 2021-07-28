import looker_sdk
import csv
import exceptions

####Initialize API/SDK for more info go here: https://pypi.org/project/looker-sdk/
from looker_sdk import methods, models40
sdk = looker_sdk.init40("../looker.ini")

#### GO TO ADMIN --> GROUPS AND FIND THE GROUP ID YOU WANT TO ADD THE PEOPLE TO. ADD IT BELOW
### Alternative would be to use the search groups endpoint

sdk.search_groups()
def add_csv_of_users_to_group(group_id:int, file_path:str):
    data = []
    i=0
    with open(file_path) as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            data.append(str(row[i]))

    ### loops through list and searches user
    ### grabs user id and passes that through add user to group        
    try:
        for email in data:
            for user in sdk.search_users(email=email):
                sdk.add_group_user(group_id=group_id, body=models40.GroupIdForGroupUserInclusion(user_id= user.id))
    except KeyError:
        print('Key error \n')
        print(email)
        pass
    except TypeError:
        print('Type error \n')
        print(email)
        pass
    except IndexError:
        print('Index error \n')
        print(email)
        pass