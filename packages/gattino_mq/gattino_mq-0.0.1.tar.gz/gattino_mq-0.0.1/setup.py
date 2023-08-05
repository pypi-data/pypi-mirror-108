from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="gattino_mq",
    install_requires=[
        "gattino",
        "redis"
    ],
)
