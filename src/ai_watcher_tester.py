import requests
import time
import json
import base64
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AIWatcherTester:
    def __init__(self, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = os.getenv('GITHUB_TOKEN')
        
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
        
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'AI-Detection-Research'
        }
        self.test_results = []
    
    def create_branch(self, branch_name):
        """Create a new branch from main"""
        print(f"Creating branch: {branch_name}")
        
        # Get main branch SHA
        response = requests.get(f"{self.base_url}/git/refs/heads/main", headers=self.headers)
        if response.status_code != 200:
            print(f"Error getting main branch: {response.status_code}")
            return False
        
        main_sha = response.json()['object']['sha']
        
        # Create new branch
        data = {
            "ref": f"refs/heads/{branch_name}",
            "sha": main_sha
        }
        
        response = requests.post(f"{self.base_url}/git/refs", headers=self.headers, json=data)
        if response.status_code == 201:
            print(f"✅ Branch '{branch_name}' created successfully")
            return True
        else:
            print(f"❌ Error creating branch: {response.status_code} - {response.text}")
            return False
    
    def create_file_in_branch(self, branch_name, file_path, content, commit_message):
        """Create a file in the specified branch"""
        print(f"Creating file: {file_path} in branch: {branch_name}")
        
        # Encode content to base64
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        
        data = {
            "message": commit_message,
            "content": encoded_content,
            "branch": branch_name
        }
        
        response = requests.put(f"{self.base_url}/contents/{file_path}", headers=self.headers, json=data)
        
        if response.status_code == 201:
            print(f"✅ File '{file_path}' created successfully")
            return True
        else:
            print(f"❌ Error creating file: {response.status_code} - {response.text}")
            return False
    
    def create_pull_request(self, branch_name, title, description, labels=None):
        """Create a pull request"""
        print(f"Creating PR from branch: {branch_name}")
        
        data = {
            "title": title,
            "head": branch_name,
            "base": "main",
            "body": description
        }
        
        response = requests.post(f"{self.base_url}/pulls", headers=self.headers, json=data)
        
        if response.status_code == 201:
            pr_data = response.json()
            pr_number = pr_data['number']
            print(f"✅ PR #{pr_number} created successfully")
            
            # Add labels if provided
            if labels:
                self.add_labels_to_pr(pr_number, labels)
            
            return pr_number
        else:
            print(f"❌ Error creating PR: {response.status_code} - {response.text}")
            return None
    
    def add_labels_to_pr(self, pr_number, labels):
        """Add labels to a pull request"""
        data = {"labels": labels}
        response = requests.post(f"{self.base_url}/issues/{pr_number}/labels", 
                               headers=self.headers, json=data)
        if response.status_code == 200:
            print(f"✅ Labels added to PR #{pr_number}: {labels}")
        else:
            print(f"❌ Error adding labels: {response.status_code}")
    
    def log_test_result(self, test_name, branch_name, pr_number, expected_detection, ai_involvement, notes):
        """Log test results for analysis"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "test_name": test_name,
            "branch_name": branch_name,
            "pr_number": pr_number,
            "pr_url": f"https://github.com/{self.repo_owner}/{self.repo_name}/pull/{pr_number}" if pr_number else None,
            "expected_detection": expected_detection,
            "actual_ai_involvement": ai_involvement,
            "notes": notes
        }
        self.test_results.append(result)
        return result
    
    def save_results(self, filename="test_results.json"):
        """Save test results to file"""
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"✅ Test results saved to {filename}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("AI-PR-WATCHER DETECTION TEST SUMMARY")
        print("="*80)
        
        for result in self.test_results:
            status = "✅ SUCCESS" if result['pr_number'] else "❌ FAILED"
            print(f"\n{status} {result['test_name']}")
            print(f"  Branch: {result['branch_name']}")
            print(f"  Expected Detection: {result['expected_detection']}")
            print(f"  Actual AI: {result['actual_ai_involvement']}")
            print(f"  PR: {result['pr_url'] or 'Not created'}")
            print(f"  Notes: {result['notes']}")
        
        print(f"\n📊 SUMMARY: {len([r for r in self.test_results if r['pr_number']])} PRs created successfully")
