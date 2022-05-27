---
layout: post
title: "Kubernetes: Timestamp to Seconds"
description: "k8s timestamp conversion on mac"
tags: ["kubernetes"]
---

How do I convert kubernetes timestamp to seconds on mac?

Like this:
```
date -j -f "%Y-%m-%dT%TZ" "2022-05-26T17:59:12Z" "+%s"
1653613152
```
