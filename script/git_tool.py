#!/usr/bin/env python
# © 2020 TechnoLibre (http://www.technolibre.ca)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from . import addons_repo_origin

from git import Repo

CST_GITHUB_TOKEN = "GITHUB_TOKEN"


class GitTool:
    @staticmethod
    def get_repo_info_submodule(repo_path="./", add_root=False, upstream="origin"):
        """
        Get information about submodule from repo_path
        :param repo_path: path of repo to get information about submodule
        :param add_root: add information about root repository
        :param upstream: Use this upstream of root
        :return:
        [{
            "url": original_url,
            "url_https": url in https,
            "url_git": url in git,
            "path": path of the submodule
            "name": name of the submodule
        }]
        """
        filename = f"{repo_path}.gitmodules"
        lst_repo = []
        with open(filename) as file:
            txt = file.readlines()
            name = ""
            path = ""
            for line in txt:
                if line[:12] == "[submodule \"":
                    name = line[12:-3]
                    continue
                elif line[:7] == "\turl = ":
                    url = line[7:-1]
                    if "https" in url:
                        url_git = f"git@{url[8:].replace('/', ':', 1)}"
                        url_https = url
                    else:
                        url_https = f"https://{(url[4:]).replace(':', '/')}"
                        url_git = url
                    continue
                elif line[:8] == "\tpath = ":
                    path = line[8:-1]
                    data = {
                        "url": url,
                        "url_https": url_https,
                        "url_git": url_git,
                        "path": path,
                        "name": name,
                    }
                    lst_repo.append(data)
                else:
                    if not line.strip():
                        continue
                    raise Exception(".gitmodules seems not correctly formatted.")
        if add_root:
            repo_root = Repo(repo_path)
            url = repo_root.git.remote("get-url", "origin")
            if "https" in url:
                url_git = f"git@{url[8:].replace('/', ':', 1)}"
                url_https = url
            else:
                url_https = f"https://{(url[4:]).replace(':', '/')}"
                url_git = url

            data = {
                "url": url,
                "url_https": url_https,
                "url_git": url_git,
                "path": repo_path,
                "name": "",
            }
            lst_repo.insert(0, data)
        return lst_repo

    @staticmethod
    def get_repo_info_from_data_structure():
        """
        Deprecated, read file addons_repo_origin to obtains repo list.
        :return:
        [{
            "url": original_url,
            "url_https": url in https,
            "url_git": url in git,
            "path": path of the submodule
            "name": name of the submodule
        }]
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

    @staticmethod
    def get_project_config(repo_path="./"):
        """
        Get information about configuration in env_var.sh
        :param repo_path: path of repo to get information env_var.sh
        :return:
        {
            CST_GITHUB_TOKEN: TOKEN,
        }
        """
        filename = f"{repo_path}env_var.sh"
        with open(filename) as file:
            txt = file.readlines()
        txt = [a[:-1] for a in txt if "=" in a]

        lst_filter = [CST_GITHUB_TOKEN]
        dct_config = {}
        # Take filtered value and get bash string values
        for f in lst_filter:
            for v in txt:
                if f in v:
                    lst_v = v.split("=")
                    if len(lst_v) > 1:
                        dct_config[CST_GITHUB_TOKEN] = v.split("=")[1][1:-1]
        return dct_config
