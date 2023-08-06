# cdkeks

Higher-level cdk construct to build an eks kubernetes platform with batteries included:

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

### Alb ingress

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
