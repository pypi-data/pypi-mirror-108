<h1>pyFileArchiver Manual</h1>

<h2>Install</h2>

<p>1.Open your project in terminal</p>
<p>2.Input "pip install pyFileArchiver"</p>

<h2>Example</h2>

```python
from pyFileArchiver.archiver import arcZip, arcExtract


arcZip('path/to/save/archive.zip', [
    'path/to/archive/directory',
    'path/to/archive/file',
], 'extension for archiving specific files (default: None)')

arcExtract('path/to/archive.zip', 'path/to/extract/archive.zip', [
    'file names if you want to extract specific files (default: None)'
])
```
