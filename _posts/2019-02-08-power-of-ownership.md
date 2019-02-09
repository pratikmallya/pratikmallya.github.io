---
layout: post
title: "How to write documentation without dying of boredom"
description: "Musings on writing documentation"
tags: [Productivity, Documentation]
---

**TLDR**: Write docs in Markdown, watch this [video](https://www.youtube.com/watch?v=pY5i0Io86UQ)

There was an incident that happened at my current workplace which made me re-think my motivations and drive at work. We use a somewhat obtuse tool called Confluence at our company to document things, both for technical and non-technical stuff. Whenever I would be tasked with writing documentation, it would perhaps be the worst part of my day. Why?

* The UI itself seems ridiculously outdated; perhaps that makes me superficial, but I read quite a few blogs, so have seen what kind of layouts/style are common. Reading something formatted poorly seemed like an exercise in futility. It felt like we now had amazing tools for presentation and had just not adopted them (which seems like an easy win)
* The only history that you can see is the last edit made; looking at changes by clicking through a bunch of "page history" buttons doesn't seem easy. What I didn't realize right away is that with documentation, some metadata around the reasons for the changes made can tell you a lot about whether the doc is trustworthy. Something that was true when your code was deployed in the DataCenter may not hold now when your code is in the Cloud.
* The only way to make changes is to literally edit every page by hand; this makes it really hard to adopt better formats or standards
* Pages are organized in a tree-like manner, but its hard to understand what the relationship is, leading to duplications, parallel documentations of the same things, and general mayhem

You can see how writing documentation with such a tool feels so amazingly disheartening.

And then I saw this great talk on [empowering non-developers to use Git](https://www.youtube.com/watch?v=pY5i0Io86UQ); the premise is basically how the author and his team convinced even the non technical folks to start using Git as a collaboration tool to write content in Markdown, and then use CI/CD to auto-publish the content on merge.

Busy with other things I didn't pay it much attention, other than posting the link to the talk in a slack channel. But then, the team manager decided to write the team charter as Markdown in Git, and then used a [python script](https://github.com/RittmanMead/md_to_conf) to deploy that to confluence, on merge. Aha!


The idea caught on pretty soon and we started moving a large amount of documentation to Git. Writing documentation is so much easier when you follow the same workflow as code contributions. It feels "clean". You can use Github labels to indicate the stage of your documentation ("draft", "ready for review" etc.). No need to deal with setting the layouts correctly. We even started moving design docs and other Google Document based content to Markdown. I actually _want_ to write documentation for things that I feel others would benefit from, and that is perhaps the most important benefit.
