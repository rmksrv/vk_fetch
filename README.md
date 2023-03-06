# vk_fetch

<p>
    <img alt="license: MIT" src="https://img.shields.io/github/license/rmksrv/vk_fetch">
    <img alt="python: 3.11" src="https://img.shields.io/badge/python-3.11-brightgreen">
    <img alt="code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</p>

Script helps to fetch all data from your VK account. No need to browse every part of profile and 
manually download every single file.


## Usage

```
vk_fetch --help

 Usage: vk_fetch [OPTIONS] COMMAND [ARGS]...

 Script helps to fetch all data from your VK account

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershe  Install completion for  │
│                             ll|pwsh]                 the specified shell.    │
│                                                      [default: None]         │
│ --show-completion           [bash|zsh|fish|powershe  Show completion for the │
│                             ll|pwsh]                 specified shell, to     │
│                                                      copy it or customize    │
│                                                      the installation.       │
│                                                      [default: None]         │
│ --help                                               Show this message and   │
│                                                      exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ download   Download data from VK profile                                     │
│ ping       Check app can connect to VK and auth as user with login/pass      │
│ show       Print available data of VK profile                                │
╰──────────────────────────────────────────────────────────────────────────────╯
```


## Sample cases

- Download all:
![](docs/images/demo-download-all.png)
- Download all exclude attachments in conversations `111`, `-222`, `c5`:
![](docs/images/demo-download-all-except.png)
- Download all attachments in conversations `111`, `-222`, `c5`:
![](docs/images/demo-download-conversations.png)
- Show all available data to fetch:
![](docs/images/demo-show-all-available.png)
