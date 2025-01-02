# Installation

Download the project using <i>pipx</i>:
> install it before - [pipx.pypa.io/latest/installation/](https://pipx.pypa.io/latest/installation/)
```bash
pipx install https://github.com/unix-based/fcloud/archive/refs/heads/main.zip
```

#### Set up

1. You need to tell fcloud which cloud storage service you will use.
 Let's take dropbox as an example
    `fcloud config cloud dropbox`

2. Create a folder in your cloud and specify it with the following command. By default, all files will be downloaded there.*

    `fcloud config folder </your folder name/>`<br>
For example: `fcloud config folder /laptop`


!!! note
    You can find more information in the *CLOUDS* section of the documentation menu about the cloud you want to use.