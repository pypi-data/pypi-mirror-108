import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="pyindia_zipcode",
    version="0.0.0",
    author="T.THAVASI GTI",
    license="MIT",
    author_email="ganeshanthavasigti1032000@gmail.com",
    description="Indian Post office zip code Information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source":"https://github.com/THAVASIGTI/pyindia_zipcode.git",
        "Tracker":"https://github.com/THAVASIGTI/pyindia_zipcode/issues",
    },
    zip_safe=True,
    data_files=[('Store', ['pyindia_zipcode/Store.db'])],
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities'],
    install_requires=["requests"],
    python_requires='>=3',
)