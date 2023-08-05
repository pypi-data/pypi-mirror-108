import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='alert-close',
     version='0.1.1',
     author="Oleksii Tkachuk",
     author_email="tkalexey@gmail.com",
     description="Squish alert close",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/oleksiitkachuk-sq/sq_alert_close",
     packages=setuptools.find_packages(where="src"),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     package_dir={"": "src"},
     python_requires=">=3.6",
 )
