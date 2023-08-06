from typing import Dict
import os
import shutil
import subprocess
from uuid import uuid4
from aws_cdk import core
import aws_cdk.aws_lambda as lambda_


class AppLambdaLayer(lambda_.LayerVersion):

    def __init__(self, scope: core.Construct, construct_id: str,
                 build_path: str = None,
                 include: Dict[str, str] = None, **kwargs,
                 ):
        """
        :param scope:
        :param construct_id:
        :param build_path: Absolute build directory path
        :param include: Dictionary that maps absolute paths to be included to -> lambda layer paths
        :param kwargs: compatible_runtimes (required), ...
        """
        if build_path is None:
            build_path = "_build_" + uuid4().hex
        if include is None:
            include = {}

        # build
        os.makedirs(build_path, exist_ok=True)
        shutil.rmtree(f"{build_path}/app_lambda_layer", ignore_errors=True)
        os.makedirs(f"{build_path}/app_lambda_layer/python")
        requirements_path = f"{build_path}/app_lambda_layer/requirements.txt"
        subprocess.run(["poetry", "export", "-f", "requirements.txt", ">", requirements_path])
        subprocess.run(
            ["pip", "install", "-r", requirements_path, "-t", f"{build_path}/app_lambda_layer/python"])
        for path in include:
            os.makedirs(f"{build_path}/app_lambda_layer/python/{include[path]}")
            shutil.copytree(path, f"{build_path}/app_lambda_layer/python/{include[path]}")

        # optimize
        lambda_included = [
            "boto3",
            "botocore",
            "s3transfer",
        ]
        for module in lambda_included:
            shutil.rmtree(f"{build_path}/app_lambda_layer/python/{module}", ignore_errors=True)

        super().__init__(
            scope,
            construct_id,
            code=lambda_.Code.from_asset(f"{build_path}/app_lambda_layer"),
            **kwargs,
        )
