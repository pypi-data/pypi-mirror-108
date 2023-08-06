import setuptools

setuptools.setup(
    name="ratsnlp",
    version="0.0.9981",
    license='MIT',
    author="ratsgo",
    author_email="ratsgo@naver.com",
    description="tools for Natural Language Processing",
    long_description=open('README.md').read(),
    url="https://github.com/ratsgo/ratsnlp",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data = {
        'ratsnlp.nlpbook.classification': ['*.html'],
        'ratsnlp.nlpbook.ner': ['*.html'],
        'ratsnlp.nlpbook.qa': ['*.html'],
        'ratsnlp.nlpbook.paircls': ['*.html'],
        'ratsnlp.nlpbook.generation': ['*.html'],
    },
    install_requires=[
        "torch==1.8.1",
        "pytorch-lightning==1.3.4",
        "transformers==4.6.1",
        "Korpora>=0.2.0",
        "flask>=1.1.4",
        "flask_ngrok>=0.0.25",
        "flask_cors>=3.0.10",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)