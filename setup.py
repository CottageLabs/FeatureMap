from setuptools import setup, find_packages

# ~~Setup:Core~~
setup(
    name='featuremap',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "lark==0.11.1",
        "jinja2==2.11.3",
        "pyyaml==5.4.1",
        "markupsafe==2.0.1"
    ],
    url='https://cottagelabs.com/',
    author='Cottage Labs',
    author_email='richard@cottagelabs.com',
    description='For annotating text files with features and their connections to other features.',
    license='Apache2',
    classifiers=[],
    entry_points={
        'console_scripts': [
            # ~~-> CLI:Entrypoint ~~
            'featuremap=featuremap.cli:main',
        ],
    }
)
