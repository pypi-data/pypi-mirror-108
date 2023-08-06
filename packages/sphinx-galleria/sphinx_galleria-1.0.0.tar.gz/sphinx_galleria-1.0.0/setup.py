from setuptools import setup
import distutils
from babel.messages import frontend as babel


class TranslateCommand(distutils.cmd.Command):
    description = "Translation"

    user_options = []
    sub_commands = [
        ('extract_messages', None),
        ('update_catalog', None),
        ('compile_catalog', None),
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)


with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="sphinx_galleria",
    version="1.0.0",
    url="https://procrastinator.nerv-project.eu/nerv-project/sphinx_galleria",
    license="EUPL 1.2",
    author="Kujiu",
    author_email="kujiu-pypi@kujiu.org",
    description="Create image galleries with Sphinx",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=["sphinx_galleria"],
    cmdclass={
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog
    },
    package_data={
        "sphinx_galleria": [
            "*.py",
            "static/sphinxgalleria/*.mjs",
            "static/sphinxgalleria/*.css",
        ]
    },
    install_requires=["sphinx>=3.0.0"],
    classifiers=[
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Extension",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ],
    keywords="sphinx image gallery",
    project_urls={
        "Source": "https://procrastinator.nerv-project.eu/nerv-project/sphinx_galleria",
        "Issues": "https://procrastinator.nerv-project.eu/nerv-project/sphinx_galleria/issues",
    },
)
