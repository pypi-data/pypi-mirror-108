# __main__.py

from configparser import ConfigParser
from importlib import resources  # Python 3.7+
import sys

from gitvars import readvars

def main():
    """Import the gitlab variables"""
    # Import Gitlab CI/CD variables from your project
    cfg = ConfigParser()
    cfg.read_string(resources.read_text("gitvars", "config.txt"))
    gitlabapi_baseurl = cfg.get("project", "gitlabapi_baseurl")

    # If an article ID is given, show the article
    if len(sys.argv) > 1:
        cicd_vars = readvars._read(gitlabapi_baseurl, sys.argv[1])

    # If no ID is given, show a list of all articles
    else:
        print("Project ID is required")

if __name__ == "__main__":
    main()
