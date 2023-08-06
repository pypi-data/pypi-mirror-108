from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="sl-whatsapp",
    version="1.3.9",
    description="A Python package to send admin message.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/shehan9909/whatsapp",
    author="shehan_slahiru",
    author_email="www.shehan6472@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["sl_whatsapp"],
    include_package_data=True,
    install_requires=["twilio"],
    entry_points={
        "console_scripts": [
            "sl-whatsapp=sl_whatsapp.__main__:main",
        ]
    },
)
