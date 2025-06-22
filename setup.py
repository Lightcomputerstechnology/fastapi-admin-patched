from setuptools import setup, find_packages

setup(
    name="fastapi-admin",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "tortoise-orm",
        "jinja2",
        "python-multipart",
        "redis>=4.5.0",
        "pydantic",
    ],
    extras_require={
        "tortoise": ["aerich"],
    },
)
