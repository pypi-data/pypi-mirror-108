### The module will be use webbrowser as a render for mermaid markdown tags; and will return the graph as matplot image object
### You can modify the package with edit the __MermaidMarkdown.py__ file, add your function, or get images in __png__ type

### step 1:
install automation tests tools
- pip install selenium
install web browser and its webdriver
- windows: install chrome or firefox, webdrivers
- ubuntu linux: install web browser, desktop or server works well in headless browser mode
    take ubuntu and firefox for example:
    - _sudo apt install firefox_
    - _sudo apt install firefox-geckodriver_
    * note * the driver and the browser version are match will be better

### step 2:
download this package, decompress, and install pymermaid
- windows: _python setup.py install_
- ubuntu linux: _sudo python setup.py install_

### step 3:
try this:

```python
from pymermaid import MermaidMarkdown

MermaidMarkdown.render('''

graph TD

​	A[first]-->B[second]

​	B-->C[third]

​	C-->D[end]

​	A->D

''')
```


### More Control In Addition:
```python
# To control image size, and dpi(pixel per inch)
# def render(tags=tags, conf_axis="off", figsize=(height, width), dpi=72)

from pymermaid import MermaidMarkdown

MermaidMarkdown.render(tags='''

graph TD

​	A[first]-->B[second]

​	B-->C[third]

​	C-->D[end]

​	A->D

''', conf_axis="on", figsize=(15, 20), dpi=300)
```