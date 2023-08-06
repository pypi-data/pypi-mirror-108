from setuptools import setup, find_packages

setup(
    name='pakfortabletocolumn',
    version='0.1.4',    
    description='table to column',
    url='https://github.com/susaninsl/pakfortabletocolumn',
    author='Sviat',
    author_email='susaninsl@gmail.com',
    license='BSD 2-clause',
    packages=['pakfortabletocolumn'],
    entry_points ={
        'console_scripts': [
            'pftc = pakfortabletocolumn.tabletocolumn:main'
        ]
    },
    install_requires=['xlrd',
                      'xlwt',
                      'argparse',
                      'xlutils',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',     
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
