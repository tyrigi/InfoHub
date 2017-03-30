from jira import JIRA

# For now, doing basic auth. Need to move to OAUTH in the future
jira = JIRA('https://jira.allseenalliance.org', basic_auth=('tyler_gilbert', 'gonnabegood'))

assigned_issues = jira.search_issues('project=ASACORE and issuetype=Bug and assignee=currentUser() and status!=Closed')
print("Currently assigned issues:")
if not assigned_issues:
    print("None")
else:
    for issue in assigned_issues:
        print(issue)

recently_logged = jira.search_issues('project=ASACORE and issuetype=Bug and created>=-1w')
print("\nIssues logged in the last week:")
if not recently_logged:
    print("Nothing in the last week.")
else:
    for issue in recently_logged:
        print(issue,": ",issue.fields.summary)
