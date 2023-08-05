# pyArchiver
## Example

```python
from pyArchiver.pyArchiver import toZip, unzipping


toZip('path where do you want to save archive.zip', [
    'path to archive directory',
    'path to archive file',
])

unzipping('path to archive.zip', 'path where do you want to unzipping archive.zip(default: path to folder with archive)')

```