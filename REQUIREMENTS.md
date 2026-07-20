# Setting Up Your Laptop

To prepare for the tutorial you can take several approaches depending on your
needs and the requirements your organization may place on you for setup. This
guide will not cover all the details as it is assumed that you have some
familiarity with setting up a development environment on your laptop.

There are several ways to set up your environment for the tutorials, but in the end
they are in jupyter notebook form and we will want to run jupyter on
your laptop inside DragonHPC. The sections below provides a number of ways you can
configure your laptop.

## Running in a Docker Container with VS Code

This is the easiest and preferred route. Clone this repository to your
laptop. Insure you have Visual Studio Code and Docker Desktop installed.
You will need:

* A working Docker engine.
  See https://docs.docker.com/engine/install/ and/or https://docs.docker.com/desktop/
  for Docker installation instructions.

* VS Code with the Dev Containers extension installed.
  See https://code.visualstudio.com/docs/devcontainers/tutorial for setup instructions.

Once these things are available you can follow these steps to get up and running.

1. Open this project folder locally in VS Code (File > Open Folder...).
2. Click the pop-up notification in the bottom-right corner that says "Reopen in Container".
3. VS Code will build the environment, reload the window, and connect you directly into the container.
4. If you miss the pop-up, open the Command Palette by pressing Ctrl+Shift+P (or Cmd+Shift+P on macOS) and run "Dev Containers: Reopen in Container".
6. VS Code will run "dragon-jupyter" next right after the container starts. You should click the bottom-right pop-up
   "Open in Browser" when prompted. You will see the browser window with the directory structure.
7. Click on the [test.ipynb](test.ipynb) file in the top directory and follow the directions in it.
8. That's it. Assuming it worked, you are all ready for the tutorial.


## Running in a Docker Container without VS Code

You can run this way as well and you would not be giving anything except some of
the automation for getting started. In this case you need to start a docker
container using the Dockerfile in the repo. It is assumed you know how to do this
in this case. Once the container is started it should provide all the necessary
code so you can run the tutorials.

From the root directory of the repo and the command-line inside the container
type `dragon-jupyter` to start Dragon's Jupyter server. This will print a message
to the screen that looks like this.

```console
(.venv) /workspaces/pearc_2026_tutorial $ dragon-jupyter
[I 2026-07-20 17:57:42.867 ServerApp] jupyter_lsp | extension was successfully linked.
[I 2026-07-20 17:57:42.868 ServerApp] jupyter_server_terminals | extension was successfully linked.
[I 2026-07-20 17:57:42.870 ServerApp] jupyterlab | extension was successfully linked.
[I 2026-07-20 17:57:42.872 ServerApp] notebook | extension was successfully linked.
[I 2026-07-20 17:57:43.008 ServerApp] notebook_shim | extension was successfully linked.
[I 2026-07-20 17:57:43.015 ServerApp] notebook_shim | extension was successfully loaded.
[I 2026-07-20 17:57:43.017 ServerApp] jupyter_lsp | extension was successfully loaded.
[I 2026-07-20 17:57:43.018 ServerApp] jupyter_server_terminals | extension was successfully loaded.
[I 2026-07-20 17:57:43.019 LabApp] JupyterLab extension loaded from /usr/local/lib/python3.12/site-packages/jupyterlab
[I 2026-07-20 17:57:43.019 LabApp] JupyterLab application directory is /usr/local/share/jupyter/lab
[I 2026-07-20 17:57:43.019 LabApp] Extension Manager is 'pypi'.
[I 2026-07-20 17:57:43.033 ServerApp] jupyterlab | extension was successfully loaded.
[I 2026-07-20 17:57:43.034 ServerApp] notebook | extension was successfully loaded.
[I 2026-07-20 17:57:43.035 ServerApp] The port 8888 is already in use, trying another port.
[I 2026-07-20 17:57:43.035 ServerApp] Serving notebooks from local directory: /workspaces/pearc_2026_tutorial
[I 2026-07-20 17:57:43.035 ServerApp] Jupyter Server 2.20.0 is running at:
[I 2026-07-20 17:57:43.035 ServerApp] http://0.0.0.0:8889/tree?token=2fd358f6df3eb13b8b696a01d25bb1784c8b216c9ca03860
[I 2026-07-20 17:57:43.035 ServerApp]     http://127.0.0.1:8889/tree?token=2fd358f6df3eb13b8b696a01d25bb1784c8b216c9ca03860
[I 2026-07-20 17:57:43.035 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2026-07-20 17:57:43.036 ServerApp]

    To access the server, open this file in a browser:
        file:///home/vscode/.local/share/jupyter/runtime/jpserver-59047-open.html
    Or copy and paste one of these URLs:
        http://23044e962396:8889/tree?token=2fd358f6df3eb13b8b696a01d25bb1784c8b216c9ca03860
        http://127.0.0.1:8889/tree?token=2fd358f6df3eb13b8b696a01d25bb1784c8b216c9ca03860
    The server is listening on all interfaces, so any hostname or IP of this machine will work.
[I 2026-07-20 17:57:43.070 ServerApp] Skipped non-installed server(s): basedpyright, bash-language-server, dockerfile-language-server-nodejs, javascript-typescript-langserver, jedi-language-server, julia-language-server, pyrefly, pyright, python-language-server, python-lsp-server, r-languageserver, sql-language-server, texlab, typescript-language-server, unified-language-server, vscode-css-languageserver-bin, vscode-html-languageserver-bin, vscode-json-languageserver-bin, yaml-language-server
```

You can copy the URL starting with `127.0.0.1` into a browser window. If the
webpage prompts you to enter a token or password, copy the token from after
`token=` and paste that into the data entry field. That will then display a
directory structure where you can open notebooks. Open the
[test.ipynb](test.ipynb) notebook, run the cell in it, and make sure the output
says that `Dragon is ready`.

## Running natively on Mac OS

In this mode you run Dragon natively on Mac OS with no container. These
directions are considerably less detailed and it is up to the user to know how to
install and configured software on their Mac.

To run natively on Mac OS you will need to install a version of Python. Python
3.12 is the default when running in a container. You may wish to have that
version as well, but 3.11, 12, or 13 should run just fine.

Open a terminal window, navigate to the Repo top-level directory. You need to
create a Python virtual environment. Then activate that environment. After
activating it you will need to install a number of packages which are provided in
requirements.txt. Navigate to the top-level directory of the repository. From
there do a

```bash
pip install -r requirements.txt
```

This will install all the required packages needed by the tutorial except for a
GNU based C++ compiler.

Run `dragon-jupyter` from the command-line and copy the URL that starts with
`127.0.0.1` into a web browser. Grab the printed token from the terminal to paste
into the browser where it asks for a token. Then open the
[test.ipynb](test.ipynb) notebook and verify that you can run the cell inside it.

You will want to make sure you have a g++ compiler installed as well. That may be
available with the XCode Command-line Tools and/or by installing the XCode
package on Mac OS. If you don't find `g++` there, then using Brew for Mac OS to
install the GNU C++ compiler may be required. The C++ compiler is only needed for
two example exercises near the end of the day, so it is not absolutely critical
to be installed and working, but desirable if possible.

With the virtual environment active, navigate to
`course2/sharing_data_mpi_and_others`. In that directory there is a Makefile. If
you can type `make` in that directory and the program `worker.cpp` program
compiles, then you have all that you need for compiling the code.

