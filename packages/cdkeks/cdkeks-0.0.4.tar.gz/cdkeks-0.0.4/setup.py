import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdkeks",
    "version": "0.0.4",
    "description": "Higher-level hybrid cdk|cdk8s construct to build an eks kubernetes platform with batteries included",
    "license": "MIT",
    "url": "https://github.com/hupe1980/cdkeks",
    "long_description_content_type": "text/markdown",
    "author": "hupe1980",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/hupe1980/cdkeks.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdkeks",
        "cdkeks._jsii"
    ],
    "package_data": {
        "cdkeks._jsii": [
            "cdkeks@0.0.4.jsii.tgz"
        ],
        "cdkeks": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-certificatemanager>=1.107.0, <2.0.0",
        "aws-cdk.aws-ec2>=1.107.0, <2.0.0",
        "aws-cdk.aws-efs>=1.107.0, <2.0.0",
        "aws-cdk.aws-eks>=1.107.0, <2.0.0",
        "aws-cdk.aws-elasticloadbalancingv2>=1.107.0, <2.0.0",
        "aws-cdk.aws-elasticsearch>=1.107.0, <2.0.0",
        "aws-cdk.aws-iam>=1.107.0, <2.0.0",
        "aws-cdk.aws-logs>=1.107.0, <2.0.0",
        "aws-cdk.aws-route53>=1.107.0, <2.0.0",
        "aws-cdk.aws-s3>=1.107.0, <2.0.0",
        "aws-cdk.core>=1.107.0, <2.0.0",
        "cdk8s-plus-17>=1.0.0.b20, <2.0.0",
        "cdk8s==1.0.0.b14",
        "constructs>=3.3.75, <4.0.0",
        "jsii>=1.30.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
