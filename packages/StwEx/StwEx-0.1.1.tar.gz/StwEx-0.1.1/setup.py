import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StwEx",
    version="0.1.1",
    author="German Sanchez Gutierrez",
    author_email="gsgsoftgroup@gmail.com",
    description="Controlar cualquier aplicación desde un icono con menú y submenus en el systray",
    license="GNU General Public License v3 (GPLv3)",
    platforms="Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/germansg/stwex",
    packages=setuptools.find_packages(include=['stwex','stwex/stwex.py','stwex/images'], exclude=['stwex/old_files']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    package_data={'stwex': ['images/*.*']},
    include_package_data=True,
    install_requires=['wxPython>=4.1.1'],
    entry_points={
        'console_scripts': [
            'stwex = stwex.stwex:main',
        ],
    },
)