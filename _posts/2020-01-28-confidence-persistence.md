---
layout: post
title: "Iterating at the speed of cloud"
description: "setting up things in cloud = fasht"
tags: ["craft", "build", "cloud"]
---

Perhaps, the biggest benefit that a stable cloud provider gives you is the 
ability to rapidly spin up internet facing applications. I don't suppose when 
developers worked out of systems hosted in datacenters, that they could spin
up internet facing applications in their work systems, which are usually 
tightly controlled by a very conservative operations team and a well intentioned
but annoying security team.

In the cloud, resources are namespaced and isolated by the cloud provider.
Request a namespaced resource box ("Project" in Google Cloud terminology)
explicitly for experimenting, and your org is happy to give you one, since its
0 effort on anyones part. That has perhaps been the biggest boon in the cloud.
That amount of freedom was just not present in the earlier generations of 
computing.

This freedom is incredibly enabling. Not only can you build all kinds of 
integrations, you also get to experiment with different tools and technologies
for incredibly cheap. New load balancer? Lets see how it performs.
New NoSQL DB? Lemme set up one over the weekend, run some benchmarks and tear
it down.

The ability to reach the internet also encourages me to try and understand in 
more depth how computer networking really works. There is no blaming the 
operations team for shitty infrastructure, both power and responsibility are in
my hands. If my service is doing shitty, its all my fault. Scary at first, but
ultimately, fun.

Modern tooling makes it easy to try different things very quickly. Spin up and
tear down LB's in minutes. Configure/re-configure cloud resources instantly.
I do not learn a lot just by reading, I need to *experience* things. Most of 
the times its failures due to silly misconfiguration. Frustration with it not 
working leads first to disappointment, then resolve, then persistence and then to 
success when I finally figure out the damn thing. That success breeds confidence
and a desire to tackle harder problems. For me, its a process of starting small
and building knowledge slowly and cautiously until confidence is built on the 
capabilities of the tooling. A lot of it is unsurprisngly related to writing 
a lot, writing about everything I try and see... capture all the things, compare
with what you see today. Avoid the same mistakes.

The process is exhilarating 
and the result makes me proud. Speed of iteration is everything, though. If I
had to invest 2 hours to just get a LB to spin up, my favorite method of trial
and error just doesn't work. And I usually don't have the patience to dig deeply
into why a side project is not working as expected; I would rather just ditch 
it.
