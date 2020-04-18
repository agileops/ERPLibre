#!/usr/bin/env python
# © 2020 TechnoLibre (http://www.technolibre.ca)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from . import addons_repo_origin
import webbrowser

from git import Repo

CST_FILE_SOURCE_REPO_ADDONS_ODOO = "source_repo_addons_odoo.csv"
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
    def get_repo_info_from_data_structure(ignore_odoo=False):
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
            "addons": addons_repo_origin.config_addons
        }
        if not ignore_odoo:
            dct_config[""] = addons_repo_origin.config
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

    @staticmethod
    def open_repo_web_browser(dct_repo):
        url = dct_repo.get("url_https")
        if url:
            webbrowser.open_new_tab(url)

    def generate_repo_source_from_building(self, path_repo="./"):
        """
        Generate csv file with information about all source addons repo of Odoo
        :param path_repo:
        :return:
        """
        file_name = f"{path_repo}{CST_FILE_SOURCE_REPO_ADDONS_ODOO}"
        lst_repo_info = self.get_repo_info_from_data_structure(ignore_odoo=True)
        lst_result = [f"{a.get('url_https')}\n" for a in lst_repo_info]
        with open(file_name, "w") as file:
            file.writelines(lst_result)

    def generate_odoo_install_locally(self):
        lst_repo = self.get_repo_info_from_data_structure(ignore_odoo=True)
        lst_result = []
        for repo in lst_repo:
            # Exception, ignore addons/OCA_web and root
            if "addons/OCA_web" == repo.get("path") or \
                    "odoo" == repo.get("path"):
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

    def get_source_repo_addons(self):
        pass
