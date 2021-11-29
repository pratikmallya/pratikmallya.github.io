---
layout: post
title: "Remote Container Daemon"
description: ""
tags: ["podman", "container", "docker", "projects"]
---

Personal projects for serve several purposes. They can be an effective learning tool, a nice way to explore a new 
technology. Sometimes its just about solving a problem in a *more* convoluted way than the optimized one, just to 
explore the problem space better and to see what all can be done. 

Most such projects don't really see the light of day, so I wanted to try an experiment where I wrote about an 
incomplete one, one where I failed to get the result I wanted, but wrote about how I approached it and how far I could
get. Maybe some day the conditions change and I'm able to look back and finish it.

The basic idea is to have remote container "daemon"; essentially something that would allow me to build container 
images from anywhere. Usually, you install docker for desktop on mac, and then `docker build`. However, docker is a 
resource hungry application; having it run on a beefy work Macbook Pro is fine, but on my lean personal Macbook Air?
Not so much.

The first improvement is to use [podman]. It removes the need to have a daemon... making this whole project 
somewhat useless 😅. However, to use `podman` on macos requires spinning up a linux vm (which `podman machine` does) 
because the underlying technology used by containers (cgroups?) is only available on linux.

So now the problem has changed from running a docker daemon somewhere, to simply having a linux instance with 
`podman` installed accessible from my machine. That seems like a much simpler problem.

[podman]: https://podman.io/
### Searching for Cheap Linux Boxes

Ideally, we can wring a free or really cheap VM from one of the multitudes of cloud providers out there. The first one
to land in my google search dragnet was [OCI], which has an always free tier. You get a pretty wimpy x86 VM or a 
decent arm VM, so of course I went with the arm VM. The "shape configuration" (i.e. specs) looked like:


|Type                    |Value                                |
|------------------------|-------------------------------------|
|OS                      |Oracle-Linux-8.4-aarch64-2021.10.25-0|
|Shape                   |VM.Standard.A1.Flex                  |
|OCPU count              |4                                    |
|Network bandwidth (Gbps)|4                                    |
|Memory (GB)             |24                                   |
|Local disk              |Block storage only                   |

[OCI]: https://www.oracle.com/cloud/free/
### Installing podman
Mostly followed [this article].

OCI lets you specify a [cloud-init] script, so just paste the following lines:

```
sudo yum module enable -y container-tools
sudo yum -y install podman
systemctl --user enable podman.socket
sudo loginctl enable-linger opc
```

(`opc` is the default username selected by OCI)

Easy 😎

However, that ended up not working. I don't know why, and didn't investigate it further. I just ran the commands after
ssh-ing into the machine. 🤷


[cloud-init]: https://cloudinit.readthedocs.io/en/latest/#
[this article]: https://www.redhat.com/sysadmin/podman-clients-macos-windows
### Configure podman to connect to remote machine

```
podman system connection add oci --identity ~/.ssh/id_rsa ssh://192.9.229.238:22/run/user/1000/podman/podman.sock
podman system connection default oci
```
(the user id for opc is 1000, as can be verified with `lslogins`: 

```
[opc@podmand ~]$ lslogins opc
Username:                           opc
UID:                                1000
```
)

I got this far, but was unable to proceed as podman is unable to connect to the remote instance as configured.
Documented this in [here](https://github.com/containers/podman/issues/12432). The repo seems like its actively 
maintained, so I hope to get some pointers. Its written in go, so I could maybe try debugging it... but I've already
spent a lot of time, the excitement has worn off, so I'm calling it done... for now 🙂.
### Appendix: Using podman on MacOS

1. `brew install podman`
2. `podman machine init`, downloads a fcos vm image
3. `podman machine start`, starts the linux vm

Now, just substitute `podman` for `docker` and it just works! (There are almost certainly cases where a simple 
substitution won't work... but for the purposes of building and running container images locally, it looks like 
`podman` just works).


While the linux vm spawned by `podman machine start` does consume a bunch of RAM, it does not eat CPU like the docker
daemon (TODO: verify this, compare resource usage b/w podman and docker daemon).