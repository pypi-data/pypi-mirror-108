import setuptools

setuptools.setup(
    name='OpenWebPortal',
    version='0.1.0',    
    description='Edit variables on a web portal',
    url='https://github.com/Alex40144/OpenWebPortal',
    author='Alex40144',
    license='GNU GPLv3',
    install_requires=['flask',                    
                      ],

    classifiers=[
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)