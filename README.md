# NGINX Agent Changelog generation script

## Description
The `agent.py` script is a tool that grabs the required content from the [NGINX Agent Changelog in GitHub](https://github.com/nginx/agent/releases) and generates the Hugo content to be used in the [NGINX Agent Changelog page](https://docs.nginx.com/nginx-agent/changelog/)

The `template.j2` file is the Jinja2 template used to generate the Hugo content.

## Installation
1. Clone the repository
2. Install the required dependencies: `pip install -r requirements.txt`

## Usage
To run the script, use the following command:

`python agent.py`

The script will generate the `changelog.md` file in the same folder as the script.

If you want to generate the changelog for a single release use the -u flag with the release URL:

`python agent.py -u https://github.com/nginx/agent/releases/tag/v2.31.0`

or the latest release url:

`python agent.py -u https://github.com/nginx/agent/releases/latest/`

The genrated `changelog.md` can be copied directly to the `/site/content/` folder in the [NGINX Agent repository](https://github.com/nginx/agent/tree/main/site/content).