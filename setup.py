import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="piicrgmms",
    version="0.1.4",
    author="Colin Weber",
    author_email="colin.weber.27@gmail.com",
    url='https://pypi.org/project/piicrgmms/',
    description="A data analysis package for PI-ICR Mass Spectrometry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        'Homepage': 'https://pypi.org/project/piicrgmms/',
        'Source code': 'https://github.com/colinweber27/piicrgmms',
        'Download': 'https://pypi.org/project/piicrgmms/#files',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires='>=3.6',
    install_requires=[
        'scikit-learn',
        'pandas',
        'matplotlib',
        'lmfit',
        'joblib',
        'tqdm',
        'pillow',
        'webcolors'
    ],
    keywords=[
        'Gaussian Mixture Models',
        'Clustering Algorithms',
        'Machine Learning',
        'Mass Spectrometry'
    ]
)
