from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

if __name__ == "__main__":

    setup(
        name="anonomatic_client",
        version="0.0.2",
        author="Andrew Gross",
        author_email="andrew.w.gross@gmail.com",
        description="Simple Anonomatic Client",
        long_description=readme + '\n\n' + changelog,
        long_description_content_type="text/markdown",
        url="https://github.com/andrewgross/anonomatic_client",
        packages=find_packages(exclude=["*tests*"]),
        install_requires=[
            "requests>=2.0.0"
        ],
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3 :: Only",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.5"
    )
