from setuptools import setup, find_packages

setup(
    name="devpulse-ai",
    version="1.0.0",
    author="Aastha Rawat",
    author_email="aastharawat47849@gmail.com",
    description="Autonomous Code Security Auditor & GitHub PR Review Agent",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aastharawat47849-oss/DevPulse-AI",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    install_requires=[
        "fastapi>=0.110.0",
        "uvicorn>=0.28.0",
        "pydantic>=2.6.4",
        "httpx>=0.27.0",
        "python-dotenv>=1.0.1",
    ],
    entry_points={
        "console_scripts": [
            "devpulse=app.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.11",
)
