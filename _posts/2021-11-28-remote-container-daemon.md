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

The first improvement is just to use podman. This is where I did stop, since `podman` ended up being pretty easy
to install and use.

What do we need?
1. Something that will let us run podman *somewhere*
2. The remote podman is somehow accessible from my machine

The most straightforward thing to do seems to be to get a cloud linux vm, install `podman` on it, and then... make it
accessible from my machine, but safely. As a first step, use ssh tunneling, but if we want to get really fancy, use 
some sort of authentication and make it publicly available. 


### Appendix: Using podman on MacOS

1. `brew install podman`
2. `podman machine init`, downloads a fcos vm image
3. `podman machine start`, starts the linux vm

Now, just substitute `podman` for `docker` and it just works! (There are almost certainly cases where a simple 
substitution won't work... but for the purposes of building and running container images locally, it looks like 
`podman` just works).


While the linux vm spawned by `podman machine start` does consume a bunch of RAM, it does not eat CPU like the docker
daemon (TODO: verify this, compare resource usage b/w podman and docker daemon).