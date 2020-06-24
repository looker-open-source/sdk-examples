from looker_sdk import init31, models31

sdk = init31("looker.ini")

all_groups = sdk.search_groups()
all_roles = sdk.search_roles()
all_users = sdk.all_users()

looker_groups = {}
looker_roles = {}
looker_existing_user_emails = []


for x in all_groups:
    looker_groups[x.name] = x.id

for x in all_roles:
    looker_roles[x.name] = x.id

for x in all_users:
    looker_existing_user_emails.append(x.email)

print("Hello There! It seems that you'd like to create some Looker users!\n")
print("These are all the paramters that you can assign to a new user:\n")
print("Current Looker Roles:")
print('\n'.join(looker_roles.keys() ))
print('\n')
print("Current Looker Groups:")
print('\n'.join(looker_groups.keys() ))
print('\n')

print("Let's get some details for that new user!")

email_existing_check = False

while email_existing_check == False:
    new_user_email = input("What is the new user's email? \n").lower()
    if new_user_email in looker_existing_user_emails:
        print("The user with this email already exists")
    else:
        email_existing_check = True



all_roles_for_new_user = []
continue_role_input = []
    
while 'n' not in continue_role_input:

    if len(all_roles_for_new_user) < 1:
        new_role_input = input(f"Enter the first role you'd like to assign to that user. Roles available: {', '.join(looker_roles)} \n").title()
    else:
        new_role_input = input(f"Enter the next role you'd like to assign to that user. Remaining roles available: {', '.join(set(looker_roles) - set(all_roles_for_new_user))}  \n").title()

    if not looker_roles.get(new_role_input):
            print("That role doesn't exist")
    else:
            all_roles_for_new_user.append(new_role_input)
            continue_role_input.append(input(f"Is there any other Role apart from {', '.join(set(all_roles_for_new_user))} that you'd like to assign to the new user? Type 'y' or 'n' \n").lower())




all_groups_for_new_user = []
continue_group_input = []

while 'n' not in continue_group_input:

    if len(all_groups_for_new_user) < 1:
        new_group_input = input(f"Enter the first group you'd like to assign to that user. Groups available: {', '.join(looker_groups)} \n").title()
    else:
        new_group_input = input(f"Enter the next group you'd like to assign to that user. Remaining groups available: {', '.join(set(looker_groups) - set(all_groups_for_new_user))}  \n").title()

    if not looker_groups.get(new_group_input):
            print("That group doesn't exist")
    else:
            all_groups_for_new_user.append(new_group_input)
            continue_group_input.append(input(f"Is there any other Group apart from {', '.join(set(all_groups_for_new_user))} that you'd like to assign to the new user? Type 'y' or 'n' \n").lower())



new_user_id = sdk.create_user({}).id

new_user = sdk.create_user_credentials_email(new_user_id, models31.WriteCredentialsEmail(
  email=f"{new_user_email}",
  forced_password_reset_at_next_login=True
))

roles = {k:v for k,v in looker_roles.items() if k in all_roles_for_new_user}
sdk.set_user_roles(new_user_id, list(roles.values()) )
print(f"Adding user {new_user_email} to roles {', '.join(list(roles.keys()))}")

for group in all_groups_for_new_user:
    print(f"Adding user {new_user_email} to group {group}")
    group_id = looker_groups[group]
    sdk.add_group_user(group_id, models31.GroupIdForGroupUserInclusion(
        user_id=new_user_id
    ))

print(f"User {new_user_email} created!")
