import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easypostgre",
    version="0.0.5",
    author="Benito Gonzalez",
    author_email="benitogonzalezh@gmail.com",
    description="Wrapper to simplify the use of psycopg2 lib",
    long_description="Wrapper to simplify the use of psycopg2 lib",
    long_description_content_type="text/markdown",
    url="https://github.com/benitogonzalezh/easypostgre",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
	    "Development Status :: 1 - Planning"
    ],
)
