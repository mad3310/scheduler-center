from setuptools import setup, find_packages

files = ["config/*"]

setup(
    name="schedulercenter",
    version="1.0.0",
    keywords=("schedulercenter"),
    description="scheduler center",
    long_description="scheduler center",
    license="MIT Licence",

    url="http://scheduler-center.com",
    author="zhoubingzheng",
    author_email="zhoubingzheng@sina.com",

    packages=find_packages(),
    package_data = {'schedulercenter' : files },
    include_package_data=False,
    platforms="any",
    install_requires=[
        'requests==2.6.0',
        'apscheduler==3.6.0',
        'rq==1.0',
        'tornado==4.4.2'
    ],

    scripts=[],
    entry_points={

    }
)
