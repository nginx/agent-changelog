import requests  # Importing requests library to make HTTP requests
from bs4 import BeautifulSoup  # Importing BeautifulSoup library to parse HTML content
from jinja2 import Template  # Importing Template from jinja2 for template rendering
import argparse  # Importing argparse for command-line argument parsing
import re  # Importing re module for regular expressions
import os # Importing os module to retrieve github token for draft release

def get_draft_releases():
    token = os.getenv('GITHUB_TOKEN')
    if token:
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        repo = 'spencerugbo/changelog-test'
        url = f'https://api.github.com/repos/{repo}/releases'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
        
            all_changes = []
            releases = response.json()
            for release in releases:
                release_version = release['tag_name']
                if release_version:
                    changes_section = release['body']
                    if changes_section:
                        changes = {}
                        changelog = parse_release_notes(changes_section)
                        for heading, content in changelog.items():
                            if content:
                                changes[heading] = content
                        all_changes.append({'release_version': release_version, 'changes': changes})

            return all_changes

        else:
            print(f"Failed to get releases: {response.status_code}")
            print(response.json())
    else:
        print("GitHub token not found, cannot access repository")
        

def parse_release_notes(release_notes):
    headings = ['🌟 Highlights', '🚀 Features', '🐛 Bug Fixes', '📝 Documentation', '⬆️ Dependencies', '🔨 Maintenance']

    changelog = {heading: [] for heading in headings}
    
    pattern = r"(### ({}))\r?\n((?:\*.*(?:\r?\n|$))+)"
    regex_pattern = pattern.format('|'.join(re.escape(heading) for heading in headings))
    
    matches = re.findall(regex_pattern, release_notes)
    
    for match in matches:
        heading, _, content = match
        heading = heading.replace('### ', '')
        changes = content.strip().splitlines()
        changelog[heading].extend([convert_links(re.sub(r'^\*\s*', '', change.strip())) for change in changes])

    changelog = {k: v for k, v in changelog.items() if v}
    
    return changelog

def convert_links(change):
    usernames = re.findall(r'@(\w+)', change)

    for username in usernames:
        change = change.replace(f'@{username}', f'[@{username}](https://github.com/{username})')

    pr_link_match = re.search(r'https://github.com/([\w-]+)/([\w-]+)/pull/(\d+)', change)
    if pr_link_match:
        repo_name = pr_link_match.group(2)
        pr_number = pr_link_match.group(3)
        pr_link = pr_link_match.group(0)
        change = change.replace(pr_link, f'[{repo_name}#{pr_number}]({pr_link})')
    
    return change

def remove_extra_blank_lines(file_path):
    """Function to remove extra blank lines from a file"""
    with open(file_path, 'r') as f:
        lines = f.readlines()  # Reading lines from file
    modified_lines = []  # List to store modified lines
    is_previous_line_blank = False  # Flag to track previous blank line
    for line in lines:
        if line.strip() == '':
            if not is_previous_line_blank:
                modified_lines.append(line)  # Appending line if it's not consecutive blank line
            is_previous_line_blank = True
        else:
            modified_lines.append(line)  # Appending non-blank line
            is_previous_line_blank = False
    with open(file_path, 'w') as f:
        f.writelines(modified_lines)  # Writing modified lines back to file

def remove_extra_lines(file_path):
    """Function to remove extra lines from the end of a file"""
    with open(file_path, 'r') as f:
        lines = f.readlines()  # Reading lines from file
    if len(lines) >= 2 and '---' in lines[-2]:
        del lines[-2]  # Removing '---' line if it's the 3rd to last line
    while len(lines) > 1 and lines[-1].strip() == '' and lines[-2].strip() == '':
        lines.pop()  # Removing consecutive blank lines at the end of file
    lines.pop()  # Removing last line which would be a blank line
    if lines[-1].strip() != '':
        lines.append('\n')  # Adding a single blank line at the end if it's not already there
    with open(file_path, 'w') as f:
        f.writelines(lines)  # Writing modified lines back to file

def main():
    """Main function to handle command-line arguments and generate changelog"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-r', '--repo', type=str, default='changelog-test', help='Repository to fetch content from')
    # args = parser.parse_args()  # Parsing command-line arguments
    all_changes = get_draft_releases()  # Parsing releases page
    if all_changes:
        template = Template(open('template.j2').read())  # Loading template for rendering
        output = template.render(all_changes=all_changes)  # Rendering template with changes data
        with open('changelog.md', 'w') as f:
            f.write(output)  # Writing rendered output to changelog file
        remove_extra_blank_lines('changelog.md')  # Removing extra blank lines from changelog
        remove_extra_lines('changelog.md')  # Removing extra lines from changelog

if __name__ == "__main__":
    main()  # Calling main function if script is executed directly