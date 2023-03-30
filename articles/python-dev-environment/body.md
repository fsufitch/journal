I’ve gotten asked this multiple times: “What’s the best way to structure my Python dev environment?
How do you install Python, and which version (and how do you switch versions)? How do you install
and manage dependencies? What’s the best way to use virtualenvs (and what are they)?” And more...

This post is my **definitive guide to how I do it**, today in 2023, for both professional and hobby projects.
There are many approaches, but this one is mine and I vouch for it 100%. It is a bit involved though, so strap in!

:::imagecard center python-branch.jpg
Photo by [David Clode on Unsplash](https://unsplash.com/@davidclode?utm_source=medium&utm_medium=referral).
:::

---

# General Summary

This post is going to take you through the whole process of creating a new Python project on your
computer, in great detail. _It’s equally applicable no matter your operating system_ — I even
recommend following this approach in Docker containers or similar environments
([devcontainers?!](https://containers.dev/)).

:::alert default

### Table of Contents

1. [Installing Python](#h1-step-1-installing-python-itself-1695632937)
   - (yes, even on Linux/Mac where it might be built in)
2. [Creating yourself a “base virtualenv” of Python](#h1-step-2-create-the-base-virtual-environment-312270074),
3. [Using Poetry with `pyproject.toml` to start developing a Python package](#h1-step-3-create-your-project-and-write-some-code-962003670)
4. [Managing your dependencies with Poetry](#h1-step-4-managing-your-dependencies-2123698302)
5. [Adding dev-time tools](#h1-step-5-adding-dev-time-tools-386261876)
6. [Building, packaging and publishing your package](#h1-step-6-building-and-packaging-1278213658)

:::

Yes, it's a lot.

But first, re-emphasizing a caveat before we get going: **the approach mentioned here is my preference
and recommendation**; you can substitute many parts of it with different tools, or depart from it entirely,
and still have a perfectly good dev environment. I will justify my choices where relevant, but ultimately
in some places (e.g. linting) it’s down to taste/preference.

Second: **this guide assumes familiarity with the command line of your OS of choice, plus some basic dev
skills**. It will not include guidance on mkdir, cd, and other basics. It also assumes you can use a
code editor of some kind, and that you do in fact already know some Python. It also addresses nothing
about Git or other version control, though you should absolutely use it.

Lastly: since I mainly develop on Unix-like systems (Linux and MacOS) **the commands that I do list will be
in Unix-like syntax**. That means variables are `$VAR`, subshells use `$()`, and other similar things.
You will want to adapt those on-the-fly on Windows… or to use Cygwin, MSYS2, or something similar as
your terminal.

With that out of the way, let’s get going.

:::imagecard center dog-typing.jpg
:::

---

# Step 1: Installing Python Itself

To write Python code, you have to have Python installed. It makes sense. _How_ you install it is another
matter, though. On Linux, you may be tempted to `apt install python3`. On Windows or MacOS, ou may be
tempted to go to [www.python.org](https://www.python.org), download an installer, and run it. **Doing
either of these is not appropriate for heavyweight development.** They works in a pinch for
scripting, and it’s perfectly adequate if you need to just run Python code that someone else gave you...
But it is insufficient for “real” development.

Why?

- These approaches usually involve installing Python system-wide. A system-wide install may be used by
  any number of programs, so you can end up with strange installed packages from their dependencies.
  Your dev environment is then inconsistent, which can trip you up with mystery bugs.
- A system-wide install also means administrator permissions. Requiring those in your dev workflow can
  make some tools misbehave, and is generally not very safe for your OS.
- In the case of Linux, apt install python3 does not give you control over which minor version you
  install. The difference between 3.8 and 3.11 is huge.
- Having multiple versions installed (which may be important if you’re working on different projects
  at the same time) is very inconvenient.

**What you should use instead is a self-contained Python install, in your user directory.**
Sometimes called a “portable” version, it simply refers to a Python installation which is contained
in its own directory, somewhere within _your_ files, not system/OS files. My recommendation is to create
a `devtools` directory to contain Python and other tools. You can put other language
interpreters/compilers/etc in there too (NodeJS, Java, etc)!
They also work better when separate from your OS.

The instructions for each OS diverge significantly, so you may want to scroll down to the stuff
that’s actually relevant to you:

- [Windows](#h2-windows-1606247296)
- [MacOS](#h2-macos-578753360)
- [Linux](#h2-linux-579426767)

> Note: this section can be simplified if you choose to use a tool such as `pyenv` or something else
> to supply you with a runnable Python of your favorite version. However, I prefer the full control
> of a complete custom build, so that’s what we’re doing.

## Windows

:::imagecard center windows-c.png
:::

I like to create devtools in the drive root: `C:\devtools`. The drive root in Windows is not a
system-protected location, and it’s short and sweet. You can put it in your home dir in
`C:\Users\<you>\devtools` as well, though. While we’re here, define an environment variable
in your terminal so you can easily refer to your devtools.

```powershell
set DEVTOOLS=C:\devtools
```

Building a portable version on Windows is such a pain that we're not actually going to do it. Sorry
if that's disappointing; we'll just download it instead. Get the official package corresponding to
your desired release version, then unzip it and put it in `%DEVTOOLS%`. Rename the dir containing it
to something shorter, like `python-3.11`.

Lastly, set an environment variable in your terminal so you have a quick reference to where it is:

```powershell
set PYROOT=%DEVTOOLS%\python-3.11
```

Now, you can run:

```powershell
%PYROOT%\python3 --version
```

That should print out Python 3.11 (or whatever version you downloaded). Whenever `$PYROOT` is
referenced in later commands in this guide, remember to replace that with `%PYROOT%` (since variables
work differently in Windows vs Unix-like systems).

## MacOS

:::imagecard center python-apple.jpg
[Snake and apple](https://www.dreamstime.com/royalty-free-stock-image-snake-apple-image513906)
:::

Portable installs are not distributed on python.org for MacOS. You could find another download, or
use a tool like `pyenv`... but my recommendation is to build it from scratch!
[The steps to do that are based on the official build guide.](https://devguide.python.org/getting-started/setup-building/)

**First, install XCode Developer Tools.** Run `xcode-select --install`.

**Next, get the binary libraries that Python needs for various features.** When a C program like
Python is compiled, it needs “shared libraries” to access certain features provided by the OS.
MacOS does not come with these, and the easiest way to get them is to use a 3rd party package
manager, like [Homebrew](https://brew.sh/) in this case (you should install it anyway).

```bash
brew install pkg-config openssl xz gdbm tcl-tk
```

**Now, you need the actual Python source code.** Download it from the
[source distribution page](https://www.python.org/downloads/source/). Unzip it, and rename/move
the contained directory to `$HOME/devtools/python-X.X` (specifying your version number there).

While you’re there, set an environment variable to remember where your devtools directory is.
It’ll be helpful later.

```bash
export DEVTOOLS=$HOME/devtools
```

**Next, configure the build for your system.** If you are building Python 3.10+, then in the
directory you put the source in, run:

```bash
CFLAGS="-I$(brew --prefix gdbm)/include -I$(brew --prefix xz)/include" \
LDFLAGS="-L$(brew --prefix gdbm)/lib -I$(brew --prefix xz)/lib" \
PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
./configure \
    --enable-framework="$(pwd)/Framework" \
    --enable-optimizations \
    --with-openssl=$(brew --prefix openssl)
```

Otherwise, run:

```bash
CFLAGS="-I$(brew --prefix gdbm)/include -I$(brew --prefix xz)/include" \
LDFLAGS="-L$(brew --prefix gdbm)/lib -L$(brew --prefix xz)/lib" \
PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
./configure \
    --enable-framework="$(pwd)/Framework" \
    --enable-optimizations \
    --with-openssl=$(brew --prefix openssl@1.1) \
    --with-tcltk-libs="$(pkg-config --libs tcl tk)" \
    --with-tcltk-includes="$(pkg-config --cflags tcl tk)"
```

You can tweak other flags to `configure` according to the documentation
[here](https://docs.python.org/3/using/configure.html).

**Note:** This build is done with --enable-framework to facilitate being able
to develop GUI applications right. MacOS is weird. See more details on Mac builds
[here](https://github.com/python/cpython/blob/main/Mac/README.rst). The above
command will check that your system is actually ready to compile Python, and do a
bunch of configuration of the source files so they “fit” your system correctly.

**Now, let's actually compile it!**

```bash
make -j4 && make install
```

Using `-j4` speeds up the build by compiling files in 4 different “threads”.
This uses 4 “threads” to compile it. You’ll know it works because it will take a
while to run, and print a whole lot of junk (you can add `-q` to the command to make
it quiet, but I like the wall of text).

You now have a runnable, self-contained `python3` at a very awkward path.
Let’s remember it in an env var, and test it:

```bash
export PYROOT=$(pwd)/Framework/Python.framework/Versions/Current/bin

$PYROOT/python3 --version
```

That should print the correct version of Python that you downloaded.
Keep `$PYROOT` defined in your shell; it will be important later.

## Linux

:::imagecard center python-penguin.jpg
[By sushirolled on Deviantart](https://www.deviantart.com/sushirolled/art/Penguin-and-the-Snake-705508542)
:::

Like in the case of MacOS, python.org does not distribute binary builds.
Actual Linux distros do, but this guide is for getting yourself a _specific version,
installed self-contained in a user directory_, so we need to build it from scratch.
The steps to do that are based on the
[official build guide](https://devguide.python.org/getting-started/setup-building/).

Installing Python’s system dependencies is easier in this case than in MacOS, since Linux
typically comes with its own package manager. The exact command will vary by your
“flavor” of Linux, but you will want something like this:

```bash
sudo apt install -y build-essential gdb lcov pkg-config \
    libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
    libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
    lzma lzma-dev tk-dev uuid-dev zlib1g-dev
```

**Now, you need the actual Python source code.** Download it from the
[source distribution page](https://www.python.org/downloads/source/).
Unzip it, and rename/move the contained directory to `$HOME/devtools/python-X.X`
(specifying your version number there).

While you’re there, set an environment variable to remember where your devtools
directory is. It’ll be helpful later.

```bash
export DEVTOOLS=$HOME/devtools
```

**Next, configure the build for your system.** In the Python directory from above, run:

```bash
./configure \
    --prefix=$(pwd)/Install \
    --enable-optimizations
```

You can tweak other flags to `configure` according to the documentation
[here](https://docs.python.org/3/using/configure.html). Note that you’re giving
the configuration a prefix, which is where Python will be installed once it’s built.

**Now, compile and install!**

```bash
make -j4 && make install
```

Using `-j4` speeds up the build by compiling files in 4 different “threads”.
This uses 4 “threads” to compile it. You’ll know it works because it will take
a while to run, and print a whole _lot_ of junk (you can add `-q` to the command
to make it quiet, but I like the wall of text).

You now have a runnable, self-contained `python3` at a very awkward path.
Let’s remember it in an env var, and test it:

```bash
export PYROOT=$(pwd)/Install/bin

$PYROOT/python3 --version
```

That should print the correct version of Python that you downloaded. Keep `$PYROOT`
defined in your shell; it will be important later.

# Step 2: Create the base virtual environment

That took a while, didn't it?

:::imagecard center waiting-skeleton.jpg
Photo by [Mathew Schwartz on Unsplash](https://unsplash.com/@cadop)
:::

That’s okay, it was the hard part. Next up: actually setting up the Python
executable we are going to use. The Python we built above, and refer to as
`$PYROOT`, is pristine. Freshly built, it just works. _We should not touch it._
If we install things into it (using `$PYROOT/pip3`), upgrade anything in it, etc,
we risk breaking things and making it depart from its pure, just-working roots.
Instead, to protect it, let’s create a virtual environment that we will use as
our “real” Python install.

A “virtual environment” is kind of like its own Python installation.
It is a directory that has things like `bin`, `include`, `lib`, `share`, and
maintains its own set of installed packages. It has a Python interpreter in
`bin/python` , Pip in `bin/pip`, and any packages get installed into `lib`.
However, all that is simply a veneer on top of the original compiled Python.

Let’s create the main virtualenv for our development Python (remember to
replace the version number with the correct one for you). Then, set an
environment variable to remember this one as well.

```bash
$PYROOT/python3 -m venv $DEVTOOLS/pyvenv-3.11

export PYVENV=$DEVTOOLS/pyvenv-3.11/bin
```

The virtualenv’s Python binaries are now `$PYVENV/python`, `$PYVENV/pip`, etc.
Now that we have an isolated environment, let’s make sure we use the latest
version of Pip, plus the build/versioning system we’ll be using ([Poetry](https://python-poetry.org/),
version 1.2.X specifically, since their commands can vary wildly between
versions).

```bash
$PYVENV/pip install -U pip 'poetry>=1.2,<1.3'
```

It is now that you can see the separation between the virtualenv and the
original install. Check this out, the versions of `pip3` they have are different,
and the `PYROOT` environment does not have Poetry installed!

```bash
# $PYROOT/pip3 --version
pip 22.3 from ... (python3.11)

# $PYVENV/pip3 --version
pip 22.3.1 from ... (python 3.11)

# $PYROOT/poetry --version
bash: .../python-3.11/Install/bin/poetry: No such file or directory

# $PYVENV/poetry --version
Poetry (version 1.2.2)
```

:::imagecard center big-brain-virtualenv.jpg
Photo by [Mathew Schwartz on Unsplash](https://unsplash.com/@cadop)
:::

**Remembering this environment.** You now have a completely working independent
Python virtualenv, and it is ready to be the Python you use for development.
You should add it do the _front of your user’s PATH variable_. How to do so
depends on your OS:

- Windows: You will have to go through the System Management UI, or through the Registry Editor.
- MacOS and Linux: Add the following line to $HOME/.zshrc or $HOME/.bashrc, depending on which one you use (usually zsh on Mac and bash on Linux, but it can vary):
  ```bash
  export PATH=$HOME/devtools/pyvenv-3.11/bin:$PATH
  ```

Close and re-launch your command terminal. When you run `which python`
(or on Windows, `where python`), your terminal now knows to find your new
virtualenv-enabled Python! Same thing with `pip` and `poetry`! Hooray!

:::alert info
Note: You can still access the Python you built at `$HOME/devtools/python-3.11/.../bin/python3` . Your system Python is also still available on MacOS/Linux at `/usr/bin/python3`. All the setup done above is purely additive and non-destructive. The way to revert anything is to simply remove the offending directory. How’s that for “easy to fix”?
:::

---

# Step 3: Create Your Project and Write Some Code

:::imagecard center cat-computer.jpg
:::

We’re going to be creating a very simple “hello world” application.
Let’s put it in `$HOME/code/awesomehello` . Create/enter that directory and run:

```bash
poetry init
```

This will create you a basic `pyproject.toml` file describing your package.
Create an empty `README.md` as well, since Poetry likes you to have one.

```bash
touch README.md
```

The source code for this project will be very quick:

1. Create an `awesomehello` directory (yes, inside the one already called `awesomehello`).
   This will be the package which gets imported whenever any code runs `import awesomehello`.
2. Create an empty `__init__.py` in that directory. This marks the directory as a regular
   (rather than namespace) package.
3. Create a file in that directory, called `hello.py`. Put the following in it:

   ```python
   def say_hello(name: str):
       print(f"Hello, {name}!")

   def hello_world():
       say_hello("world")
   ```

That’s it! Now, back in the main directory for the project (`$HOME/code/awesomehello`), run:

```bash
poetry install
```

This command did a few things:

- It created _yet another_ virtualenv, this time specific to _just this project_.
  This way, you can install dependencies into this virtualenv (as you will see in a bit),
  without them being installed in either `PYVENV`, `PYROOT`, or your OS’s Python.
- It started a new `poetry.lock` file. This file contains super-exact “locked”
  specifications for your dependencies. You’ll see more on this later as well.
- It installed your `awesomehello` package code in the new virtualenv.

:::imagecard center xzibit-venv.jpg
:::

Where is this virtualenv? That depends on your OS, but ultimately it doesn’t matter.
In the same way that in the previous sections you accessed different Python interpreters
using `$PYVENV/python` versus `$PYROOT/python` versus `/usr/bin/python`, Poetry lets you
get to its venv with a command prefix as well: `poetry run`.

The `poetry run` command takes any other command after it, and runs it within the context
of the project’s virtualenv. If you have multiple projects, it even selects the correct
virtualenv based on your current directory. You can also use `which` (or on Windows, `where`)
to find the actual virtualenv’s path as well.

```bash
# poetry run which python
/home/fsufitch/.cache/pypoetry/virtualenvs/awesomehello-rRmrMFYP-py3.11/bin/python

# poetry run python -c 'from awesomehello.hello import say_hello; say_hello("Filip")'
Hello, Filip!
```

As you can see, using `poetry run` allowed a quick Python snippet to import the `say_hello`
function from above, and use it!

:::alert info
If you really hate prefixing stuff with `poetry run`, you can use the `poetry shell`
command, to modify your current shell so that simply `python` and other related
commands refer to the correct versions from the project virtualenv. I like the
explicitness of poetry run though. It means that my different terminals all have
a consistent value for python (specifically `$PYVENV/python`), so I don’t confuse
myself.
:::

Finally, if you are using your favorite handy IDE, you can give it the output of
`poetry run which python` in its settings, wherever the “Python interpreter” is
specified. Visual Studio Code, for example, has a command under `Ctrl+Shift+P `named
`Python: Select Interpreter`, which lets you paste in the path to the Python
interpreter to use:

:::imagecard center vscode-select-python.png
:::

You can tell it worked because it then displays this on its status bar,
indicating it is using the stuff in that specific virtualenv, rather than any
other Python environment:

:::imagecard center vscode-python-status.png
:::

This same functionality is available in all other Python IDEs I’ve worked with.
How to do it in your favorite one is left up to you.

## Creating an Executable

Running the code with poetry run `python -c 'import ...; ...'` is cumbersome. Wouldn’t it be cooler if there were a way to make an actual executable to run it? There is! Add the following snippet to `pyproject.toml`:

```ini
[tool.poetry.scripts]
hello = 'awesomehello.hello:hello_world'
```

Then, run `poetry install`. Now, try running `poetry run hello`.

```
Hello, world!
```

The scripts tool generated a `hello` script file! `poetry run which hello` says:

```
/home/fsufitch/.cache/pypoetry/virtualenvs/awesomehello-rRmrMFYP-py3.11/bin/hello
```

And its contents are:

```python
#!/home/fsufitch/.cache/pypoetry/virtualenvs/awesomehello-rRmrMFYP-py3.11/bin/hello
import sys
from awesomehello.hello import hello_world

if __name__ == '__main__':
    sys.exit(hello_world())
```

It did the hard work for us! Not only that, but if we were in a shell where the
virtualenv is on the current PATH (using `poetry shell`, or by installing
`awesomehello` in the `PYVENV` Python, or our system Python), all we have to do
to run the “hello world” script is to simply run `hello`.

---

# Step 4: Managing your Dependencies

:::imagecard center python-depends.jpg
Your code "depends" on stuff. Get it?
:::

Say you found this awesome library called
[`pyfiglet`](https://pypi.org/project/pyfiglet/). It turns text into ASCII art!
Let’s build it into `awesomehello`.

Your first instinct to install `pyfiglet` so your code can use it may be to use Pip,
perhaps running `poetry run pip install pyfiglet`. It may even appear to work at first.
**This is wrong**, however. Using Pip in this manner does indeed install `pyfiglet`
into the project’s virtualenv; however, the fact that your code depends on it is not
saved anywhere.

Before [PEP 517](https://peps.python.org/pep-0517/), common practice for keeping
track of dependencies was to have a requirements.txt containing the list, and using
`pip install -r requirements.txt` to install them. Another one was to have a project
`setup.py` and have the dependencies specified via `setuptools`. Neither of these
is best practice as of time of writing.

Instead, the dependencies are listed in `pyproject.toml`, under a section specific
to whatever build tool you’re using (in this case, Poetry). You can edit the file
yourself, and in the `[tool.poetry.dependencies]` section, add the line
`pyfiglet = "^0.8.post1"`. That’s rough though, since you need to look up the proper
`pyfiglet` version, think about the [semantic string format](https://semver.org/), etc.
Why not just use this quick command instead?

```bash
poetry add pyfiglet
```

This will do all of that for you, plus check it against any other project
dependencies (none in the current case, but still) and ensure that there are no
version mismatches.

Whenever you edit the dependencies in `pyproject.toml`, you should follow it up with:

```bash
poetry lock
```

The `lock` command updates the `poetry.lock` file with the hashes of your dependencies.
If you look in there, you’ll perhaps see something like this:

```ini
[[package]]
name = "pyfiglet"
version = "0.8.post1"
description = "Pure-python FIGlet implementation"
category = "main"
optional = false
python-versions = "*"

[metadata]
lock-version = "1.1"
python-versions = "^3.11"
content-hash = "f72a0bf53f693600b240bf57d434e9a37815e26d3d2953974c6dbbdab73b74ec"

[metadata.files]
pyfiglet = [
    {file = "pyfiglet-0.8.post1-py2.py3-none-any.whl", hash = "sha256:d555bcea17fbeaf70eaefa48bb119352487e629c9b56f30f383e2c62dd67a01c"},
    {file = "pyfiglet-0.8.post1.tar.gz", hash = "sha256:c6c2321755d09267b438ec7b936825a4910fec696292139e664ca8670e103639"},
]
```

The lock file is used whenever you run `poetry install` to make sure you have the
**absolute exact and correct version** for each dependency. That is, if you took this
code and put it on a different computer, then recreated the virtualenv on that
computer (using poetry install), you are guaranteed that the pyfiglet package
not only says it has version `0.8.post1` , but that even the hash of the downloaded
file is the exact same. If it is not the same, Poetry will tell you.

:::alert info
Note: Technically, `poetry add` and a few other commands run `poetry lock `implicitly.
Still, it’s good to keep in mind: always remember to lock your dependencies.
Poetry will helpfully remind you if `pyproject.toml` and `poetry.lock` are out of
sync, too.
:::

You don’t actually ever need to look at `poetry.lock` again. It’s not really meant
for human consumption. However, you should absolutely add it to your source control
(Git, SVN, or whatever).

Alongside `poetry add`, there is also `poetry remove` for doing the opposite.
Alternatively, you could remove the line from pyproject.toml yourself, then run `poetry lock`.

## Updating Dependencies

:::imagecard upgrade-button.jpg
:::

It just so happens now and then that versions of your dependencies update. Thanks
to the “locking” mechanism for above, though, Poetry will never install anything
except the very specific version that your project is “locked” to. That’s good
from a consistency and security aspect, but what if you want the new version?

Poetry has a helpful `poetry update` command for handling this. However,
it may not be as intuitive as it immediately appears.
To demonstrate this, run `poetry add django==3.2.1`.

If you then run `poetry show django` (to show the details of that installed package), you would see:

```
name         : django
version      : 3.2.1
```

That’s cool. It did what we expected, and installed version `3.2.1`.
However, version `3.2.16` is out, and you might want to upgrade to it.
So, let’s try running `poetry update`.

```
No dependencies to install or update
```

Uh-oh! What gives? `poetry show django` says we’re still using `3.2.1` as well!
Why did the update not, well, update?

_Poetry does not second-guess you on what is in `pyproject.toml`_.
If you open the file and read it, you’ll see `django = "3.2.1"`. That means
your project depends on _exactly_ `3.2.1`; no more, no less.

Try to edit that line so it reads `django = "^3.2.1"` instead (or, run
`poetry add 'django@^3.2.1'`. The `^` is part of Poetry’s dependency specification syntax,
and `^3.2.1` translates to "`3.2.1` or newer, but not as new as anything 4".
Or, in Pip’s dependency syntax, `>=3.2.1,<4`.

After that edit, if you run `poetry update`, it will correctly jump to `3.2.16` —
but not to the true latest, which is `4.1.3`.

```
  • Updating django (3.2.1 -> 3.2.16)
```

:::imagecard center feelsgood.jpg
:::

Thus, if you had wanted to upgrade to Django of the 4-series, you would have to
modify your project definition manually (by editing `pyproject.toml` or running
`poetry add django@^4`) before running `poetry update`.

:::alert info
`poetry lock` implicitly runs a `poetry update` as well.
You can stop it doing so by using its `--no-update` option.
:::

Poetry also takes a variety of other syntaxes beyond `^`. Check its documentation
for more details: https://python-poetry.org/docs/dependency-specification/

---

# Step 5: Adding Dev-Time Tools

A proper Python project that goes beyond light scripting is going to need a
variety of tools: tests, linting, static checking, and more.
These are not technically _dependencies_ of your code; all the `awesomehello`
package and `hello` command really needs is `pyfiglet`.
However, the dev tools should be version-locked and installed too, or your
dev experience is going to suck.

Poetry 1.2 features the concept of optional dependency “groups” beyond the
default ones. You can then add those tools to a group called “dev”.

```bash
poetry add --group=dev pytest black pyright
```

If you look in `pyproject.toml`, you’ll see a new section:

```ini
[tool.poetry.group.dev.dependencies]
pytest = "^7.2.0"
black = "^22.10.0"
pyright = "^1.1.279"
```

These tools will also be accessible using `poetry run`.

```bash
# poetry run black ./awesomehello/
reformatted ./awesomehello/hello.py

All done! ✨ 🍰 ✨
1 file reformatted, 1 file left unchanged.
```

Your IDE should also recognize these are available, and be able to take
configuration to use them.

---

# Step 6: Building and Packaging

:::imagecard cat-box.gif
:::

All of this Poetry stuff is cool, but not every Python user will have it
installed. In fact, most of them likely do not. How could they use this
great package you just made? All they know for installation is `pip`.

There is plenty of good news here. First, `pip` knows how to read `pyproject.toml`;
thanks to the PEP 517 standard, it then knows how to interpret the
Poetry-specific sections, and install exactly what you need — even without
Poetry being on the system. That means that one way to give your friend
your code is to just give them your source code, and tell them to run
`pip install /path/to/the/code/dir`.

It gets even easier though! What about running `poetry build`?

```
Building awesomehello (0.1.0)
  - Building sdist
  - Built awesomehello-0.1.0.tar.gz
  - Building wheel
  - Built awesomehello-0.1.0-py3-none-any.whl
```

That command created two different “distributions” of `awesomehello`,
in the `dist/` directory. These can be shipped around and installed
directly with Pip. They should work regardless of OS (hence the `any` on
the wheel distribution), and will make sure to install `pyfiglet` on the
user’s computer, but none of the `dev` dependencies (since they’re not necessary).

Even better, these distribution files can be uploaded to the
[Python Package Index](https://pypi.org), so anyone around the world can
get your package by using the command `pip install awesomehello`. You can
also automate uploading it to PyPI, or even other custom repositories,
using the `poetry publish` command.

All of these methods take advantage of the advanced tools, version locking,
and other features of Poetry, without the end user’s computer ever needing
to know Poetry was involved.

---

# The End...?

:::imagecard right shakespeare.jpg
Just some other guy who cared too much about poetry.
:::

That was quite a trip, wasn’t it? You ended up with a well-configured,
standalone, isolated package of Python code, ready to receive your latest
awesome idea or hare-brained experiment. Its dependencies are super
consistent, meaning that teams of developers can be sure that they are
actually using the same tools (even across different OSes).

Despite the longwindedness of this article, I hope I’ve given you an
awesome new tool for your development toy-box.

Happy coding!

:::alert success
This post was [originally published on Nov 15, 2022 to my Medium blog](https://medium.com/@fsufitch/filips-awesome-overcomplicated-python-dev-environment-dd24ee2a009c).
This re-post is an update containing some corrections and additional content.
:::
