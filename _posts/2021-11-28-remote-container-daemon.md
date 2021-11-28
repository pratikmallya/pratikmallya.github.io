---
layout: post
title: "Remote Container Daemon"
description: ""
tags: ["podman", "container", "docker", "projects"]
---

Personal projects for me serve several purposes. They can be an effective learning tool, a good way to explore a new 
tool or technology. Often its about solving a problem in a *more* convoluted way than the optimized one, just to 
explore the problem space better and to see what all you can do with it. 


Most projects/ideas don't really see the light of day, so I wanted to try an experiment where I wrote about an 
incomplete one, one where I failed to get the result I wanted, but wrote about how I approached it and how far I could
get. Maybe some day the conditions change and I'm able to look back and finish it.

The basic idea was to have remote container "daemon"; essentially something that would allow us to build container 
images from anywhere. Usually, you install docker for desktop on mac, and then `docker build`. However, docker is a 
resource hungry application; having it run on a beefy work Macbook Pro is fine, but on my lean personal Macbook Air?
Not so much.

The first improvement is just to use `podman`. It removes the need to have a daemon... making this whole project 
somewhat useless. However, to use `podman` on macos requires spinning up a linux vm (which `podman machine` does) 
because the underlying technology used by containers (cgroups?) is only available on linux.

OK, so now the problem has changed from running a docker daemon somewhere, to simply having a linux instance with 
`podman` installed accessible from my machine. That seems like a much simpler problem.

### Appendix: Using podman on MacOS

1. `brew install podman`
2. `podman machine init`, downloads a fcos vm image
3. `podman machine start`, starts the linux vm

Now, just substitute `podman` for `docker` and it just works! (There are almost certainly cases where a simple 
substitution won't work... but for the purposes of building and running container images locally, it looks like 
`podman` just works).


While the linux vm spawned by `podman machine start` does consume a bunch of RAM, it does not eat CPU like the docker
daemon (TODO: verify this, compare resource usage b/w podman and docker daemon).