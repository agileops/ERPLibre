#!/usr/bin/env python
# © 2020 TechnoLibre (http://www.technolibre.ca)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import argparse
import logging
from git import Repo

from script.git_tool import GitTool

_logger = logging.getLogger(__name__)


def get_config():
    """Parse command line arguments, extracting the config file name,
    returning the union of config file and command line arguments

    :return: dict of config file settings and command line arguments
    """
    # config = get_project_config()

    # TODO update description
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''\
''',
        epilog='''\
'''
    )
    parser.add_argument('-d', '--dir', dest="dir", default="./",
                        help="Path of repo to change remote, including submodule.")
    parser.add_argument('-f', '--upstream', dest="upstream", default="origin",
                        help="Upstream name to change address https to git.")
    args = parser.parse_args()
    return args


def main():
    git_tool = GitTool()
    config = get_config()

    upstream_name = config.upstream
    lst_repo = git_tool.get_repo_info_submodule(config.dir, add_root=True,
                                                upstream=upstream_name)
    i = 0
    total = len(lst_repo)
    for repo in lst_repo:
        i += 1
        print(f"Nb element {i}/{total}")
        repo_sm = Repo(repo.get("name"))
        remote_upstream_name = [a for a in repo_sm.remotes if upstream_name == a.name]
        for remote in remote_upstream_name:
            remote.set_url(repo.get("url_git"))
        print('Remote "%s" created for %s' % (upstream_name, repo.get("url_git")))


if __name__ == '__main__':
    main()
