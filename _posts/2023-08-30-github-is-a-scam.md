---
layout: post
title: "Github Is a Scam"
description: "Why not to use Github"
tags: ["Github", "Gitops", "CI/CD"]
---

Or at least don't use it for your business.

Or at least don't depend on it to build your deployment pipeline.

Its the end of August, and Github has had _17 incidents_ this month:

![Github Incidents on August (from https://www.githubstatus.com/history)](/assets/images/github_status_august.png)

If you use Github actions for your deployment pipeline, what do you do when you want to make an emergency deploy
and there is an outage? You curse a lot and wait around impatiently.

Is there a better way?

When I joined Github back in 2011, it was a place to host and find cool OSS repos. Pull requests weren't that great
to review code (credit where its due: that's improved greatly)
Today its a multi-billion dollar subdivision of a MegaCorp. At some point along the way from 2011 to now, they
bamboozled developers into building their entire software lifecycle pipeline within the system. Perhaps its time 
to step back.

Github still has a place in the software development lifecycle. Using it to host code and as a mechanism for 
reviewing and updating the code base is ok. But we should reconsider what happens after that merge is made.

Generally, today the application binaries are packaged as container images, and application configurations as yaml. So
its shouldn't be that hard to build some platform agnostic, reliable tool that takes those artifacts and pushes them
to differnt deployment environments. At the very least, we should think about break glass mechanisms for when Github
is having incidents, like the [UK Government](https://docs.publishing.service.gov.uk/manual/github-unavailable.html).