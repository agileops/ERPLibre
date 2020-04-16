#!/usr/bin/env python
import os
from script import fork_github_repo
from git import Repo
import webbrowser

root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))


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
                raise Exception(".gitmodules seems not correctly formated.")
    return lst_repo


url_switch = {
    'https://github.com/MathBenTech/odoo.git': 'https://github.com/odoo/odoo.git'
}


def main():
    # repo = Repo(root_path)
    lst_repo = get_all_repo()
    for repo in lst_repo:
        # url = "https://github.com/octocat/Spoon-Knife"
        url = repo.get("url")
        github_token = ""
        # repo_dir_root = "/tmp"
        repo_dir_root = repo.get("path")
        branch_name = None
        upstream_name = "upstream"
        organization_name = "ERPLibre"

        webbrowser.open_new_tab(url)
        continue

        if url in url_switch.keys():
            url = url_switch.get(url)
        fork_github_repo.get_list_fork_repo(url, github_token)

        fork_github_repo.fork_and_clone_repo(
            url,
            github_token,
            repo_dir_root,
            branch_name=branch_name,
            upstream_name=upstream_name,
            organization_name=organization_name,
            fork_only=True,
        )


if __name__ == '__main__':
    main()
