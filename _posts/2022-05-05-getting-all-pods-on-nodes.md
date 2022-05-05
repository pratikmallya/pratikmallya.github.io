---
layout: post
title: "Get all pods running on kubernetes nodes"
description: "How to get all pods running on kubernetes nodes"
tags: ["kubernetes", "unix"]
---

A common question when working with kubernetes is to get all the pods running on a certain set of nodes. Lets see if its possible to come up with an idiomatic way to do this.

The nodes are often obtained by using labels, such as:

```
$ kubectl get no -lLABEL=VALUE
NAME                           STATUS   ROLES   AGE   VERSION
ip-10-42-80-248.ec2.internal   Ready    node    34d   v1.16.15
ip-10-42-87-138.ec2.internal   Ready    node    29d   v1.16.15
ip-10-42-87-58.ec2.internal    Ready    node    42d   v1.16.15
```
A useful flag is `--no-headers` which will remove the table header:

```
$ kubectl get no -lLABEL=VALUE --no-headers
ip-10-42-80-248.ec2.internal   Ready   node   34d   v1.16.15
ip-10-42-87-138.ec2.internal   Ready   node   29d   v1.16.15
ip-10-42-87-58.ec2.internal    Ready   node   42d   v1.16.15
```
with a little bit of `awk`, we can get just the node names:

```
$ kubectl get no -lLABEL=VALUE --no-headers | awk '{print $1}'
ip-10-42-80-248.ec2.internal
ip-10-42-87-138.ec2.internal
ip-10-42-87-58.ec2.internal
```
we can pipe this into another `kubectl` command to get the pods! To do this, we can use xargs with its handy `-I` flag, that lets us pass data piped through in a specific position in the command.

```
$ kubectl get no -lLABEL=VALUE --no-headers | awk '{print $1}' | \
    xargs -I % kubectl get po -A --field-selector spec.nodeName=% --no-headers
kube-system    kiam-agent-8xpjr      1/1   Running   0     2d13h
kube-system    npd-v0.7.1-gd8jt      1/1   Running   0     2d13h
monitoring     node-exporter-8j5mx   1/1   Running   0     2d13h
kube-system     kiam-agent-q2xgj                 1/1   Running   0     32h
kube-system     npd-v0.7.1-4l6rk                 1/1   Running   0     32h
monitoring      node-exporter-8znlh              1/1   Running   0     32h
```
In this command the `-I %` instructs `xargs` to substitute `%` for whatever comes in through the pipe, which in this case are the node names, which are then substituted at the right place in the `kubectl` command.

Nice! While we've got all the pods, its kind of ugly and difficult to read. There are 2 problems:

* the columns are not aligned
* its not sorted

To fix the column alignment, we can use the `column` command with the `-t` option:

```
$ kubectl get no -lLABEL=VALUE --no-headers | awk '{print $1}' | \
    xargs -I % kubectl get po -A --field-selector spec.nodeName=% --no-headers | column -t
kube-system    kiam-agent-8s72h     1/1  Running  0  2d14h
kube-system    npd-v0.7.1-hx9lc     1/1  Running  0  2d14h
monitoring     node-exporter-rbs6k  1/1  Running  0  2d14h
kube-system    kiam-agent-dr9jq     1/1  Running  0  2d14h
kube-system    npd-v0.7.1-vzjsj     1/1  Running  0  2d14h
monitoring     node-exporter-5pwzq  1/1  Running  0  2d14h
```
🎉
Now, we just need to sort it, and we can use the `sort` command:
```
$ kubectl get no -lLABEL=VALUE --no-headers | awk '{print $1}' | \
    xargs -I % kubectl get po -A --field-selector spec.nodeName=% --no-headers | column -t | sort
kube-system    kiam-agent-8s72h     1/1  Running  0  2d14h
kube-system    kiam-agent-dr9jq     1/1  Running  0  2d14h
kube-system    npd-v0.7.1-hx9lc     1/1  Running  0  2d14h
kube-system    npd-v0.7.1-vzjsj     1/1  Running  0  2d14h
monitoring     node-exporter-5pwzq  1/1  Running  0  2d14h
monitoring     node-exporter-rbs6k  1/1  Running  0  2d14h
```
Yay! We solved both the issues. Now we've got a similar output as a `kubectl get po` but for multiple nodes.

There is one more optimization to make. By default, `xargs` will run through each input sequentially, which can get really slow if we have a lot of nodes. To make it go faster, we can use the `-P` option for `xargs`, set to `0`, so it uses the max parallelism that a machine is capable of.

So our final command would look something like:

```
$ kubectl get no -lLABEL=VALUE --no-headers | awk '{print $1}' | \
    xargs -P0 -I % kubectl get po -A --field-selector spec.nodeName=% --no-headers | column -t | sort
```

And that's it!
