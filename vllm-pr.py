import requests
from tabulate import tabulate
from datetime import datetime, timezone

# Retrieve open pull requests
open_url = 'https://api.github.com/repos/vllm-project/vllm/pulls?state=open&per_page=100'
# merged_url = 'https://api.github.com/repos/vllm-project/vllm/pulls?state=closed&per_page=100'
open_response = requests.get(open_url)
# merged_response = requests.get(merged_url)

authors = ['Yard1', 'cadedaniel', 'pcmoritz', 'tterrysun', 'rkooo567', 'xwjiang2010'] # , 'WoosukKwon', 'zhuohan123', 'simon-mo']
open_pr_table_data = []
# merged_pr_table_data = []

if open_response.status_code == 200:
    open_prs = open_response.json()

    for pr in open_prs:
        if pr['user']['login'] in authors and not pr['draft'] and "wip" not in pr['title'].lower():# and pr['state'] == 'open':
            pr_name = pr['title']
            pr_link = pr['html_url']
            author = pr['user']['login']
            assignee = pr['assignee']['login'] if pr['assignee'] else 'None'
            last_updated = pr['updated_at']
            # Convert last_updated to datetime object with timezone aware
            last_updated_dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
            # Make datetime.now timezone aware
            now_dt = datetime.now(timezone.utc)
            days_inactive = (now_dt - last_updated_dt).days

            # Check for PR approvals
            reviews_url = pr['review_comments_url'].replace('/comments', '/reviews')
            reviews_response = requests.get(reviews_url)
            approvals = False
            if reviews_response.status_code == 200:
                reviews = reviews_response.json()
                for review in reviews:
                    if review['state'] == 'APPROVED':
                        approvals = True
                        break

            open_pr_table_data.append([pr_name, pr_link, author, assignee, days_inactive, approvals])

    if open_pr_table_data:
        headers = ["PR Name", "PR Link", "Author", "Assignee", "Days Inactive", "Approved"]
        print("Open PRs:")
        print(tabulate(open_pr_table_data, headers=headers, tablefmt="pipe"))
    else:
        print(f"No open PRs found for authors {', '.join(authors)}")
else:
    print(f"Failed to fetch open pull requests. Status code: {open_response.status_code}")

# if merged_response.status_code == 200:
#     merged_prs = merged_response.json()

#     for pr in merged_prs:
#         if pr['user']['login'] in authors and pr['merged_at'] is not None:
#             pr_name = pr['title']
#             pr_link = pr['html_url']
#             author = pr['user']['login']
#             merged_at = pr['merged_at']
#             # Convert merged_at to datetime object with timezone aware
#             merged_at_dt = datetime.fromisoformat(merged_at.replace('Z', '+00:00'))
#             # Calculate days since merged
#             now_dt = datetime.now(timezone.utc)
#             days_since_merged = (now_dt - merged_at_dt).days

#             merged_pr_table_data.append([pr_name, pr_link, author, days_since_merged])

#     if merged_pr_table_data:
#         headers = ["PR Name", "PR Link", "Author", "Days Since Merged"]
#         print("Merged PRs:")
#         print(tabulate(merged_pr_table_data, headers=headers, tablefmt="pipe"))
#     else:
#         print(f"No merged PRs found for authors {', '.join(authors)}")
# else:
#     print(f"Failed to fetch merged pull requests. Status code: {merged_response.status_code}")
