#!/usr/bin/env python3
"""
AI Ecosystem Mapper for ai-pr-watcher Dataset

Maps the complete AI tool ecosystem for each PR in ai-pr-watcher's dataset:
- WHO created the PR (primary AI tool/bot)
- WHAT other AI tools were used during the PR lifecycle
"""

import requests
import json
import time
import re
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class AIEcosystemMapper:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Define AI tool patterns for detection
        self.ai_tool_patterns = {
            # Major AI Coding Tools
            'chatgpt': [
                'chatgpt', 'chat-gpt', 'gpt-4', 'gpt-3.5', 'gpt-3', 'openai gpt',
                'generated with chatgpt', 'chatgpt helped', 'used chatgpt', 'chatgpt suggested',
                'ask chatgpt', 'chatgpt says', 'according to chatgpt'
            ],
            'github_copilot': [
                'github copilot', 'copilot', 'gh copilot', 'copilot suggested',
                'copilot generated', 'with copilot', 'copilot helped', 'copilot says',
                'copilot completion', 'copilot auto', 'thanks copilot'
            ],
            'claude': [
                'claude', 'anthropic claude', 'claude ai', 'claude helped', 'claude says',
                'generated with claude', 'claude suggested', 'asked claude', 'claude thinks',
                'claude code', 'claude-code'
            ],
            'codex': [
                'codex', 'openai codex', 'codex generated', 'with codex', 'codex says',
                'codex completion', 'codex helped'
            ],
            'cursor': [
                'cursor ai', 'cursor', 'cursor suggested', 'cursor helped', 'with cursor',
                'cursor completion', 'cursor says'
            ],
            'devin': [
                'devin', 'devin ai', 'devin-ai', 'devin generated', 'devin says',
                'devin helped', 'devin suggested'
            ],
            'codewhisperer': [
                'codewhisperer', 'code whisperer', 'amazon codewhisperer', 'aws codewhisperer'
            ],
            'tabnine': [
                'tabnine', 'tab nine', 'tabnine completion', 'tabnine suggested'
            ],
            'cody': [
                'cody ai', 'sourcegraph cody', 'cody', 'cody helped', 'cody suggested'
            ],
            'general_ai': [
                'ai assisted', 'ai generated', 'ai helped', 'ai suggestion', 'ai tool',
                'artificial intelligence', 'machine learning', 'neural network',
                'large language model', 'llm', 'ai model', 'ai review', 'ai analysis'
            ]
        }
        
        # Define primary creator detection patterns
        self.creator_patterns = {
            'devin': {
                'bot_accounts': ['devin-ai-integration[bot]', 'devin-ai[bot]'],
                'branch_patterns': ['devin/', 'devin-'],
                'commit_patterns': ['devin:', 'by devin']
            },
            'codegen': {
                'bot_accounts': ['codegen-sh[bot]', 'codegen[bot]'],
                'branch_patterns': ['codegen/', 'codegen-'],
                'commit_patterns': ['codegen:', 'by codegen']
            },
            'github_copilot': {
                'bot_accounts': ['github-copilot[bot]'],
                'branch_patterns': ['copilot/', 'copilot-'],
                'commit_patterns': ['copilot:', 'by copilot']
            },
            'codex': {
                'bot_accounts': ['openai-codex[bot]'],
                'branch_patterns': ['codex/', 'codex-'],
                'commit_patterns': ['codex:', 'by codex']
            },
            'cursor': {
                'bot_accounts': ['cursor[bot]', 'cursor-ai[bot]'],
                'branch_patterns': ['cursor/', 'cursor-'],
                'commit_patterns': ['cursor:', 'by cursor']
            }
        }
    
    def get_ai_pr_watcher_prs(self, limit=50):
        """Get PRs from ai-pr-watcher's detection patterns."""
        print("🔍 Collecting PRs from ai-pr-watcher dataset...")
        
        # ai-pr-watcher's search patterns
        search_queries = [
            'is:pr head:copilot/',
            'is:pr head:codex/',
            'is:pr head:cursor/',
            'is:pr author:devin-ai-integration[bot]',
            'is:pr author:codegen-sh[bot]'
        ]
        
        ai_prs = []
        
        for query in search_queries:
            print(f"   📋 Searching: {query}")
            
            search_url = "https://api.github.com/search/issues"
            params = {
                'q': query,
                'sort': 'updated',
                'order': 'desc',
                'per_page': min(20, limit)  # Limit per query
            }
            
            try:
                response = requests.get(search_url, headers=self.headers, params=params)
                if response.status_code == 200:
                    results = response.json()
                    found_count = len(results['items'])
                    print(f"      ✅ Found {found_count} PRs")
                    
                    for pr in results['items']:
                        repo_parts = pr['repository_url'].split('/')
                        pr_info = {
                            'pr_number': pr['number'],
                            'title': pr['title'],
                            'url': pr['html_url'],
                            'repo_owner': repo_parts[-2],
                            'repo_name': repo_parts[-1],
                            'detection_query': query,
                            'state': pr['state'],
                            'created_at': pr['created_at'],
                            'updated_at': pr['updated_at'],
                            'author': pr['user']['login'],
                            'body': pr.get('body', '')
                        }
                        ai_prs.append(pr_info)
                else:
                    print(f"      ❌ Error: {response.status_code}")
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"      ❌ Error: {e}")
        
        # Remove duplicates based on URL
        unique_prs = {}
        for pr in ai_prs:
            unique_prs[pr['url']] = pr
        
        final_prs = list(unique_prs.values())[:limit]
        print(f"📊 Total unique PRs collected: {len(final_prs)}")
        
        return final_prs
    
    def identify_primary_creator(self, pr_data):
        """Identify the primary AI tool that created the PR."""
        author = pr_data['author'].lower()
        detection_query = pr_data['detection_query']
        
        # Check bot accounts first (most reliable)
        for tool_name, patterns in self.creator_patterns.items():
            if author in [bot.lower() for bot in patterns['bot_accounts']]:
                return {
                    'primary_creator': tool_name,
                    'confidence': 'high',
                    'evidence': f"Bot account: {pr_data['author']}"
                }
        
        # Check branch patterns from detection query
        if 'head:copilot/' in detection_query:
            return {
                'primary_creator': 'github_copilot',
                'confidence': 'medium',
                'evidence': 'Branch pattern: copilot/'
            }
        elif 'head:codex/' in detection_query:
            return {
                'primary_creator': 'codex',
                'confidence': 'medium',
                'evidence': 'Branch pattern: codex/'
            }
        elif 'head:cursor/' in detection_query:
            return {
                'primary_creator': 'cursor',
                'confidence': 'low',
                'evidence': 'Branch pattern: cursor/ (cursor is primarily an IDE)'
            }
        
        # If no clear pattern, mark as unknown
        return {
            'primary_creator': 'unknown',
            'confidence': 'low',
            'evidence': f"Author: {pr_data['author']}, Query: {detection_query}"
        }
    
    def scan_pr_for_ai_tools(self, pr_data):
        """Scan entire PR lifecycle for AI tool mentions."""
        repo_owner = pr_data['repo_owner']
        repo_name = pr_data['repo_name']
        pr_number = pr_data['pr_number']
        
        print(f"   🔍 Scanning {repo_owner}/{repo_name} PR #{pr_number}")
        
        ai_tools_found = {}  # tool_name -> [evidence_list]
        
        # Scan PR title and description
        pr_text = (pr_data['title'] + ' ' + pr_data.get('body', '')).lower()
        
        for tool_name, patterns in self.ai_tool_patterns.items():
            for pattern in patterns:
                if pattern in pr_text:
                    if tool_name not in ai_tools_found:
                        ai_tools_found[tool_name] = []
                    ai_tools_found[tool_name].append({
                        'location': 'PR description',
                        'pattern': pattern,
                        'context': self._extract_context(pr_text, pattern)
                    })
        
        # Scan PR comments
        comment_evidence = self._scan_pr_comments(repo_owner, repo_name, pr_number)
        for tool_name, evidence_list in comment_evidence.items():
            if tool_name not in ai_tools_found:
                ai_tools_found[tool_name] = []
            ai_tools_found[tool_name].extend(evidence_list)
        
        # Scan code review comments
        review_evidence = self._scan_review_comments(repo_owner, repo_name, pr_number)
        for tool_name, evidence_list in review_evidence.items():
            if tool_name not in ai_tools_found:
                ai_tools_found[tool_name] = []
            ai_tools_found[tool_name].extend(evidence_list)
        
        # Scan commit messages
        commit_evidence = self._scan_commit_messages(repo_owner, repo_name, pr_number)
        for tool_name, evidence_list in commit_evidence.items():
            if tool_name not in ai_tools_found:
                ai_tools_found[tool_name] = []
            ai_tools_found[tool_name].extend(evidence_list)
        
        return ai_tools_found
    
    def _scan_pr_comments(self, repo_owner, repo_name, pr_number):
        """Scan PR issue comments for AI tool mentions."""
        ai_evidence = {}
        
        try:
            comments_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
            response = requests.get(comments_url, headers=self.headers)
            
            if response.status_code == 200:
                comments = response.json()
                
                for comment in comments:
                    comment_body = comment.get('body', '').lower()
                    comment_author = comment['user']['login']
                    comment_date = comment['created_at']
                    
                    for tool_name, patterns in self.ai_tool_patterns.items():
                        for pattern in patterns:
                            if pattern in comment_body:
                                if tool_name not in ai_evidence:
                                    ai_evidence[tool_name] = []
                                ai_evidence[tool_name].append({
                                    'location': 'PR comment',
                                    'pattern': pattern,
                                    'author': comment_author,
                                    'date': comment_date,
                                    'context': self._extract_context(comment_body, pattern)
                                })
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"      ❌ Error scanning comments: {e}")
        
        return ai_evidence
    
    def _scan_review_comments(self, repo_owner, repo_name, pr_number):
        """Scan PR code review comments for AI tool mentions."""
        ai_evidence = {}
        
        try:
            review_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/comments"
            response = requests.get(review_url, headers=self.headers)
            
            if response.status_code == 200:
                review_comments = response.json()
                
                for comment in review_comments:
                    comment_body = comment.get('body', '').lower()
                    comment_author = comment['user']['login']
                    file_path = comment.get('path', 'Unknown')
                    
                    for tool_name, patterns in self.ai_tool_patterns.items():
                        for pattern in patterns:
                            if pattern in comment_body:
                                if tool_name not in ai_evidence:
                                    ai_evidence[tool_name] = []
                                ai_evidence[tool_name].append({
                                    'location': 'Code review comment',
                                    'pattern': pattern,
                                    'author': comment_author,
                                    'file': file_path,
                                    'context': self._extract_context(comment_body, pattern)
                                })
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"      ❌ Error scanning review comments: {e}")
        
        return ai_evidence
    
    def _scan_commit_messages(self, repo_owner, repo_name, pr_number):
        """Scan commit messages for AI tool mentions."""
        ai_evidence = {}
        
        try:
            commits_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/commits"
            response = requests.get(commits_url, headers=self.headers)
            
            if response.status_code == 200:
                commits = response.json()
                
                for commit in commits:
                    commit_message = commit['commit']['message'].lower()
                    commit_sha = commit['sha'][:8]
                    commit_author = commit['commit']['author']['name']
                    
                    for tool_name, patterns in self.ai_tool_patterns.items():
                        for pattern in patterns:
                            if pattern in commit_message:
                                if tool_name not in ai_evidence:
                                    ai_evidence[tool_name] = []
                                ai_evidence[tool_name].append({
                                    'location': 'Commit message',
                                    'pattern': pattern,
                                    'commit_sha': commit_sha,
                                    'author': commit_author,
                                    'context': self._extract_context(commit_message, pattern)
                                })
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"      ❌ Error scanning commits: {e}")
        
        return ai_evidence
    
    def _extract_context(self, text, pattern, context_length=80):
        """Extract context around found pattern."""
        try:
            pattern_pos = text.find(pattern)
            if pattern_pos == -1:
                return text[:context_length].strip()
            
            start = max(0, pattern_pos - context_length//2)
            end = min(len(text), pattern_pos + len(pattern) + context_length//2)
            
            context = text[start:end].strip()
            return context
        except:
            return text[:context_length].strip()
    
    def analyze_pr_ai_ecosystem(self, pr_data):
        """Complete AI ecosystem analysis for a single PR."""
        # Identify primary creator
        primary_creator = self.identify_primary_creator(pr_data)
        
        # Scan for all AI tool mentions
        ai_tools_found = self.scan_pr_for_ai_tools(pr_data)
        
        # Compile results
        analysis = {
            'pr_info': {
                'url': pr_data['url'],
                'repo': f"{pr_data['repo_owner']}/{pr_data['repo_name']}",
                'pr_number': pr_data['pr_number'],
                'title': pr_data['title'],
                'author': pr_data['author'],
                'state': pr_data['state']
            },
            'primary_creator': primary_creator,
            'ai_tools_detected': ai_tools_found,
            'ai_tool_count': len(ai_tools_found),
            'ai_tool_names': list(ai_tools_found.keys()),
            'is_multi_ai': len(ai_tools_found) > 1
        }
        
        return analysis
    
    def run_ecosystem_mapping(self, max_prs=30):
        """Run complete AI ecosystem mapping on ai-pr-watcher dataset."""
        print("🤖 AI Ecosystem Mapper for ai-pr-watcher Dataset")
        print("="*70)
        print("🎯 Goal: Map WHO created each PR and WHAT other AI tools were used")
        print()
        
        # Get PRs from ai-pr-watcher dataset
        ai_prs = self.get_ai_pr_watcher_prs(max_prs)
        
        if not ai_prs:
            print("❌ No PRs found in ai-pr-watcher dataset")
            return
        
        print(f"\n🔄 Analyzing {len(ai_prs)} PRs for complete AI ecosystem...")
        
        ecosystem_results = []
        
        for i, pr_data in enumerate(ai_prs, 1):
            print(f"\n📄 [{i}/{len(ai_prs)}] Analyzing PR: {pr_data['url']}")
            
            analysis = self.analyze_pr_ai_ecosystem(pr_data)
            ecosystem_results.append(analysis)
            
            # Show immediate results
            creator = analysis['primary_creator']['primary_creator']
            ai_count = analysis['ai_tool_count']
            ai_tools = ', '.join(analysis['ai_tool_names'])
            
            print(f"      🤖 Primary Creator: {creator}")
            print(f"      🔧 AI Tools Found: {ai_count} ({ai_tools})")
            
            if analysis['is_multi_ai']:
                print(f"      ✅ Multi-AI ecosystem detected!")
            
            # Rate limiting between PRs
            time.sleep(1)
        
        # Generate comprehensive report
        self._generate_ecosystem_report(ecosystem_results)
        
        # Save detailed results
        self._save_ecosystem_results(ecosystem_results)
        
        return ecosystem_results
    
    def _generate_ecosystem_report(self, results):
        """Generate comprehensive AI ecosystem report."""
        print("\n" + "="*80)
        print("🤖 AI ECOSYSTEM MAPPING REPORT")
        print("="*80)
        
        total_prs = len(results)
        multi_ai_prs = len([r for r in results if r['is_multi_ai']])
        
        print(f"📊 Total PRs analyzed: {total_prs}")
        print(f"🔧 PRs with multiple AI tools: {multi_ai_prs} ({multi_ai_prs/total_prs*100:.1f}%)")
        
        # Primary creators analysis
        creators = {}
        for result in results:
            creator = result['primary_creator']['primary_creator']
            creators[creator] = creators.get(creator, 0) + 1
        
        print(f"\n👥 PRIMARY CREATORS:")
        for creator, count in sorted(creators.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_prs) * 100
            print(f"   {creator}: {count} PRs ({percentage:.1f}%)")
        
        # AI tool frequency
        tool_frequency = {}
        for result in results:
            for tool in result['ai_tool_names']:
                tool_frequency[tool] = tool_frequency.get(tool, 0) + 1
        
        print(f"\n🔧 AI TOOL USAGE FREQUENCY:")
        for tool, count in sorted(tool_frequency.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_prs) * 100
            print(f"   {tool}: {count} PRs ({percentage:.1f}%)")
        
        # Multi-AI ecosystems
        if multi_ai_prs > 0:
            print(f"\n🌐 MULTI-AI ECOSYSTEMS:")
            multi_ai_results = [r for r in results if r['is_multi_ai']]
            
            for result in multi_ai_results[:5]:  # Show top 5
                pr_info = result['pr_info']
                creator = result['primary_creator']['primary_creator']
                tools = ', '.join(result['ai_tool_names'])
                
                print(f"\n   📄 {pr_info['repo']} PR #{pr_info['pr_number']}")
                print(f"      🔗 {pr_info['url']}")
                print(f"      🤖 Creator: {creator}")
                print(f"      🔧 AI Tools: {tools}")
                print(f"      📝 Title: {pr_info['title'][:60]}...")
        
        # Key insights
        print(f"\n💡 KEY INSIGHTS:")
        
        # Creator with most multi-AI usage
        creator_multi_ai = {}
        for result in results:
            if result['is_multi_ai']:
                creator = result['primary_creator']['primary_creator']
                creator_multi_ai[creator] = creator_multi_ai.get(creator, 0) + 1
        
        if creator_multi_ai:
            top_multi_creator = max(creator_multi_ai.items(), key=lambda x: x[1])
            print(f"   • {top_multi_creator[0]} PRs most likely to involve other AI tools ({top_multi_creator[1]} cases)")
        
        # Most common tool combinations
        combinations = {}
        for result in results:
            if result['is_multi_ai']:
                tools = tuple(sorted(result['ai_tool_names']))
                combinations[tools] = combinations.get(tools, 0) + 1
        
        if combinations:
            top_combo = max(combinations.items(), key=lambda x: x[1])
            print(f"   • Most common AI combination: {' + '.join(top_combo[0])} ({top_combo[1]} times)")
        
        print(f"   • Average AI tools per PR: {sum(r['ai_tool_count'] for r in results) / total_prs:.1f}")
    
    def _save_ecosystem_results(self, results, filename="ai_ecosystem_mapping.json"):
        """Save detailed ecosystem mapping results."""
        # Prepare data for JSON serialization
        serializable_results = []
        for result in results:
            serializable_result = {
                'pr_info': result['pr_info'],
                'primary_creator': result['primary_creator'],
                'ai_tools_detected': {
                    tool: [
                        {k: v for k, v in evidence.items() if k != 'context'} 
                        for evidence in evidence_list
                    ]
                    for tool, evidence_list in result['ai_tools_detected'].items()
                },
                'ai_tool_count': result['ai_tool_count'],
                'ai_tool_names': result['ai_tool_names'],
                'is_multi_ai': result['is_multi_ai']
            }
            serializable_results.append(serializable_result)
        
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to {filename}")

def main():
    """Main function to run AI ecosystem mapping."""
    mapper = AIEcosystemMapper()
    
    # Run the complete ecosystem mapping
    results = mapper.run_ecosystem_mapping(max_prs=20)  # Start with 20 PRs
    
    print(f"\n🎯 Ecosystem mapping complete!")
    print(f"📊 Analyzed {len(results)} PRs from ai-pr-watcher dataset")
    print(f"🔍 Found complete AI tool ecosystem for each PR")

if __name__ == "__main__":
    main()
