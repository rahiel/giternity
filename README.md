# giternity

Giternity is a tool to mirror your git repositories from GitHub. You can specify
a username/organization to mirror all their repositories, or just individual
repo's. It retrieves some repo metadata so they can be nicely served with
[cgit][]. Run giternity periodically to update the mirrors.

[cgit]: https://git.zx2c4.com/cgit/about/

# Installation

Install giternity:

``` shell
sudo pip3 install giternity
```

You also need to have git installed.

# Configuration

The configuration file is at `/etc/giternity.toml`:

``` toml
# path where to keep the git mirrors
git_data_path = "/srv/git/"

# URL of your cgit instance (optional)
# cgit_url = "https://git.cpu.re/"

[github]
repositories = [
    "rahiel",
    "sunsistemo",
    "TeMPOraL/nyan-mode",
]
```

In the `[github]` section you specify which repositories to mirror. You list a
username (`"rahiel"`) or an organization (`"sunsistemo"`) to mirror all of their
non-fork repositories. For individual repos (`"TeMPOraL/nyan-mode"`) you specify
them like `owner/repo`.

With the configuration in place you simply run `giternity`.

For convenience there is an automatic configuration that sets up a separate
system user, gives this user permissions to `git_data_path` and creates a cron
job at `/etc/cron.d/giternity` to update the mirrors every hour. Apply these
defaults with:

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
