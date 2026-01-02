from leaderboard_system import LeaderboardManager
import os

def update_readme():
    lm = LeaderboardManager()
    leaderboard_md = lm.get_leaderboard_markdown()
    
    readme_path = "README.md"
    with open(readme_path, "r") as f:
        content = f.read()
        
    # Check if leaderboard section exists
    start_marker = "## 🏆 LLM Leaderboard"
    if start_marker in content:
        # Replace existing section
        # Assuming it ends at the next ## or end of file
        start_idx = content.find(start_marker)
        end_idx = content.find("\n## ", start_idx + len(start_marker))
        
        if end_idx == -1:
            new_content = content[:start_idx] + leaderboard_md
        else:
            new_content = content[:start_idx] + leaderboard_md + content[end_idx:]
    else:
        # Append to end or after "Status" section
        # Let's put it after "Project Overview"
        insert_marker = "## Project Overview"
        insert_idx = content.find(insert_marker)
        if insert_idx != -1:
            # Find end of Overview section (next ##)
            next_section = content.find("\n## ", insert_idx + len(insert_marker))
            if next_section != -1:
                new_content = content[:next_section] + "\n\n" + leaderboard_md + content[next_section:]
            else:
                new_content = content + "\n\n" + leaderboard_md
        else:
            new_content = content + "\n\n" + leaderboard_md
            
    with open(readme_path, "w") as f:
        f.write(new_content)
    print("README.md updated with leaderboard.")

if __name__ == "__main__":
    update_readme()
