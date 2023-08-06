import setuptools
import pkg_resources

with open("requirements.txt", "r") as f:
    requirements = [str(req) for req in pkg_resources.parse_requirements(f)]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="curve_linear",
    version="0.0.0",
    author="@not-so-fat",
    author_email="conjurer.not.so.fat@gmail.com",
    description="Linear model of monotonic curves of each feature",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/not-so-fat/curve_linear",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
