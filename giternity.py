#!/usr/bin/env python3
# giternity - Mirror git repositories
# Copyright (C) 2017 Rahiel Kasim
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANT ABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import argparse
import os
import subprocess
import sys
from os.path import exists
from pwd import getpwnam
from subprocess import CalledProcessError, run

import requests
import toml


__version__ = "0.1"


def main():
    parser = argparse.ArgumentParser(description="Mirror git repositories.",
                                     epilog="Homepage: https://github.com/rahiel/giternity")
    parser.add_argument("-c", "--configure", help="configure %(prog)s", action="store_true")
    parser.add_argument("--version", action="version", version="%(prog)s {}".format(__version__))
    args = parser.parse_args()

    try:
        config = toml.load("/etc/giternity.toml")
    except FileNotFoundError:
        print(markup("No configuration file found!", "red"))
        print("Please place your configuration at " + markup("/etc/giternity.toml", "bold"))
        sys.exit(1)

    git_data_path = config.get("git_data_path", "/srv/git/")
    cgit_url = config.get("cgit_url")

    if args.configure:
        return configure(git_data_path)

    if config.get("github") and config["github"].get("repositories"):
        gh = GitHub(cgit_url=cgit_url)
        for r in config["github"]["repositories"]:
            if "/" in r:
                path = git_data_path + r + "/"
                owner, name = r.split("/")
                url = "https://github.com/{}/{}.git".format(owner, name)
                repo = gh.get_repo(owner, name)
                mirror(url, path)
                with open(path + "cgitrc", "w") as f:
                    f.write(gh.repo_to_cgitrc(repo))
            else:
                for repo in gh.get_repos(r):
                    path = git_data_path + repo["full_name"] + "/"
                    mirror(repo["clone_url"], path)
                    with open(path + "cgitrc", "w") as f:
                        f.write(gh.repo_to_cgitrc(repo))


def configure(git_data_path: str):
    try:
        try:
            getpwnam("giternity")
        except KeyError:
            run("adduser giternity --system --no-create-home".split(), check=True)

        run(["mkdir", "-p", git_data_path], check=True)
        run(["chown", "-R", "giternity", git_data_path], check=True)

        cron = """SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
0 * * * * giternity giternity\n"""

        with open("/etc/cron.d/giternity", "w") as f:
            f.write(cron)

    except (FileNotFoundError, PermissionError, CalledProcessError):
        print("Please run the configuration with root privileges: " +
              markup("sudo giternity --configure", "bold"))
        sys.exit(1)

    print(markup("Everything is OK!", "green") + "\nHave fun using giternity!")


def mirror(url: str, path: str):
    if exists(path):
        run(["git", "-C", path, "remote", "update", "--prune"], stdout=subprocess.DEVNULL)
    else:
        run(["git", "clone", "--mirror", url, path], stdout=subprocess.DEVNULL)
    # set last modified date
    date = run(["git", "-C", path,
                "for-each-ref", "--sort=-authordate", "--count=1", "--format='%(authordate:iso8601)'"],
               stdout=subprocess.PIPE)
    os.makedirs(path + "info/web/", exist_ok=True)
    with open(path + "info/web/last-modified", "wb") as f:
        f.write(date.stdout)


class GitHub:
    def __init__(self, cgit_url=None):
        session = requests.Session()
        session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "giternity ({})".format(__version__)
        })
        self.s = session
        self.api = "https://api.github.com"
        self.cgit_url = cgit_url

    def get_repo(self, owner: str, repository: str):
        data = self.s.get(self.api + "/repos/{}/{}".format(owner, repository)).json()
        return data

    def get_repos(self, user: str):
        data = self.s.get(self.api + "/users/{}/repos".format(user)).json()
        data = [r for r in data if not r["fork"]]
        return data

    def repo_to_cgitrc(self, data):
        cgitrc = []
        if self.cgit_url:
            local_url = self.cgit_url + data["full_name"]
            clone_url = "clone-url={} {}\n".format(local_url, data["clone_url"])
        else:
            clone_url = "clone-url={}\n".format(data["clone_url"])
        if data["description"]:
            desc = "desc={}\n".format(data["description"].replace("\n", ""))
        else:
            desc = "desc=Mysterious Project\n"
        if data["homepage"]:
            homepage = "homepage={}\n".format(data["homepage"])
            cgitrc.append(homepage)
        name = "name={}\n".format(data["name"])
        cgitrc += [clone_url, desc, name]
        return "".join(cgitrc)


def markup(text: str, style: str):
    ansi_codes = {"bold": "\033[1m", "red": "\033[31m", "green": "\033[32m",
                  "cyan": "\033[36m", "magenta": "\033[35m"}
    return ansi_codes[style] + text + "\033[0m"


if __name__ == "__main__":
    main()
