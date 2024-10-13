import os
import time
from dotenv import load_dotenv
from embeddings import CodebaseEmbeddings
from github_handler import GitHubHandler
from update_handler import UpdateHandler

def main():
    load_dotenv()

    # Initialize components
    embeddings = CodebaseEmbeddings()
    github = GitHubHandler(
        os.getenv("GITHUB_TOKEN"),
        os.getenv("GITHUB_REPO_OWNER"),
        os.getenv("GITHUB_REPO_NAME")
    )
    updater = UpdateHandler()

    print("AI Coder is running. Press Ctrl+C to stop.")
    
    try:
        while True:
            # Check for new issues
            new_issues = github.get_new_issues()
            
            for issue in new_issues:
                print(f"Processing issue #{issue.number}: {issue.title}")
                # Process each issue
                relevant_code = embeddings.search_relevant_code(issue.body)
                update_description = updater.generate_update(issue.body, relevant_code)
                
                # Create a new branch and pull request
                branch_name = f"update-{issue.number}"
                github.create_branch(branch_name)
                github.create_pull_request(branch_name, update_description, issue.number)
                print(f"Created pull request for issue #{issue.number}")
            
            # Wait for 5 minutes before checking for new issues again
            time.sleep(300)
    except KeyboardInterrupt:
        print("AI Coder stopped.")

if __name__ == "__main__":
    main()
