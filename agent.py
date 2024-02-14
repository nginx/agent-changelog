import requests  # Importing requests library to make HTTP requests
from bs4 import BeautifulSoup  # Importing BeautifulSoup library to parse HTML content
from jinja2 import Template  # Importing Template from jinja2 for template rendering
import argparse  # Importing argparse for command-line argument parsing
import re  # Importing re module for regular expressions

def get_url_content(url):
    """Function to fetch content from a given URL"""
    response = requests.get(url)  # Sending HTTP GET request to the URL
    if response.status_code == 200:  # Checking if request was successful
        return response.content  # Returning the content if successful
    else:
        print("Failed to fetch URL content")  # Printing error message if request fails
        return None

def parse_html(content, url):
    """Function to parse HTML content"""
    soup = BeautifulSoup(content, 'html.parser')  # Parsing HTML content using BeautifulSoup
    if url == 'https://github.com/nginx/agent/releases/':
        # Parsing releases page of nginx/agent repository on GitHub
        releases = soup.find_all('a', class_='Link--primary')  # Finding all release links
        all_changes = []  # List to store all changes
        for release in releases:
            release_version = release.text.strip()  # Getting the text of release version
            if re.match(r'^v\d+(\.\d+)*$', release_version):
                # Checking if the text matches the release version format
                release_url = 'https://github.com' + release['href']  # Building release URL
                release_content = get_url_content(release_url)  # Fetching release content
                if release_content:
                    _, changes = parse_html(release_content, '')  # Recursive call to parse release content
                    if changes:
                        all_changes.append({'release_version': release_version, 'changes': changes})
        return all_changes  # Returning all changes
    else:
        # Parsing individual release pages
        release_version_tag = soup.find('h1', string=re.compile(r'^v\d+(\.\d+)*'))
        # Finding release version tag
        if release_version_tag:
            release_version = release_version_tag.text.strip()  # Extracting release version
        else:
            return None  # Returning None if release version is not found
        changes_section = soup.find('h2', string="What's Changed")
        # Finding the section containing changes
        if changes_section:
            changes = {}  # Dictionary to store different types of changes
            for h3 in changes_section.find_all_next('h3'):
                label = h3.text.strip()  # Extracting label for changes
                if label in ['🚀 Features', '🐛 Bug Fixes', '📝 Documentation', '⬆️ Dependencies', '🔨 Maintenance']:
                    ul = h3.find_next_sibling('ul')  # Finding unordered list of changes
                    if ul:
                        changes[label] = [convert_links(li) for li in ul.find_all('li')]
                        # Converting links in list items and storing them in dictionary
            return release_version, changes  # Returning release version and changes
        else:
            return None, None  # Returning None if changes section is not found

def convert_links(li):
    """Function to convert links in list items"""
    new_text = ""  # String to store modified text
    for elem in li.contents:
        if elem.name == 'a':
            href = elem.get('href')  # Extracting URL from link
            text = elem.text  # Extracting link text
            if href and text:
                new_text += f'[{text}]({href})'  # Formatting link in markdown format
        else:
            new_text += str(elem)  # Appending non-link text as it is
    return new_text.strip()  # Returning modified text

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
    parser.add_argument('-u', '--url', type=str, default='https://github.com/nginx/agent/releases/', help='URL to fetch content from')
    args = parser.parse_args()  # Parsing command-line arguments
    url_content = get_url_content(args.url)  # Fetching content from the specified URL
    if url_content:
        if args.url == 'https://github.com/nginx/agent/releases/':
            all_changes = parse_html(url_content, args.url)  # Parsing releases page
        else:
            release_version, changes = parse_html(url_content, args.url)  # Parsing individual release page
            all_changes = [{'release_version': release_version, 'changes': changes}]
        if all_changes:
            template = Template(open('template.j2').read())  # Loading template for rendering
            output = template.render(all_changes=all_changes)  # Rendering template with changes data
            with open('changelog.md', 'w') as f:
                f.write(output)  # Writing rendered output to changelog file
            remove_extra_blank_lines('changelog.md')  # Removing extra blank lines from changelog
            remove_extra_lines('changelog.md')  # Removing extra lines from changelog

if __name__ == "__main__":
    main()  # Calling main function if script is executed directly
