'''
# cdkeks

Higher-level hybrid cdk|cdk8s construct to build an eks kubernetes platform with batteries included:

* Network policies with [aws-calico](https://github.com/aws/eks-charts/tree/master/stable/aws-calico)
* DNS management with [external-dns](https://github.com/kubernetes-sigs/external-dns)
* Forwarding logs to CloudWatch Logs or ElasticSearch with [fluent-bit](https://github.com/aws/aws-for-fluent-bit)
* Ingress management with the [aws load balancer controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller)

:warning: This is experimental and subject to breaking changes.

## Install

TypeScript/JavaScript:

```bash
npm install --save cdkeks
```

Python:

```bash
pip install cdkeks
```

## Howto use

### Install Addons

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
platform = Platform(self, "Platform",
    cluster=cluster,
    addons=[AwsCalicoAddon(), AwsLoadBalancerControllerAddon()]
)
```

See more [addons](https://github.com/hupe1980/cdkeks/tree/main/cdkeks/src/addons).

### AlbIngress

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
deployment = Deployment(self, "Deployment",
    platform=platform,
    containers=[{
        "image": "nginx"
    }
    ]
)

backend = IngressBackend.from_service(deployment.expose("Service", 80))

ingress = AlbIngress(self, "Ingress",
    platform=platform,
    target_type=TargetType.IP,
    internet_facing=True
)

ingress.connections.allow_from_any_ipv4(Port.tcp(80))
ingress.add_rule("/", backend)
```

### LoadBalancer

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
deployment = Deployment(self, "Deployment",
    platform=platform,
    containers=[{
        "image": "nginx"
    }
    ]
)

deployment.expose("LoadBalancer", 80,
    service_type=ServiceType.LOAD_BALANCER
)
```

## API Reference

See [API.md](https://github.com/hupe1980/cdkeks/tree/master/cdkeks/API.md).

## Example

See more complete [examples](https://github.com/hupe1980/cdkeks/tree/main/examples).

## License

[MIT](https://github.com/hupe1980/cdkeks/tree/main/cdkeks/LICENSE)
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

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_ec2
import aws_cdk.aws_eks
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.core
import cdk8s
import cdk8s_plus_17
import constructs


@jsii.data_type(
    jsii_type="cdkeks.AwsCalicoProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class AwsCalicoProps:
    def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
        '''
        :param version: Default: ``0.3.5``
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :default: ``0.3.5``
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCalicoProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkeks.AwsLoadBalancerControllerAddonProps",
    jsii_struct_bases=[],
    name_mapping={"namespace_name": "namespaceName", "version": "version"},
)
class AwsLoadBalancerControllerAddonProps:
    def __init__(
        self,
        *,
        namespace_name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace_name: Default: ``kube-system``
        :param version: Default: ``1.2.0``
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if namespace_name is not None:
            self._values["namespace_name"] = namespace_name
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def namespace_name(self) -> typing.Optional[builtins.str]:
        '''
        :default: ``kube-system``
        '''
        result = self._values.get("namespace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :default: ``1.2.0``
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsLoadBalancerControllerAddonProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdkeks.BackendProtocol")
class BackendProtocol(enum.Enum):
    HTTPS = "HTTPS"
    HTTP = "HTTP"
    TCP = "TCP"
    SSL = "SSL"


class Cdk8sConstruct(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdkeks.Cdk8sConstruct",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        platform: "Platform",
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param platform: -
        :param metadata: -
        '''
        props = Cdk8sConstructProps(platform=platform, metadata=metadata)

        jsii.create(Cdk8sConstruct, self, [scope, id, props])

    @jsii.member(jsii_name="onPrepare")
    def _on_prepare(self) -> None:
        '''Perform final modifications before synthesis.

        This method can be implemented by derived constructs in order to perform
        final changes before synthesis. prepare() will be called after child
        constructs have been prepared.

        This is an advanced framework feature. Only use this if you
        understand the implications.
        '''
        return typing.cast(None, jsii.invoke(self, "onPrepare", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="chart")
    def _chart(self) -> cdk8s.Chart:
        return typing.cast(cdk8s.Chart, jsii.get(self, "chart"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metadata")
    @abc.abstractmethod
    def metadata(self) -> cdk8s.ApiObjectMetadataDefinition:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="platform")
    def _platform(self) -> "Platform":
        return typing.cast("Platform", jsii.get(self, "platform"))


class _Cdk8sConstructProxy(Cdk8sConstruct):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> cdk8s.ApiObjectMetadataDefinition:
        return typing.cast(cdk8s.ApiObjectMetadataDefinition, jsii.get(self, "metadata"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Cdk8sConstruct).__jsii_proxy_class__ = lambda : _Cdk8sConstructProxy


@jsii.data_type(
    jsii_type="cdkeks.Cdk8sConstructProps",
    jsii_struct_bases=[],
    name_mapping={"platform": "platform", "metadata": "metadata"},
)
class Cdk8sConstructProps:
    def __init__(
        self,
        *,
        platform: "Platform",
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''
        :param platform: -
        :param metadata: -
        '''
        if isinstance(metadata, dict):
            metadata = cdk8s.ApiObjectMetadata(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "platform": platform,
        }
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def platform(self) -> "Platform":
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast("Platform", result)

    @builtins.property
    def metadata(self) -> typing.Optional[cdk8s.ApiObjectMetadata]:
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[cdk8s.ApiObjectMetadata], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cdk8sConstructProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Deployment(
    Cdk8sConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdkeks.Deployment",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        containers: typing.Optional[typing.Sequence[cdk8s_plus_17.ContainerProps]] = None,
        service_account: typing.Optional[aws_cdk.aws_eks.ServiceAccount] = None,
        platform: "Platform",
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param containers: -
        :param service_account: -
        :param platform: -
        :param metadata: -
        '''
        props = DeploymentProps(
            containers=containers,
            service_account=service_account,
            platform=platform,
            metadata=metadata,
        )

        jsii.create(Deployment, self, [scope, id, props])

    @jsii.member(jsii_name="expose")
    def expose(
        self,
        id: builtins.str,
        port: jsii.Number,
        *,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[cdk8s_plus_17.Protocol] = None,
        service_type: typing.Optional[cdk8s_plus_17.ServiceType] = None,
        target_port: typing.Optional[jsii.Number] = None,
    ) -> "Service":
        '''
        :param id: -
        :param port: -
        :param name: The name of the service to expose. This will be set on the Service.metadata and must be a DNS_LABEL Default: undefined Uses the system generated name.
        :param protocol: The IP protocol for this port. Supports "TCP", "UDP", and "SCTP". Default is TCP. Default: Protocol.TCP
        :param service_type: The type of the exposed service. Default: - ClusterIP.
        :param target_port: The port number the service will redirect to. Default: - The port of the first container in the deployment (ie. containers[0].port)
        '''
        options = cdk8s_plus_17.ExposeOptions(
            name=name,
            protocol=protocol,
            service_type=service_type,
            target_port=target_port,
        )

        return typing.cast("Service", jsii.invoke(self, "expose", [id, port, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiObject")
    def api_object(self) -> cdk8s_plus_17.Deployment:
        return typing.cast(cdk8s_plus_17.Deployment, jsii.get(self, "apiObject"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="containers")
    def containers(self) -> typing.List[cdk8s_plus_17.Container]:
        return typing.cast(typing.List[cdk8s_plus_17.Container], jsii.get(self, "containers"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="labelSelector")
    def label_selector(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labelSelector"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> cdk8s.ApiObjectMetadataDefinition:
        return typing.cast(cdk8s.ApiObjectMetadataDefinition, jsii.get(self, "metadata"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdkeks.DeploymentProps",
    jsii_struct_bases=[Cdk8sConstructProps],
    name_mapping={
        "platform": "platform",
        "metadata": "metadata",
        "containers": "containers",
        "service_account": "serviceAccount",
    },
)
class DeploymentProps(Cdk8sConstructProps):
    def __init__(
        self,
        *,
        platform: "Platform",
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
        containers: typing.Optional[typing.Sequence[cdk8s_plus_17.ContainerProps]] = None,
        service_account: typing.Optional[aws_cdk.aws_eks.ServiceAccount] = None,
    ) -> None:
        '''
        :param platform: -
        :param metadata: -
        :param containers: -
        :param service_account: -
        '''
        if isinstance(metadata, dict):
            metadata = cdk8s.ApiObjectMetadata(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "platform": platform,
        }
        if metadata is not None:
            self._values["metadata"] = metadata
        if containers is not None:
            self._values["containers"] = containers
        if service_account is not None:
            self._values["service_account"] = service_account

    @builtins.property
    def platform(self) -> "Platform":
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast("Platform", result)

    @builtins.property
    def metadata(self) -> typing.Optional[cdk8s.ApiObjectMetadata]:
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[cdk8s.ApiObjectMetadata], result)

    @builtins.property
    def containers(self) -> typing.Optional[typing.List[cdk8s_plus_17.ContainerProps]]:
        result = self._values.get("containers")
        return typing.cast(typing.Optional[typing.List[cdk8s_plus_17.ContainerProps]], result)

    @builtins.property
    def service_account(self) -> typing.Optional[aws_cdk.aws_eks.ServiceAccount]:
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.ServiceAccount], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdkeks.IAddon")
class IAddon(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        ...

    @jsii.member(jsii_name="install")
    def install(self, scope: constructs.Construct, platform: "Platform") -> None:
        '''
        :param scope: -
        :param platform: -
        '''
        ...


class _IAddonProxy:
    __jsii_type__: typing.ClassVar[str] = "cdkeks.IAddon"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @jsii.member(jsii_name="install")
    def install(self, scope: constructs.Construct, platform: "Platform") -> None:
        '''
        :param scope: -
        :param platform: -
        '''
        return typing.cast(None, jsii.invoke(self, "install", [scope, platform]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAddon).__jsii_proxy_class__ = lambda : _IAddonProxy


@jsii.interface(jsii_type="cdkeks.INamespace")
class INamespace(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        ...


class _INamespaceProxy:
    __jsii_type__: typing.ClassVar[str] = "cdkeks.INamespace"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INamespace).__jsii_proxy_class__ = lambda : _INamespaceProxy


class IngressBackend(metaclass=jsii.JSIIMeta, jsii_type="cdkeks.IngressBackend"):
    def __init__(self) -> None:
        jsii.create(IngressBackend, self, [])

    @jsii.member(jsii_name="fromService") # type: ignore[misc]
    @builtins.classmethod
    def from_service(
        cls,
        service: "Service",
        *,
        port: typing.Optional[jsii.Number] = None,
    ) -> cdk8s_plus_17.IngressV1Beta1Backend:
        '''
        :param service: -
        :param port: The port to use to access the service. - This option will fail if the service does not expose any ports. - If the service exposes multiple ports, this option must be specified. - If the service exposes a single port, this option is optional and if specified, it must be the same port exposed by the service. Default: - if the service exposes a single port, this port will be used.
        '''
        options = cdk8s_plus_17.ServiceIngressV1BetaBackendOptions(port=port)

        return typing.cast(cdk8s_plus_17.IngressV1Beta1Backend, jsii.sinvoke(cls, "fromService", [service, options]))


@jsii.data_type(
    jsii_type="cdkeks.LoadBalancerProps",
    jsii_struct_bases=[Cdk8sConstructProps],
    name_mapping={
        "platform": "platform",
        "metadata": "metadata",
        "internal": "internal",
        "backend_protocal": "backendProtocal",
        "certificate": "certificate",
        "ssl_policy": "sslPolicy",
    },
)
class LoadBalancerProps(Cdk8sConstructProps):
    def __init__(
        self,
        *,
        platform: "Platform",
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
        internal: builtins.bool,
        backend_protocal: typing.Optional[BackendProtocol] = None,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        ssl_policy: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.SslPolicy] = None,
    ) -> None:
        '''
        :param platform: -
        :param metadata: -
        :param internal: Default: false
        :param backend_protocal: -
        :param certificate: -
        :param ssl_policy: -
        '''
        if isinstance(metadata, dict):
            metadata = cdk8s.ApiObjectMetadata(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "platform": platform,
            "internal": internal,
        }
        if metadata is not None:
            self._values["metadata"] = metadata
        if backend_protocal is not None:
            self._values["backend_protocal"] = backend_protocal
        if certificate is not None:
            self._values["certificate"] = certificate
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def platform(self) -> "Platform":
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast("Platform", result)

    @builtins.property
    def metadata(self) -> typing.Optional[cdk8s.ApiObjectMetadata]:
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[cdk8s.ApiObjectMetadata], result)

    @builtins.property
    def internal(self) -> builtins.bool:
        '''
        :default: false
        '''
        result = self._values.get("internal")
        assert result is not None, "Required property 'internal' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def backend_protocal(self) -> typing.Optional[BackendProtocol]:
        result = self._values.get("backend_protocal")
        return typing.cast(typing.Optional[BackendProtocol], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[aws_cdk.aws_certificatemanager.ICertificate], result)

    @builtins.property
    def ssl_policy(
        self,
    ) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.SslPolicy]:
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[aws_cdk.aws_elasticloadbalancingv2.SslPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INamespace)
class Namespace(Cdk8sConstruct, metaclass=jsii.JSIIMeta, jsii_type="cdkeks.Namespace"):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        platform: "Platform",
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param platform: -
        :param metadata: -
        '''
        props = Cdk8sConstructProps(platform=platform, metadata=metadata)

        jsii.create(Namespace, self, [scope, id, props])

    @jsii.member(jsii_name="fromNamespaceName") # type: ignore[misc]
    @builtins.classmethod
    def from_namespace_name(cls, name: builtins.str) -> INamespace:
        '''
        :param name: -
        '''
        return typing.cast(INamespace, jsii.sinvoke(cls, "fromNamespaceName", [name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiObject")
    def api_object(self) -> "Namespace":
        return typing.cast("Namespace", jsii.get(self, "apiObject"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> cdk8s.ApiObjectMetadataDefinition:
        return typing.cast(cdk8s.ApiObjectMetadataDefinition, jsii.get(self, "metadata"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdkeks.NetworkLoadBalancerProps",
    jsii_struct_bases=[Cdk8sConstructProps],
    name_mapping={
        "platform": "platform",
        "metadata": "metadata",
        "internal": "internal",
    },
)
class NetworkLoadBalancerProps(Cdk8sConstructProps):
    def __init__(
        self,
        *,
        platform: "Platform",
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
        internal: builtins.bool,
    ) -> None:
        '''
        :param platform: -
        :param metadata: -
        :param internal: Default: false
        '''
        if isinstance(metadata, dict):
            metadata = cdk8s.ApiObjectMetadata(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "platform": platform,
            "internal": internal,
        }
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def platform(self) -> "Platform":
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast("Platform", result)

    @builtins.property
    def metadata(self) -> typing.Optional[cdk8s.ApiObjectMetadata]:
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[cdk8s.ApiObjectMetadata], result)

    @builtins.property
    def internal(self) -> builtins.bool:
        '''
        :default: false
        '''
        result = self._values.get("internal")
        assert result is not None, "Required property 'internal' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAddon)
class NginxIngressAddon(metaclass=jsii.JSIIMeta, jsii_type="cdkeks.NginxIngressAddon"):
    def __init__(
        self,
        *,
        namespace_name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace_name: Default: ``nginx-ingress``
        :param version: Default: ``3.6.6``
        '''
        props = NginxIngressAddonProps(namespace_name=namespace_name, version=version)

        jsii.create(NginxIngressAddon, self, [props])

    @jsii.member(jsii_name="install")
    def install(self, scope: constructs.Construct, platform: "Platform") -> None:
        '''
        :param scope: -
        :param platform: -
        '''
        return typing.cast(None, jsii.invoke(self, "install", [scope, platform]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="NAME")
    def NAME(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdkeks.NginxIngressAddonProps",
    jsii_struct_bases=[],
    name_mapping={"namespace_name": "namespaceName", "version": "version"},
)
class NginxIngressAddonProps:
    def __init__(
        self,
        *,
        namespace_name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace_name: Default: ``nginx-ingress``
        :param version: Default: ``3.6.6``
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if namespace_name is not None:
            self._values["namespace_name"] = namespace_name
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def namespace_name(self) -> typing.Optional[builtins.str]:
        '''
        :default: ``nginx-ingress``
        '''
        result = self._values.get("namespace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :default: ``3.6.6``
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NginxIngressAddonProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Platform(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdkeks.Platform",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.ICluster,
        addons: typing.Optional[typing.Sequence[IAddon]] = None,
        strict: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: -
        :param addons: -
        :param strict: Default: false;
        '''
        props = PlatformProps(cluster=cluster, addons=addons, strict=strict)

        jsii.create(Platform, self, [scope, id, props])

    @jsii.member(jsii_name="addAddon")
    def add_addon(self, addon: IAddon) -> None:
        '''
        :param addon: -
        '''
        return typing.cast(None, jsii.invoke(self, "addAddon", [addon]))

    @jsii.member(jsii_name="addCdk8sChart")
    def add_cdk8s_chart(
        self,
        id: builtins.str,
        chart: constructs.Construct,
    ) -> aws_cdk.aws_eks.KubernetesManifest:
        '''
        :param id: -
        :param chart: -
        '''
        return typing.cast(aws_cdk.aws_eks.KubernetesManifest, jsii.invoke(self, "addCdk8sChart", [id, chart]))

    @jsii.member(jsii_name="addHelmChart")
    def add_helm_chart(
        self,
        id: builtins.str,
        *,
        chart: builtins.str,
        create_namespace: typing.Optional[builtins.bool] = None,
        namespace: typing.Optional[builtins.str] = None,
        release: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        version: typing.Optional[builtins.str] = None,
        wait: typing.Optional[builtins.bool] = None,
    ) -> aws_cdk.aws_eks.HelmChart:
        '''
        :param id: -
        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful
        '''
        options = aws_cdk.aws_eks.HelmChartOptions(
            chart=chart,
            create_namespace=create_namespace,
            namespace=namespace,
            release=release,
            repository=repository,
            timeout=timeout,
            values=values,
            version=version,
            wait=wait,
        )

        return typing.cast(aws_cdk.aws_eks.HelmChart, jsii.invoke(self, "addHelmChart", [id, options]))

    @jsii.member(jsii_name="addManifest")
    def add_manifest(
        self,
        id: builtins.str,
        *manifest: typing.Mapping[builtins.str, typing.Any],
    ) -> aws_cdk.aws_eks.KubernetesManifest:
        '''
        :param id: -
        :param manifest: -
        '''
        return typing.cast(aws_cdk.aws_eks.KubernetesManifest, jsii.invoke(self, "addManifest", [id, *manifest]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        return typing.cast(aws_cdk.aws_eks.ICluster, jsii.get(self, "cluster"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="strict")
    def strict(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "strict"))


@jsii.data_type(
    jsii_type="cdkeks.PlatformProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster", "addons": "addons", "strict": "strict"},
)
class PlatformProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_eks.ICluster,
        addons: typing.Optional[typing.Sequence[IAddon]] = None,
        strict: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param cluster: -
        :param addons: -
        :param strict: Default: false;
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }
        if addons is not None:
            self._values["addons"] = addons
        if strict is not None:
            self._values["strict"] = strict

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.ICluster, result)

    @builtins.property
    def addons(self) -> typing.Optional[typing.List[IAddon]]:
        result = self._values.get("addons")
        return typing.cast(typing.Optional[typing.List[IAddon]], result)

    @builtins.property
    def strict(self) -> typing.Optional[builtins.bool]:
        '''
        :default: false;
        '''
        result = self._values.get("strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlatformProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Service(Cdk8sConstruct, metaclass=jsii.JSIIMeta, jsii_type="cdkeks.Service"):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        ports: typing.Optional[typing.Sequence[cdk8s_plus_17.ServicePort]] = None,
        type: typing.Optional["ServiceType"] = None,
        platform: Platform,
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ports: -
        :param type: Default: ServiceType.CLUSTER_IP
        :param platform: -
        :param metadata: -
        '''
        props = ServiceProps(
            ports=ports, type=type, platform=platform, metadata=metadata
        )

        jsii.create(Service, self, [scope, id, props])

    @jsii.member(jsii_name="addDeployment")
    def add_deployment(
        self,
        deployment: Deployment,
        port: jsii.Number,
        *,
        name: typing.Optional[builtins.str] = None,
        node_port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[cdk8s_plus_17.Protocol] = None,
        target_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param deployment: -
        :param port: -
        :param name: The name of this port within the service. This must be a DNS_LABEL. All ports within a ServiceSpec must have unique names. This maps to the 'Name' field in EndpointPort objects. Optional if only one ServicePort is defined on this service.
        :param node_port: The port on each node on which this service is exposed when type=NodePort or LoadBalancer. Usually assigned by the system. If specified, it will be allocated to the service if unused or else creation of the service will fail. Default is to auto-allocate a port if the ServiceType of this Service requires one. Default: to auto-allocate a port if the ServiceType of this Service requires one.
        :param protocol: The IP protocol for this port. Supports "TCP", "UDP", and "SCTP". Default is TCP. Default: Protocol.TCP
        :param target_port: The port number the service will redirect to. Default: - The value of ``port`` will be used.
        '''
        options = cdk8s_plus_17.ServicePortOptions(
            name=name, node_port=node_port, protocol=protocol, target_port=target_port
        )

        return typing.cast(None, jsii.invoke(self, "addDeployment", [deployment, port, options]))

    @jsii.member(jsii_name="addSelector")
    def add_selector(self, label: builtins.str, value: builtins.str) -> None:
        '''
        :param label: -
        :param value: -
        '''
        return typing.cast(None, jsii.invoke(self, "addSelector", [label, value]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiObject")
    def api_object(self) -> cdk8s_plus_17.Service:
        return typing.cast(cdk8s_plus_17.Service, jsii.get(self, "apiObject"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> cdk8s.ApiObjectMetadataDefinition:
        return typing.cast(cdk8s.ApiObjectMetadataDefinition, jsii.get(self, "metadata"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[cdk8s_plus_17.ServicePort]:
        return typing.cast(typing.List[cdk8s_plus_17.ServicePort], jsii.get(self, "ports"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="selector")
    def selector(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "selector"))


@jsii.implements(aws_cdk.aws_iam.IPrincipal)
class ServiceAccount(
    Cdk8sConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdkeks.ServiceAccount",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        secrets: typing.Optional[typing.Sequence[cdk8s_plus_17.ISecret]] = None,
        platform: Platform,
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param secrets: -
        :param platform: -
        :param metadata: -
        '''
        props = ServiceAccountProps(
            secrets=secrets, platform=platform, metadata=metadata
        )

        jsii.create(ServiceAccount, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> builtins.bool:
        '''(deprecated) (deprecated) Add to the policy of this principal.

        :param statement: -

        :deprecated: use ``addToPrincipalPolicy()``

        :stability: deprecated
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToPrincipalPolicyResult:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        return typing.cast(aws_cdk.aws_iam.AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiObject")
    def api_object(self) -> cdk8s_plus_17.ServiceAccount:
        return typing.cast(cdk8s_plus_17.ServiceAccount, jsii.get(self, "apiObject"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(aws_cdk.aws_iam.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> cdk8s.ApiObjectMetadataDefinition:
        return typing.cast(cdk8s.ApiObjectMetadataDefinition, jsii.get(self, "metadata"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> aws_cdk.aws_iam.PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(aws_cdk.aws_iam.PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="cdkeks.ServiceAccountProps",
    jsii_struct_bases=[Cdk8sConstructProps],
    name_mapping={
        "platform": "platform",
        "metadata": "metadata",
        "secrets": "secrets",
    },
)
class ServiceAccountProps(Cdk8sConstructProps):
    def __init__(
        self,
        *,
        platform: Platform,
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
        secrets: typing.Optional[typing.Sequence[cdk8s_plus_17.ISecret]] = None,
    ) -> None:
        '''
        :param platform: -
        :param metadata: -
        :param secrets: -
        '''
        if isinstance(metadata, dict):
            metadata = cdk8s.ApiObjectMetadata(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "platform": platform,
        }
        if metadata is not None:
            self._values["metadata"] = metadata
        if secrets is not None:
            self._values["secrets"] = secrets

    @builtins.property
    def platform(self) -> Platform:
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(Platform, result)

    @builtins.property
    def metadata(self) -> typing.Optional[cdk8s.ApiObjectMetadata]:
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[cdk8s.ApiObjectMetadata], result)

    @builtins.property
    def secrets(self) -> typing.Optional[typing.List[cdk8s_plus_17.ISecret]]:
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.List[cdk8s_plus_17.ISecret]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAccountProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkeks.ServiceProps",
    jsii_struct_bases=[Cdk8sConstructProps],
    name_mapping={
        "platform": "platform",
        "metadata": "metadata",
        "ports": "ports",
        "type": "type",
    },
)
class ServiceProps(Cdk8sConstructProps):
    def __init__(
        self,
        *,
        platform: Platform,
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
        ports: typing.Optional[typing.Sequence[cdk8s_plus_17.ServicePort]] = None,
        type: typing.Optional["ServiceType"] = None,
    ) -> None:
        '''
        :param platform: -
        :param metadata: -
        :param ports: -
        :param type: Default: ServiceType.CLUSTER_IP
        '''
        if isinstance(metadata, dict):
            metadata = cdk8s.ApiObjectMetadata(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "platform": platform,
        }
        if metadata is not None:
            self._values["metadata"] = metadata
        if ports is not None:
            self._values["ports"] = ports
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def platform(self) -> Platform:
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(Platform, result)

    @builtins.property
    def metadata(self) -> typing.Optional[cdk8s.ApiObjectMetadata]:
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[cdk8s.ApiObjectMetadata], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[cdk8s_plus_17.ServicePort]]:
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[cdk8s_plus_17.ServicePort]], result)

    @builtins.property
    def type(self) -> typing.Optional["ServiceType"]:
        '''
        :default: ServiceType.CLUSTER_IP
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["ServiceType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdkeks.ServiceType")
class ServiceType(enum.Enum):
    CLUSTER_IP = "CLUSTER_IP"
    NODE_PORT = "NODE_PORT"
    LOAD_BALANCER = "LOAD_BALANCER"
    EXTERNAL_NAME = "EXTERNAL_NAME"


@jsii.enum(jsii_type="cdkeks.TargetType")
class TargetType(enum.Enum):
    '''How to interpret the load balancing target identifiers.'''

    IP = "IP"
    '''Targets identified by IP address.'''
    INSTANCE = "INSTANCE"
    '''Targets identified by instance ID.'''


@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class AlbIngress(
    Cdk8sConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdkeks.AlbIngress",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        certificates: typing.Optional[typing.Sequence[aws_cdk.aws_certificatemanager.ICertificate]] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        ip_adress_type: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.IpAddressType] = None,
        rules: typing.Optional[typing.Sequence[cdk8s_plus_17.IngressV1Beta1Rule]] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        ssl_policy: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.SslPolicy] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_type: typing.Optional[TargetType] = None,
        platform: Platform,
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param certificates: Certificates to attach.
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param ip_adress_type: The type of IP addresses to use. Only applies to application load balancers. Default: IpAddressType.Ipv4
        :param rules: -
        :param security_group: Security Group to assign to this instance. Default: - create new security group
        :param ssl_policy: Default: SslPolicy.RECOMMENDED
        :param tags: Tags that will be applied to AWS resources created.
        :param target_type: Default: AlbTargetType.INSTANCE
        :param platform: -
        :param metadata: -
        '''
        props = AlbIngressProps(
            certificates=certificates,
            internet_facing=internet_facing,
            ip_adress_type=ip_adress_type,
            rules=rules,
            security_group=security_group,
            ssl_policy=ssl_policy,
            tags=tags,
            target_type=target_type,
            platform=platform,
            metadata=metadata,
        )

        jsii.create(AlbIngress, self, [scope, id, props])

    @jsii.member(jsii_name="addRule")
    def add_rule(
        self,
        path: builtins.str,
        backend: cdk8s_plus_17.IngressV1Beta1Backend,
    ) -> None:
        '''
        :param path: -
        :param backend: -
        '''
        return typing.cast(None, jsii.invoke(self, "addRule", [path, backend]))

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        security_group: aws_cdk.aws_ec2.ISecurityGroup,
    ) -> None:
        '''Add the security group to the instance.

        :param security_group: : The security group to add.
        '''
        return typing.cast(None, jsii.invoke(self, "addSecurityGroup", [security_group]))

    @jsii.member(jsii_name="logAccessLogs")
    def log_access_logs(
        self,
        bucket: aws_cdk.aws_s3.IBucket,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Enable access logging for this load balancer.

        :param bucket: -
        :param prefix: -
        '''
        return typing.cast(None, jsii.invoke(self, "logAccessLogs", [bucket, prefix]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiObject")
    def api_object(self) -> cdk8s_plus_17.IngressV1Beta1:
        return typing.cast(cdk8s_plus_17.IngressV1Beta1, jsii.get(self, "apiObject"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        '''Allows specify security group connections for the instance.'''
        return typing.cast(aws_cdk.aws_ec2.Connections, jsii.get(self, "connections"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> cdk8s.ApiObjectMetadataDefinition:
        return typing.cast(cdk8s.ApiObjectMetadataDefinition, jsii.get(self, "metadata"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdkeks.AlbIngressProps",
    jsii_struct_bases=[Cdk8sConstructProps],
    name_mapping={
        "platform": "platform",
        "metadata": "metadata",
        "certificates": "certificates",
        "internet_facing": "internetFacing",
        "ip_adress_type": "ipAdressType",
        "rules": "rules",
        "security_group": "securityGroup",
        "ssl_policy": "sslPolicy",
        "tags": "tags",
        "target_type": "targetType",
    },
)
class AlbIngressProps(Cdk8sConstructProps):
    def __init__(
        self,
        *,
        platform: Platform,
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
        certificates: typing.Optional[typing.Sequence[aws_cdk.aws_certificatemanager.ICertificate]] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        ip_adress_type: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.IpAddressType] = None,
        rules: typing.Optional[typing.Sequence[cdk8s_plus_17.IngressV1Beta1Rule]] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        ssl_policy: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.SslPolicy] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_type: typing.Optional[TargetType] = None,
    ) -> None:
        '''
        :param platform: -
        :param metadata: -
        :param certificates: Certificates to attach.
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param ip_adress_type: The type of IP addresses to use. Only applies to application load balancers. Default: IpAddressType.Ipv4
        :param rules: -
        :param security_group: Security Group to assign to this instance. Default: - create new security group
        :param ssl_policy: Default: SslPolicy.RECOMMENDED
        :param tags: Tags that will be applied to AWS resources created.
        :param target_type: Default: AlbTargetType.INSTANCE
        '''
        if isinstance(metadata, dict):
            metadata = cdk8s.ApiObjectMetadata(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "platform": platform,
        }
        if metadata is not None:
            self._values["metadata"] = metadata
        if certificates is not None:
            self._values["certificates"] = certificates
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if ip_adress_type is not None:
            self._values["ip_adress_type"] = ip_adress_type
        if rules is not None:
            self._values["rules"] = rules
        if security_group is not None:
            self._values["security_group"] = security_group
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy
        if tags is not None:
            self._values["tags"] = tags
        if target_type is not None:
            self._values["target_type"] = target_type

    @builtins.property
    def platform(self) -> Platform:
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(Platform, result)

    @builtins.property
    def metadata(self) -> typing.Optional[cdk8s.ApiObjectMetadata]:
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[cdk8s.ApiObjectMetadata], result)

    @builtins.property
    def certificates(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_certificatemanager.ICertificate]]:
        '''Certificates to attach.'''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_certificatemanager.ICertificate]], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        '''Whether the load balancer has an internet-routable address.

        :default: false
        '''
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ip_adress_type(
        self,
    ) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.IpAddressType]:
        '''The type of IP addresses to use.

        Only applies to application load balancers.

        :default: IpAddressType.Ipv4
        '''
        result = self._values.get("ip_adress_type")
        return typing.cast(typing.Optional[aws_cdk.aws_elasticloadbalancingv2.IpAddressType], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List[cdk8s_plus_17.IngressV1Beta1Rule]]:
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List[cdk8s_plus_17.IngressV1Beta1Rule]], result)

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        '''Security Group to assign to this instance.

        :default: - create new security group
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.ISecurityGroup], result)

    @builtins.property
    def ssl_policy(
        self,
    ) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.SslPolicy]:
        '''
        :default: SslPolicy.RECOMMENDED
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[aws_cdk.aws_elasticloadbalancingv2.SslPolicy], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags that will be applied to AWS resources created.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target_type(self) -> typing.Optional[TargetType]:
        '''
        :default: AlbTargetType.INSTANCE
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional[TargetType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbIngressProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAddon)
class AwsCalicoAddon(metaclass=jsii.JSIIMeta, jsii_type="cdkeks.AwsCalicoAddon"):
    def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
        '''
        :param version: Default: ``0.3.5``
        '''
        props = AwsCalicoProps(version=version)

        jsii.create(AwsCalicoAddon, self, [props])

    @jsii.member(jsii_name="install")
    def install(self, scope: constructs.Construct, platform: Platform) -> None:
        '''
        :param scope: -
        :param platform: -
        '''
        return typing.cast(None, jsii.invoke(self, "install", [scope, platform]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="NAME")
    def NAME(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.implements(IAddon)
class AwsLoadBalancerControllerAddon(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdkeks.AwsLoadBalancerControllerAddon",
):
    def __init__(
        self,
        *,
        namespace_name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace_name: Default: ``kube-system``
        :param version: Default: ``1.2.0``
        '''
        props = AwsLoadBalancerControllerAddonProps(
            namespace_name=namespace_name, version=version
        )

        jsii.create(AwsLoadBalancerControllerAddon, self, [props])

    @jsii.member(jsii_name="install")
    def install(self, scope: constructs.Construct, platform: Platform) -> None:
        '''
        :param scope: -
        :param platform: -
        '''
        return typing.cast(None, jsii.invoke(self, "install", [scope, platform]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="NAME")
    def NAME(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


class LoadBalancer(Service, metaclass=jsii.JSIIMeta, jsii_type="cdkeks.LoadBalancer"):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        internal: builtins.bool,
        backend_protocal: typing.Optional[BackendProtocol] = None,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        ssl_policy: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.SslPolicy] = None,
        platform: Platform,
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param internal: Default: false
        :param backend_protocal: -
        :param certificate: -
        :param ssl_policy: -
        :param platform: -
        :param metadata: -
        '''
        props = LoadBalancerProps(
            internal=internal,
            backend_protocal=backend_protocal,
            certificate=certificate,
            ssl_policy=ssl_policy,
            platform=platform,
            metadata=metadata,
        )

        jsii.create(LoadBalancer, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))


class NetworkLoadBalancer(
    Service,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdkeks.NetworkLoadBalancer",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        internal: builtins.bool,
        platform: Platform,
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param internal: Default: false
        :param platform: -
        :param metadata: -
        '''
        props = NetworkLoadBalancerProps(
            internal=internal, platform=platform, metadata=metadata
        )

        jsii.create(NetworkLoadBalancer, self, [scope, id, props])


__all__ = [
    "AlbIngress",
    "AlbIngressProps",
    "AwsCalicoAddon",
    "AwsCalicoProps",
    "AwsLoadBalancerControllerAddon",
    "AwsLoadBalancerControllerAddonProps",
    "BackendProtocol",
    "Cdk8sConstruct",
    "Cdk8sConstructProps",
    "Deployment",
    "DeploymentProps",
    "IAddon",
    "INamespace",
    "IngressBackend",
    "LoadBalancer",
    "LoadBalancerProps",
    "Namespace",
    "NetworkLoadBalancer",
    "NetworkLoadBalancerProps",
    "NginxIngressAddon",
    "NginxIngressAddonProps",
    "Platform",
    "PlatformProps",
    "Service",
    "ServiceAccount",
    "ServiceAccountProps",
    "ServiceProps",
    "ServiceType",
    "TargetType",
]

publication.publish()
