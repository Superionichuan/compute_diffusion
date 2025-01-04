from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="compute_diffusion",  
    version="1.0.0",  
    author="Sun Shichuan",  
    author_email="shichuan.sun@gmail.com",
    description="A Python tool to calculate diffusion coefficients from MSD data.",
    long_description=long_description,  # 项目描述
    long_description_content_type="text/markdown",  
    url="https://github.com/Superionichuan/compute_diffusion",  
    packages=find_packages(),  
    py_modules=["compute_diffusion"],  
    python_requires=">=3.6",   
    entry_points={
        "console_scripts": [
            "compute-diffusion=compute_diffusion.compute_diffusion:main",  
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

