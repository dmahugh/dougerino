# dougerino
Library of functions for common Python development tasks.

## ChangeDirectory

For tools that work with files and folders, it's often useful to temporarily change the current working directory. This context managers provides a simple syntax for changing to another directory and then reverting to the prior working directory when don

```python
from dougerino import ChangeDirectory
with ChangeDirectory(folder):
    pass # code that should run in folder
# returns to previous working directory when done
```
