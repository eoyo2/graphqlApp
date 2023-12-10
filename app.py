from flask import Flask, render_template
import requests
import pandas as pd

app = Flask(__name__)

# GitHub GraphQL API endpoint
api_url = 'https://api.github.com/graphql'

# GitHub GraphQL query
graphql_query = '''
    query {
        viewer {
            login
            repositories(first: 5) {
                nodes {
                    name
                    description
                }
            }
        }
    }
'''

# Replace 'YOUR_GITHUB_TOKEN' with your GitHub personal access token
github_token = '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'

# Function to fetch GitHub repository data
def get_repo_data(github_token=github_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {github_token}'
    }
    response = requests.post(api_url, json={'query': graphql_query}, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        repositories_data = response_json.get("data", {}).get("viewer", {}).get("repositories", {}).get("nodes", [])
        df = pd.json_normalize(repositories_data)
        return df.to_html()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

@app.route('/')
def display_repo_data():
    repo_data_html = get_repo_data()
    return render_template('repo_data.html', repo_data_html=repo_data_html)

if __name__ == '__main__':
    app.run(debug=True)
