import setuptools

setuptools.setup(
    name="me_main_libs",
    version="0.0.1",
    description='Main python libraries',
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'matplotlib', 'requests',
                      'requests_cache', 'numpy', 'bs4',
                      'tqdm', 'pytz'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
