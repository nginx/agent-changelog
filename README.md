[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/nginx/agent-changelog/badge)](https://securityscorecards.dev/viewer/?uri=github.com/nginx/agent-changelog)
[![Community Support](https://badgen.net/badge/support/community/cyan?icon=awesome)](https://github.com/nginx/agent-changelog/blob/main/SUPPORT.md)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/nginx/agent-changelog/blob/main/CODE_OF_CONDUCT.md)

# NGINX Agent Changelog generation script

## Description
The `agent.py` script is a tool that grabs the required content from the [NGINX Agent Changelog in GitHub](https://github.com/nginx/agent/releases) and generates the Hugo content to be used in the [NGINX Agent Changelog page](https://docs.nginx.com/nginx-agent/changelog/)

The `template.j2` file is the Jinja2 template used to generate the Hugo content.

## Installation
1. Clone the repository
2. Install the required dependencies: `pip install -r requirements.txt`

## Usage
Run this script within a GitHub Actions workflow to generate a changelog. 

Make sure to define the GitHub token as an environment variable.

To run the script, use the following command:

`python agent.py`

The script will generate the `changelog.md` file in the same folder as the script containing the changes from the last 10 releases.

The genrated `changelog.md` can be copied directly to the `/site/content/` folder in the [NGINX Agent repository](https://github.com/nginx/agent/tree/main/site/content).

## License

[Apache License, Version 2.0](https://github.com/nginx/agent-changelog/blob/main/LICENSE)

&copy; [F5, Inc.](https://www.f5.com/) 2024