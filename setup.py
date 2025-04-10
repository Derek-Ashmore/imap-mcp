from setuptools import setup, find_packages

setup(
    name="imap-mcp",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "python-dotenv>=1.0.0",
        "fastmcp>=0.1.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
    ],
    python_requires=">=3.8",
    author="Your Name",
    author_email="derek.ashmore@asperitas.consulting",
    description="IMAP MCP Server",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/imap-mcp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "imap-mcp=imap_mcp.server:main",
        ],
    },
) 