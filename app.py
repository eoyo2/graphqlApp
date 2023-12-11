from flask import Flask, render_template
import requests
import pandas as pd

app = Flask(__name__)

# GitHub GraphQL API endpoint
api_url = 'https://api.github.com/graphql'

# GitHub GraphQL query
graphql_query = '''
query Nodes {
  repository(owner: "eoyo2", name: "graphqlApp") {
    defaultBranchRef {
      target {
        ... on Commit {
          history(first: 10) {
            edges {
              node {
                message
                oid
                author {
                  name
                  email
                  date
                }
              }
            }
          }
        }
      }
    }
  }
}
'''

# Replace 'YOUR_GITHUB_TOKEN' with your GitHub personal access token
with open('config.txt','r') as f:
    github_token = f.readlines()[0]

# Function to fetch GitHub repository data
def get_repo_data():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {github_token}'
    }
    response = requests.post(api_url, json={'query': graphql_query}, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        commit_history = response_json['data']['repository']['defaultBranchRef']['target']['history']['edges']
        flattened_data = pd.json_normalize([commit['node'] for commit in commit_history])
        return flattened_data.to_html()
        #return response_json
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

@app.route('/')
def display_repo_data():
    repo_data_html = get_repo_data()
    return render_template('repo_data.html', repo_data_html=repo_data_html)

if __name__ == '__main__':
    app.run(debug=True)
