'''
# Django CDK Construct Library

This is a CDK construct library for deploying Django applications on AWS.

High-level constructs are available for deploying applications with the following AWS compute services:

* ECS (near complete)
* EKS (in progress)
* Lambda (planned)

To use one of the constructs you need to provide:

* A path to the root of your Django project
* The location of the `Dockerfile` used to build your application's image (for EKS and ECS) relative to your Django project's root directory
* The commands used to start the process that run your application:

  * web server process (required)
  * celery (optional)
  * celery beat (optional)
* Options for how to run the application and which additional services your application requires

This project uses the AWS CDK and is written in TypeScript, so the options for each construct are defined by TypeScript Interfaces. See [API.md](/API.md) for automatically-generated documentation on the interfaces for each construct.

The construct library is published both to `npm` and `PyPI`, so you can use it in CDK projects that are written in TypeScript or Python.

## Features

The constructs provides everything you will need for your backend including:

* VPC (Subnets, Security Groups, AZs, NAT Gateway)
* Load Balancer
* ACM Certificates (for TLS)
* Route53 Records
* RDS (postgres)
* ElastiCache (redis)

## Using the constructs

This repository includes sample CDK applications that use the libraries.

### EKS

Here's an example from `src/integ.django-eks.ts`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from ..index import DjangoEks

env = {
    "region": process.env.AWS_DEFAULT_REGION || "us-east-1",
    "account": process.env.AWS_ACCOUNT_ID
}

app = cdk.App()
stack = cdk.Stack(app, "DjangoEks", env=env)

construct = DjangoEks(stack, "Cdk-Sample-Lib",
    image_directory="./test/django-step-by-step/backend",
    web_command=["./scripts/start_prod.sh"
    ]
)

#
# Add tagging for this construct and all child constructs
#
cdk.Tags.of(construct).add("stack", "MyStack")
```

This sample application (and others defined in the `integ.*.ts` files in this repo) can be easily deployed for testing purposes with targets defined in the `Makefile`. To deploy the above application, you can run:

```
npm run build
make deploy-eks
```

Destroy the application with:

```
make destroy-eks
```

This assumes that you have credentials configured in your AWS CLI with sufficient permissions and that you have [bootstrapped your AWS account](https://docs.aws.amazon.com/cdk/latest/guide/bootstrapping.html). You will also need to have docker CLI configured in order for CDK to build images and push them to ECR.

### ECS

The ECS construct uses the `ApplicationLoadBalancedFargateService` construct from `@aws-cdk/aws-ecs-patterns`. This is a powerful abstraction that handles a lot of the networking requirements for the construct.

## Key differences between ECS and EKS constructs

The ECS and EKS constructs aim to do the same thing: deploy containerized applications to AWS.

### Container orchestration

The ECS constructs uses Amazon's proprietary, closed-source container orchestration tool called ECS. The EKS construct uses an [open source distribution of Kubernetes](https://github.com/aws/eks-distro) called Amazon EKS Distro (EKS-D).

### Load Balancer

Another important difference from an infrastructure and Infrastructure as Code (IaC) perspective is the use of Application Load Balancers (ALBs).

> The load balancer distributes incoming application traffic across multiple targets, such as EC2 instances, in multiple Availability Zones.

The ECS and EKS constructs go about provisioning ALBs differently. In the ECS construct, the `ApplicationLoadBalancedFargateService` in the CDK code results in CloudFormation code that requests an application load balancer.

The EKS construct does not directly request an ALB. Instead, it installs the [AWS Load Balancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html), [an open source project](https://github.com/kubernetes-sigs/aws-load-balancer-controller), using a Helm chart. This controller satisfies Kubernetes Ingress resources by provisioning Application Load Balancers. The contruct defines a Kubernetes Ingress object which, when deployed to the EKS cluster, causes the AWS Load Balancer Controller to provision an ALB. You can read more about Kubernetes Controllers [here](https://kubernetes.io/docs/concepts/architecture/controller/#direct-control).

The Ingress object defined in the construct uses [annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) that the controller processes when provisioning the ALB. A list of all supported annotations can be found [here on the AWS Load Balancer Controller website](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.2/guide/ingress/annotations/#annotations)

### Compute

One other important difference between the two constructs is the type of compute used to run the container workloads. The ECS construct uses Fargate, a serverless computer offering from AWS. The EKS construct uses EC2 instances for the worker nodes of the EKS cluster. It is possible to use Fargate with EKS, but AWS currently recommends not using Fargate for sensitive workloads on EKS.

## projen

This project uses [projen](https://github.com/projen/projen).

> projen synthesizes project configuration files such as package.json, tsconfig.json, .gitignore, GitHub Workflows, eslint, jest, etc from a well-typed definition written in JavaScript.

## Development

For development of this library, a sample Django application is included as a git submodule in `test/django-step-by-step`. This Django project is used when deploying the application, and can be replaced with your own project for testing purposes.

## Current Development Efforts

This project is under active development. Here are some of the things that I'm curently working on:

* [x] Deploy sample nginx application to test AWS Load Balancer Controller
* [ ] Pass ACM ARN to Ingress annotation
* [ ] Use Fargate Profile to deploy application on Fargate
* [ ] Configure the rest of the Django application components for the EKS construct (web, celery, RDS, ElastiCache, S3 buckets, permissions)
* [ ] Split constructs into `eks`, `ecs` and `common` directories to keep code DRY
* [ ] Build constructs for each component
* [ ] Consider using managed DB services in production environments and in-cluster services for non-production environments (external services)
* [ ] Configure application secrets.
* [ ] Use secrets manager secrets (boto3) for accessing secrets in products
* [ ] Look into logging and observability tools that can be used in the project (EFK, Jaeger, etc.)
* [ ] Go over this Kubernetes checklist: [https://www.weave.works/blog/production-ready-checklist-kubernetes](https://www.weave.works/blog/production-ready-checklist-kubernetes)
* [ ] Add comments to EKS resources docgen
* [ ] Add snapshot tests and refactor the application
* [ ] Add unit tests
* [ ] Consider using cdk8s or cdk8s+ for manifest declarations
* [ ] User the `dockerImageAssets` construct to define the Django project image to be used in the sample application
* [ ]
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_eks
import aws_cdk.aws_s3
import aws_cdk.core


class DjangoCdk(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="django-cdk.DjangoCdk",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        image_directory: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        use_celery_beat: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        web_command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image_directory: The location of the Dockerfile used to create the main application image. This is also the context used for building the image. TODO: set image and context path separately.
        :param bucket_name: Name of existing bucket to use for media files. This name will be auto-generated if not specified
        :param use_celery_beat: Used to enable the celery beat service. Default: false
        :param vpc: The VPC to use for the application. It must contain PUBLIC, PRIVATE and ISOLATED subnets. A VPC will be created if this is not specified
        :param web_command: The command used to run the API web service.
        '''
        props = DjangoCdkProps(
            image_directory=image_directory,
            bucket_name=bucket_name,
            use_celery_beat=use_celery_beat,
            vpc=vpc,
            web_command=web_command,
        )

        jsii.create(DjangoCdk, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.Cluster:
        return typing.cast(aws_cdk.aws_ecs.Cluster, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: aws_cdk.aws_ecs.Cluster) -> None:
        jsii.set(self, "cluster", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="image")
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        return typing.cast(aws_cdk.aws_ecs.ContainerImage, jsii.get(self, "image"))

    @image.setter
    def image(self, value: aws_cdk.aws_ecs.ContainerImage) -> None:
        jsii.set(self, "image", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="staticFileBucket")
    def static_file_bucket(self) -> aws_cdk.aws_s3.Bucket:
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "staticFileBucket"))

    @static_file_bucket.setter
    def static_file_bucket(self, value: aws_cdk.aws_s3.Bucket) -> None:
        jsii.set(self, "staticFileBucket", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: aws_cdk.aws_ec2.IVpc) -> None:
        jsii.set(self, "vpc", value)


@jsii.data_type(
    jsii_type="django-cdk.DjangoCdkProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_directory": "imageDirectory",
        "bucket_name": "bucketName",
        "use_celery_beat": "useCeleryBeat",
        "vpc": "vpc",
        "web_command": "webCommand",
    },
)
class DjangoCdkProps:
    def __init__(
        self,
        *,
        image_directory: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        use_celery_beat: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        web_command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param image_directory: The location of the Dockerfile used to create the main application image. This is also the context used for building the image. TODO: set image and context path separately.
        :param bucket_name: Name of existing bucket to use for media files. This name will be auto-generated if not specified
        :param use_celery_beat: Used to enable the celery beat service. Default: false
        :param vpc: The VPC to use for the application. It must contain PUBLIC, PRIVATE and ISOLATED subnets. A VPC will be created if this is not specified
        :param web_command: The command used to run the API web service.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "image_directory": image_directory,
        }
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if use_celery_beat is not None:
            self._values["use_celery_beat"] = use_celery_beat
        if vpc is not None:
            self._values["vpc"] = vpc
        if web_command is not None:
            self._values["web_command"] = web_command

    @builtins.property
    def image_directory(self) -> builtins.str:
        '''The location of the Dockerfile used to create the main application image.

        This is also the context used for building the image.

        TODO: set image and context path separately.
        '''
        result = self._values.get("image_directory")
        assert result is not None, "Required property 'image_directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Name of existing bucket to use for media files.

        This name will be auto-generated if not specified
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_celery_beat(self) -> typing.Optional[builtins.bool]:
        '''Used to enable the celery beat service.

        :default: false
        '''
        result = self._values.get("use_celery_beat")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        '''The VPC to use for the application. It must contain PUBLIC, PRIVATE and ISOLATED subnets.

        A VPC will be created if this is not specified
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    @builtins.property
    def web_command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command used to run the API web service.'''
        result = self._values.get("web_command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DjangoCdkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DjangoEks(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="django-cdk.DjangoEks",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        image_directory: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        use_celery_beat: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        web_command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image_directory: The location of the Dockerfile used to create the main application image. This is also the context used for building the image. TODO: set image and context path separately.
        :param bucket_name: Name of existing bucket to use for media files. This name will be auto-generated if not specified
        :param use_celery_beat: Used to enable the celery beat service. Default: false
        :param vpc: The VPC to use for the application. It must contain PUBLIC, PRIVATE and ISOLATED subnets. A VPC will be created if this is not specified
        :param web_command: The command used to run the API web service.
        '''
        props = DjangoEksProps(
            image_directory=image_directory,
            bucket_name=bucket_name,
            use_celery_beat=use_celery_beat,
            vpc=vpc,
            web_command=web_command,
        )

        jsii.create(DjangoEks, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        return typing.cast(aws_cdk.aws_eks.Cluster, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: aws_cdk.aws_eks.Cluster) -> None:
        jsii.set(self, "cluster", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="staticFileBucket")
    def static_file_bucket(self) -> aws_cdk.aws_s3.Bucket:
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "staticFileBucket"))

    @static_file_bucket.setter
    def static_file_bucket(self, value: aws_cdk.aws_s3.Bucket) -> None:
        jsii.set(self, "staticFileBucket", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: aws_cdk.aws_ec2.IVpc) -> None:
        jsii.set(self, "vpc", value)


@jsii.data_type(
    jsii_type="django-cdk.DjangoEksProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_directory": "imageDirectory",
        "bucket_name": "bucketName",
        "use_celery_beat": "useCeleryBeat",
        "vpc": "vpc",
        "web_command": "webCommand",
    },
)
class DjangoEksProps:
    def __init__(
        self,
        *,
        image_directory: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        use_celery_beat: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        web_command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param image_directory: The location of the Dockerfile used to create the main application image. This is also the context used for building the image. TODO: set image and context path separately.
        :param bucket_name: Name of existing bucket to use for media files. This name will be auto-generated if not specified
        :param use_celery_beat: Used to enable the celery beat service. Default: false
        :param vpc: The VPC to use for the application. It must contain PUBLIC, PRIVATE and ISOLATED subnets. A VPC will be created if this is not specified
        :param web_command: The command used to run the API web service.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "image_directory": image_directory,
        }
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if use_celery_beat is not None:
            self._values["use_celery_beat"] = use_celery_beat
        if vpc is not None:
            self._values["vpc"] = vpc
        if web_command is not None:
            self._values["web_command"] = web_command

    @builtins.property
    def image_directory(self) -> builtins.str:
        '''The location of the Dockerfile used to create the main application image.

        This is also the context used for building the image.

        TODO: set image and context path separately.
        '''
        result = self._values.get("image_directory")
        assert result is not None, "Required property 'image_directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Name of existing bucket to use for media files.

        This name will be auto-generated if not specified
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_celery_beat(self) -> typing.Optional[builtins.bool]:
        '''Used to enable the celery beat service.

        :default: false
        '''
        result = self._values.get("use_celery_beat")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        '''The VPC to use for the application. It must contain PUBLIC, PRIVATE and ISOLATED subnets.

        A VPC will be created if this is not specified
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    @builtins.property
    def web_command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command used to run the API web service.'''
        result = self._values.get("web_command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DjangoEksProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DjangoCdk",
    "DjangoCdkProps",
    "DjangoEks",
    "DjangoEksProps",
]

publication.publish()
