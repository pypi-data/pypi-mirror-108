import setuptools

setuptools.setup(
    name="me_helpers_lib",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=['me_main_libs', 'bokeh',
                      'pandas', 'numpy',
                      'psutil', 'Pillow', 'PyPDF2',
                      'redis-decorator', 'redis'
                      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
