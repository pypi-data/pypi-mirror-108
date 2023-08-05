import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leecarter",
    version="1.0.0",
    author="Andy Chen",
    author_email="andy97_861022_chen@hotmail.com",
    description="leecarter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andy971022/leecarter",
    packages=setuptools.find_packages(),
    classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy>=1.18.0'
    ],
    python_requires='>=3.6',
)
