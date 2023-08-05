# newpyter

New and better jupyter for teams. 

- Newpyter ❤️ git: notebooks can be versioned and merged without pain
- Newpyter ❤️ IDEs: notebook contents are plain python (markdown represented as a string literal)
- Newpyter ❤️ outputs: outputs are not discarded, but stored separately from code
- Newpyter ❤️ Jupyter: continue working from your favourite environment

Project status is much beta (much betta than nothing). Expect some changes.

## Setup

Make sure you're using fresh jupyter; Install newpyter
```bash
pip install notebook nbformat jupyterlab jupyter_core jupyter_server --upgrade
pip install newpyter
```


Generate config with `jupyter notebook --generate-config` (do not overwrite if exists).

Add following to your jupyter config (usually `~/.jupyter/jupyter_notebook_config.py`):
```python
from newpyter import patch_jupyterlab_frontend
patch_jupyterlab_frontend()

c.ServerApp.contents_manager_class = "newpyter.ContentsManager.NewpyterContentsManager"
```

Create configuration file `~/.newpyter_config.toml` with following content:
```toml
[newpyter]
local_cache_dir = "~/.newpyter_cache/"

default_storage = "local"
# default_storage = "ssh://<server ip or hostname>:/path/to/newpyter_output_storage/"
# default_storage = "s3://<yourbucket>/newpyter_output_storage/"
```

Select only one storage, comment out or delete others.
This defines where outputs are going to be stored. 

## Get started

Start (or restart) `jupyter lab` or `jupyter notebook` as usual.

Open a notebook from `demo` folder, run it, save it. Look at how original file is changed 
(outputs are going to be stored in your storage, links added to original text). 

Pick one of your notebooks, rename if from `<notebookname>.ipynb` to `<notebookname>.newpy` in jupyter.
This converts notebook between two formats. Conversion works just as well when renaming back.

Tip: if you're disconnected from the network, use ipynb, and convert back to newpy when want to commit in git or share.


## Creating a new notebook

- create an empty text file with extension `.newpy`, e.g. `touch my_notebook.newpy`
- ... or create an `.ipynb` notebook, rename to `.newpy`

## How do I share newpyter notebooks with my team?

- select storage that is available to every member of your team (ssh access or s3 bucket), set it in `.toml`
- each member working with notebooks follows "Setup" part (or admin magically makes this for everyone)
- commit `.newpy` as ordinary files. Or send as text files. Or paste as text in chats. Why not if you can?

## Can I setup storage individually for a project?

Yes, create `.newpyter_config.toml` in the project root, this will apply to all notebooks.
It is possible override configs for sub-folders.
It is recommended to define `local_cache_dir` in user-level config, not in project-level config.

## Troubleshooting

If `newpyter` does not seem to work, check output of process, below is an example. 

<img width="973" alt="Screen Shot 2021-05-20 at 1 31 46 PM" src="https://user-images.githubusercontent.com/6318811/119045383-3e70fd00-b970-11eb-9679-e2594d48b289.png">

Newpyter informs that it patched frontend code (or it was patched previously), and then informs that it was activated. If both pieces missing - your config file probably was not picked up. If it fails during patching, make sure to provide write permission for the being patched. If it is not activated, check your config again.


## Convenience

Following steps are all optional, but those are real benefits of using .newpy over .ipynb 

- setup IDE to treat notebooks as regular python files 
  - `Pycharm:` Settings > File Types > Python > add '*.newpy'
  - `VS Code:` Settings > File Associations > Add Item > add Item "*.newpy", value is "python"

- after setting up your IDE, play with these functions to better understand benefits
  ```
    - navigate to definition of a function, find usages of a function
    - reformat notebook or fragment of a notebook
    - check that IDE shows unused imports
    - check that undefined variables are reported  
    - check that refactoring (e.g. renaming of a function) works
    - try merging or splitting cells by editing the text file, not in jupyter interface
    - move outputs between cells by moving around lines with # Out: ...
    - duplicated output line, see how that changes
    - do you write SQL in IDE? If you use sql hinting, you can now use it with notebooks!
  ```
- github highlighting for ".newpy"
  - see `.gitattributes` in this repository, you can just copy it

- reloading the notebook after editing in IDE:
  - in Jupyter Notebook, reload the page
  - in Jupyterlab, use File > "reload notebook from disk", you can create a key binding by plugging this 
    ```
    {
        ... other config stuff goes here ...
        "shortcuts": [
            {
                "command": "docmanager:reload",
                "keys": ["Ctrl R",], # change keystroke!
                "selector": "body"
            }
        ]
    }
    ```

- You may want to add automated formatting/linting for `.newpy` notebooks.
  Use your team's conventions


## Other approaches

Making a friendship between jupyter and git is a long-standing problem 
that every team approaches in their own way. 
Below are some commonly known choices:

- notebooks are rare and small <br /> → just save in git
- need to share notebook with wide audience <br /> → just save in git, share link to nbviewer / colab
- don't care about outputs and no need to diff/merge <br /> → strip output and save
- don't care about outputs, but need to merge/diff code 
  <br /> → use only code cells and export/import to script. 
  <br /> →  or use Spyder
  <br /> →  or use VS Code special mode for python scripts 
  <br /> →  or use JupyText, it also keeps most of your local outputs

- keeping notebooks is important, diffs not needed, merging required, outputs are small (you don't expect to go over github limits)
  <br /> → use nbdev (?)
  

- want to keep outputs, need to diff/merge, need to update notebooks during refactoring, want code monitoring for notebooks, many notebooks, within a team
  <br /> → use newpyter
