import setuptools
import os
import importlib.util

spec = importlib.util.spec_from_file_location('grey_models', os.path.join(os.getcwd(), 'greyai_sdk', 'version.py'))
model_pkg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model_pkg)

setuptools.setup(
    name='greyai-sdk',
    version=model_pkg.__version__,
    author="Grey Development Team",
    author_email="dev@greyai.io",
    description="Grey AI Model Builder SDK",
    long_description_content_type="text/markdown",
    url="",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(where="."),
    python_requires=">=3",
    entry_points={'console_scripts': ['grey = greyai_sdk.cli:main']},
    install_requires=[
        'tensorflow==2.4.1',
        'fastapi==0.64.0',
        'pydantic==1.8.2',
        'click==8.0.1'
    ]
)

