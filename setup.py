"""Setup script for the GivingTuesday Campaign Advisor package."""

from setuptools import find_packages, setup

setup(
    name="gt-campaign-advisor",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "langchain>=0.1.8",
        "langchain-community>=0.0.19",
        "langchain-openai>=0.0.5",
        "langchain-anthropic>=0.1.1",
        "langchain-chroma>=0.1.0",
        "openai>=1.10.0",
        "anthropic>=0.23.3",
        "chroma-hnswlib>=0.7.3",
        "chromadb>=0.4.22",
        "faiss-cpu>=1.7.4",
        "pydantic>=2.5.3",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.8.0",
        "pandera>=0.17.2",
        "pandas>=2.1.3",
        "typer>=0.9.0",
        "tqdm>=4.66.1",
        "rich>=13.6.0",
        "fastapi>=0.105.0",
        "uvicorn>=0.24.0",
        "python-multipart>=0.0.6",
        "jinja2>=3.1.2",
    ],
    entry_points={
        "console_scripts": [
            "gt-advisor=src.cli.app:main",
        ],
    },
    python_requires=">=3.10",
    author="GivingTuesday Campaign Advisor Team",
    author_email="example@example.com",
    description="AI-powered advisor for GivingTuesday campaigns",
    keywords="givingtuesday, campaign, advisor, ai, langchain",
    url="https://github.com/example/gt-campaign-advisor",
    project_urls={
        "Bug Tracker": "https://github.com/example/gt-campaign-advisor/issues",
        "Documentation": "https://github.com/example/gt-campaign-advisor/blob/main/README.md",
        "Source Code": "https://github.com/example/gt-campaign-advisor",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)