import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
        name="satisfy-calc",
        version="1.1.2",
        description="Command line crafting tree visualizer for Satisfactory Game by CoffeeStain Studios",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/sedatDemiriz/satisfy-calc",
        author="Sedat Demiriz",
        author_email="sedatdemiriz97@gmail.com",
        license="MIT",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
        install_requires=["bs4", "jsonpickle", "requests"],
        packages=["satisfy_calc"],
        entry_points={
            "console_scripts": [
                "satisfy_calc=satisfy_calc.__main__:main"
            ]
        },
    )

# setup(
#     name="realpython-reader",
#     version="1.0.0",
#     description="Read the latest Real Python tutorials",
#     long_description=README,
#     long_description_content_type="text/markdown",
#     url="https://github.com/realpython/reader",
#     author="Real Python",
#     author_email="info@realpython.com",
#     license="MIT",
#     classifiers=[
#         "License :: OSI Approved :: MIT License",
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.7",
#     ],
#     packages=["reader"],
#     include_package_data=True,
#     install_requires=["feedparser", "html2text"],
#     entry_points={
#         "console_scripts": [
#             "realpython=reader.__main__:main",
#         ]
#     },
# )

