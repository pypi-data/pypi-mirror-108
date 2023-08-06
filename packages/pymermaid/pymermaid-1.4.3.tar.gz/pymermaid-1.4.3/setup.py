from setuptools import setup

setup(name='pymermaid',
      version='1.4.3',
      description='(firefox recommended)a package in getting images output from mermaid markdown tags. Especially this package could be used in jupyter lab or notebook, cause it is lack of flowchart\gatt\seqeunses',
      author='Gavin Long',
      author_email='longgenxing@126.com',
      url='https://gitee.com/longgenxing/jupyter_mermaid',
      license='MIT',
      keywords='mermaid jupyter lab notebook',
      project_urls={
            'Documentation': 'https://gitee.com/longgenxing/jupyter_mermaid',
            'Funding': 'https://gitee.com/longgenxing/jupyter_mermaid',
            'Source': 'https://gitee.com/longgenxing/jupyter_mermaid',
            'Tracker': 'https://gitee.com/longgenxing/jupyter_mermaid',
      },
      packages=['pymermaid'],
      install_requires=['matplotlib>=3.0.0','matplotlib-inline>=0.1.0','selenium>=3.0.0'],
      python_requires='>=3'
     )
