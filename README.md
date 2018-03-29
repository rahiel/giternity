# giternity

[![Version](https://img.shields.io/pypi/v/giternity.svg)](https://pypi.org/project/giternity/)
[![pyversions](https://img.shields.io/pypi/pyversions/giternity.svg)](https://pypi.org/project/giternity/)
[![Downloads](https://www.cpu.re/static/giternity/downloads.svg)](https://www.cpu.re/static/giternity/downloads-by-python-version.txt)
[![License](https://img.shields.io/badge/License-GPLv3+-blue.svg)](https://github.com/rahiel/giternity/blob/master/LICENSE.txt)

Giternity is a tool to mirror git repositories from GitHub. You can specify a
username/organization to mirror all their repositories, or just individual
repos. It retrieves some repo metadata so they can be nicely served with
[cgit][]. Run giternity periodically to update the mirrors.

An example result is [git.cpu.re][]. Follow the [tutorial][] to host your own.

[cgit]: https://git.zx2c4.com/cgit/about/
[git.cpu.re]: https://git.cpu.re/
[tutorial]: https://www.rahielkasim.com/mirror-git-repositories-and-serve-them-with-cgit/

# Installation

Install giternity:

``` shell
sudo pip3 install giternity
```

You also need to have git installed.

# Configuration

The configuration file is at `/etc/giternity.toml`:
<!-- TODO: ini should be toml when pygments has toml support -->
``` ini
# path for the git mirrors
git_data_path = "/srv/git/"

# path for checkouts of the git mirrors (optional)
# checkout_path = "/srv/git_checkout/"

# public URL of your cgit instance (optional)
# cgit_url = "https://git.cpu.re/"

[github]
repositories = [
    "rahiel",
    "sunsistemo",
    "TeMPOraL/nyan-mode",
]
```

Set `git_data_path` to the path where you want to store the git repositories. It
will contain bare git repositories: the data you usually see in the `.git`
directory in your projects. To also have the actual working files of the repos,
set `checkout_path` to where to keep them. If you'll be hosting the repos with
cgit, set `cgit_url` to the public URL.

In the `[github]` section you specify which repositories to mirror. You list a
username (`"rahiel"`) or an organization (`"sunsistemo"`) to mirror all of their
non-fork repositories. For individual repos (`"TeMPOraL/nyan-mode"`) you specify
them like `owner/repo`.

With the configuration in place you simply run `giternity`.

For convenience there is an automatic configuration that sets up a separate
system user, gives this user permissions to `git_data_path` (and to
`checkout_path` if specified) and creates a cron job at `/etc/cron.d/giternity`
to update the mirrors every hour. Apply these defaults with:

``` shell
sudo giternity --configure
```

# cgit

Your git mirrors are now suitable to serve with cgit. Customize your
`/etc/cgitrc` as you like and add the following to the bottom:

``` ini
agefile=info/web/last-modified
section-from-path=1
scan-path=/srv/git/
```

where you replace `/srv/git/` with the `git_data_path` from your
`/etc/giternity.toml`.
