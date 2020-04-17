#!/usr/bin/env python
import os
import webbrowser
import argparse
import logging
from git import Repo

from retrying import retry  # pip install retrying

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
        "": addons_repo_origin.config,
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
    # repo = Repo(root_path)
    # lst_repo = get_all_repo()
    config = get_config()

    repo_root = Repo(".")

    lst_repo = get_addons_repo_origin()
    i = 0
    total = len(lst_repo)
    for repo in lst_repo:
        i += 1
        print(f"Nb element {i}/{total}")
        # url = "https://github.com/octocat/Spoon-Knife"
        # TODO remove repo.get("name"), not used
        url = repo.get("url")
        # repo_dir_root = "/tmp"
        repo_dir_root = repo.get("path")
        upstream_name = "MathBenTech"
        organization_name = "ERPLibre"

        # webbrowser.open_new_tab(url)
        # continue

        # if url in url_switch.keys():
        #     url = url_switch.get(url)
        # fork_github_repo.get_list_fork_repo(url, github_token)

        _logger.info(
            f"Fork {url} on dir {repo_dir_root} for organization {organization_name}")

        # fork_github_repo.fork_and_clone_repo(
        #     url,
        #     repo_dir_root,
        #     branch_name=branch_name,
        #     upstream_name=upstream_name,
        #     organization_name=organization_name,
        #     # fork_only=True,
        #     repo_root=repo_root,
        # )

        # Create the remote upstream
        split_url = url.split("/")
        split_url[-2] = upstream_name
        upstream_url = "/".join(split_url)

        cloned_repo = Repo(repo_dir_root)
        # Checkout branch 12.0
        # try:
        #     cloned_repo.git.checkout("origin/12.0", b="12.0")
        # except:
        #     try:
        #         cloned_repo.git.checkout("12.0")
        #     except:
        #         print(f"ERROR, missing branch 12.0 for {repo_dir_root}")

        try:
            upstream_remote = cloned_repo.remote(upstream_name)
            print('Remote "%s" already exists in %s' %
                  (upstream_name, repo_dir_root))
        except ValueError:
            upstream_remote = retry(
                wait_exponential_multiplier=1000,
                stop_max_delay=15000
            )(cloned_repo.create_remote)(upstream_name, upstream_url)
            print('Remote "%s" created for %s' % (upstream_name, upstream_url))

        try:
            # Fetch the remote upstream
            retry(wait_exponential_multiplier=1000, stop_max_delay=15000)(
                upstream_remote.fetch)()
            print('Remote "%s" fetched' % upstream_name)
        except Exception:
            print(f"ERROR git {repo_dir_root} remote {upstream_name} not exist.")
            upstream_remote.remove(cloned_repo, upstream_name)


if __name__ == '__main__':
    main()
