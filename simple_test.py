#!/usr/bin/env python3
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class SimpleAITest:
    def __init__(self, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def create_branch_and_pr(self, branch_name, file_content, commit_msg, pr_title, pr_description):
        try:
            # Get main branch SHA
            response = requests.get(f"{self.base_url}/git/refs/heads/main", headers=self.headers)
            main_sha = response.json()['object']['sha']
            
            # Create branch
            branch_data = {"ref": f"refs/heads/{branch_name}", "sha": main_sha}
            requests.post(f"{self.base_url}/git/refs", headers=self.headers, json=branch_data)
            
            # Create file
            encoded_content = base64.b64encode(file_content.encode()).decode()
            file_data = {
                "message": commit_msg,
                "content": encoded_content,
                "branch": branch_name
            }
            requests.put(f"{self.base_url}/contents/test_{branch_name.replace('/', '_')}.py", 
                        headers=self.headers, json=file_data)
            
            # Create PR
            pr_data = {"title": pr_title, "head": branch_name, "base": "main", "body": pr_description}
            response = requests.post(f"{self.base_url}/pulls", headers=self.headers, json=pr_data)
            
            if response.status_code == 201:
                pr_number = response.json()['number']
                print(f"✅ Created PR #{pr_number}: {pr_title}")
                print(f"🔗 https://github.com/{self.repo_owner}/{self.repo_name}/pull/{pr_number}")
                return pr_number
            else:
                print(f"❌ Failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

def run_tests():
    # UPDATE THIS WITH YOUR GITHUB USERNAME
    tester = SimpleAITest("RubyShe", "ai-detection-validation")
    
    print("🧪 Testing ai-pr-watcher detection")
    print("=" * 40)
    
    # Test 1: copilot/ branch (should be detected)
    print("\n🧪 Test 1: copilot/ branch")
    tester.create_branch_and_pr(
        "copilot/simple-test",
        'def hello():\n    print("Hello!")\n\nhello()',
        "Add hello function",
        "Test: Hello function",
        "Simple test with copilot/ branch"
    )
    
    # Test 2: normal branch (should NOT be detected)
    print("\n🧪 Test 2: normal branch + AI code")  
    tester.create_branch_and_pr(
        "feature/ai-fibonacci",
        '''def fibonacci(n):
    """Generated with ChatGPT"""
    if n <= 0: return []
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence

print(fibonacci(10))''',
        "Add ChatGPT fibonacci",
        "Test: AI Fibonacci", 
        "**Generated with ChatGPT** - AI code with normal branch"
    )
    
    print("\n🎯 Expected: Only Test 1 detected by ai-pr-watcher")

if __name__ == "__main__":
    run_tests()
