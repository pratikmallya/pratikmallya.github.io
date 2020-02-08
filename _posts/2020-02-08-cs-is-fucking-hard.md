---
layout: post
title: "Software Engineering is Hard"
description: "Software Engineering is Hard"
tags: ["engineering", "software"]
---

Software engineering is really hard. I severely underestimated the magnitude
of the problem. Machines are unreliable. Computers fail all the time. 
Database systems get corrupted. HTTP requests fail for no discernable reason.
Things that run just fine on one machine behave weirdly on another. Code that
compiled yesterday doesn't today.


If I had known just how difficult the field really is, I would not have 
entered it. Physics is even harder but at least your probing the secrets of 
nature. Manager of unreliable machines does not sound very appealing. 
Especially around the time I graduated, the situation was even worse. No cloud,
IaaS was just taking off. How the heck did people sleep at night without 
PagerDuty/DataDog actively  monitoring their shit? With only Slack to 
communicate with team members... I guess people actually called each other 
when something bad happened.

Hoever, cloud and other reliability improvements to the base layers of 
computing have made it a lot more solid, and improvements in observability 
make it easier to see why something failed. Systems remain unreliable as 
before, but ways of getting around that behavior is now known. OK so maybe it
isn't that bad.

I don't envy those lured by bootcamps into learning programming. There is 
just so much stuff to know and understand and it changes so much so fast. 
Writing simple code may not be hard, deploying it at scale and reliably still
is. Well, at least it ain't trivial.

Heroku was a step in the right direction. PaaS and FaaS is what developers 
really want. The OPS part of DevOps is still hard and most developers would 
rather not do it. Perhaps FaaS will become powerful and cheap enough that 
they don't have to. Who knows.  
