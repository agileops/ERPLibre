#!/usr/bin/env python
import os
import webbrowser
import argparse
import logging
from git import Repo

from script import fork_github_repo
from script import addons_repo_origin

_logger = logging.getLogger(__name__)
CST_GITHUB_TOKEN = "GITHUB_TOKEN"


# root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
# url_switch = {
#     'https://github.com/MathBenTech/odoo.git': 'https://github.com/odoo/odoo.git'
# }


def get_all_repo():
    lst_repo = []
    with open(".gitmodules") as file:
        txt = file.readlines()
        name = ""
        path = ""
        url = ""
        for line in txt:
            if line[:12] == "[submodule \"":
                name = line[12:-3]
                continue
            elif line[:8] == "\tpath = ":
                path = line[8:-1]
                continue
            elif line[:7] == "\turl = ":
                url = line[7:-1]
                # TODO support when git/ssh
                data = {
                    "url": url,
                    "path": path,
                    "name": name,
                }
                lst_repo.append(data)
            else:
                if not line.strip():
                    continue
                raise Exception(".gitmodules seems not correctly formatted.")
    return lst_repo


def get_project_config():
    with open("env_var.sh") as file:
        txt = file.readlines()
    txt = [a[:-1] for a in txt if "=" in a]

    lst_filter = [CST_GITHUB_TOKEN]
    lst_config = {}
    # Take filtered value and get bash string values
    for f in lst_filter:
        for v in txt:
            if f in v:
                lst_v = v.split("=")
                if len(lst_v) > 1:
                    lst_config[CST_GITHUB_TOKEN] = v.split("=")[1][1:-1]
    return lst_config


def get_config():
    """Parse command line arguments, extracting the config file name,
    returning the union of config file and command line arguments

    :return: dict of config file settings and command line arguments
    """
    config = get_project_config()

    # TODO update description
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''\
Fork a GitHub repo, clone that repo to a local directory, add the upstream
remote, create an optional feature branch and checkout that branch''',
        epilog='''\
The config file with a default location of
~/.github/fork_github_repo.yaml contains the following settings:

-  github_token : The `GitHub personal access token with the public_repo scope
   allowed.
   https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
-  repo_dir : The directory path to the directory containing all your cloned
    repos. If this isn't defined, /tmp is used.

The file is YAML formatted and the contents look like this :

github_token: 0123456789abcdef0123456789abcdef01234567
repo_dir: ~/Documents/github.com/example/
organization:
'''
    )
    # parser.add_argument(
    #     '-c', '--config',
    #     help='Filename of the yaml config file (default : %s)'
    #          % DEFAULT_CONFIG_FILENAME,
    #     default=filename_argument(DEFAULT_CONFIG_FILENAME),
    #     type=filename_argument)
    # parser.add_argument('url', help="GitHub URL of the upstream repo to fork",
    #                     type=github_url_argument)
    # parser.add_argument('branch', nargs='?', default=None,
    #                     help="Name of the feature branch to create")
    # parser.add_argument('url', help="GitHub URL of the upstream repo to fork")
    parser.add_argument('--github_token', dest="github_token",
                        default=config.get(CST_GITHUB_TOKEN),
                        help="GitHub token generated by user")
    args = parser.parse_args()
    return args
    # if (args.config == filename_argument(DEFAULT_CONFIG_FILENAME)) and (
    #         not os.path.isfile(args.config)):
    #     parser.error('Please create a config file at %s or point to one with '
    #                  'the --config option.' % DEFAULT_CONFIG_FILENAME)
    # if not os.path.isfile(args.config):
    #     raise argparse.ArgumentTypeError(
    #         'Could not find config file %s.' % args.config)
    # with open(args.config, 'r') as f:
    #     try:
    #         config = yaml.safe_load(f)
    #         if isinstance(config, dict):
    #             config.update(vars(args))
    #             return config
    #         else:
    #             raise argparse.ArgumentTypeError(
    #                 'Config contains %s of "%s" but it should be a dict'
    #                 % (type(config), config))
    #     except yaml.YAMLError:
    #         raise argparse.ArgumentTypeError(
    #             'Could not parse YAML in %s' % args.config)


def get_addons_repo_origin():
    """

    :return: list of {
                    "url": ...,
                    "path": ...,
                    "name": ...,
                }
    """
    dct_config = {
        # "": addons_repo_origin.config,
        "addons": addons_repo_origin.config_addons
    }
    result = []
    for c_path, dct_config in dct_config.items():
        for server, dct_organization in dct_config.items():
            for organization, lst_repo in dct_organization.items():
                for repo in lst_repo:
                    url = f"https://{server}/{organization}/{repo}.git"
                    url_https = f"https://{server}/{organization}/{repo}.git"
                    url_git = f"git@{server}:{organization}/{repo}.git"
                    if not c_path:
                        path = f"{repo}"
                    else:
                        path = f"{c_path}/{organization}_{repo}"

                    name = path
                    result.append(
                        {
                            "url": url,
                            "url_https": url_https,
                            "url_git": url_git,
                            "path": path,
                            "name": name,
                        }
                    )
    return result


def main():
    config = get_config()

    lst_repo = get_addons_repo_origin()
    lst_result = []
    for repo in lst_repo:
        # Exception, ignore addons/OCA_web
        if "addons/OCA_web" == repo.get("path"):
            continue
        str_repo = f'    printf "${{OE_HOME}}/{repo.get("path")}," >> ' \
                   f'${{OE_CONFIG_FILE}}\n'
        lst_result.append(str_repo)
    with open("script/odoo_install_locally.sh") as file:
        all_lines = file.readlines()
    # search place to add/replace lines
    index = 0
    find_index = False
    index_find = 0
    for line in all_lines:
        if not find_index and "if [ $MINIMAL_ADDONS = \"False\" ]; then\n" == line:
            index_find = index + 1
            for insert_line in lst_result:
                all_lines.insert(index_find, insert_line)
                index_find += 1
            find_index = True
            # Delete all next line until meet fi
        if find_index and "fi\n" == line:
            # slice it
            all_lines = all_lines[0:index_find] + all_lines[index:]
            break
        index += 1

    # create file
    with open("script/odoo_install_locally.sh", mode="w") as file:
        file.writelines(all_lines)

if __name__ == '__main__':
    main()
