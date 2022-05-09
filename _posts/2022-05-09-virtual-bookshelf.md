---
layout: post
title: "Virtual Bookshelf"
description: "Building a virtual bookshelf"
tags: ["books"]
---

A [hacker news post] linked to a project to build a [virtual bookshelf]. The author made the source freely avaialble, so naturally I was tempted to deploy a clone with my reading history. The result is at: [bookshelf.mallya.dev/](https://bookshelf.mallya.dev/).

The setup was fairly easy, just had to add stanzas to the [index.html] file, add a CNAME to point to it, and done! I added a few tweaks like making the books link to their goodreads page.

I did want to point out one thing I learned about custom domains. I wanted the page to be located under `bookshelf.mallya.dev`. I realized that I could just use Github pages, and so I did. To get the DNS to work correctly, I had to:

* add a file named `CNAME` [in the repo](https://github.com/pratikmallya/virtual-bookshelf/blob/816e8bac6ab3faede29d5536a6732892f28e618c/CNAME) containing the subdomain
* add a CNAME DNS record. this pointed not to the project, but to the user github subdomain. So it looks like

```
bookshelf.mallya.dev.	3573	IN	CNAME	pratikmallya.github.io.
``` 

The only annoying this is that the [index.html] file needs everything to be input manually. Not really a problem considering that there weren't all that many books. Naturally, I wanted to make it easier, and it seemed like a good opportunity to dive into JS (which I haven't really worked with in a while).

First, I did have to get the data from somewhere. I could store the raw data in a JSON and use that to generate the stanzas, but I wanted to go one step further. Did Goodreads offer an API?

It looks like [goodreads does have an api], but its [being deprecated]. 😭

But wait a second, what does the search bar in the goodreads page use? Firing up the Web Console, I was able to locate this API:

```
curl "https://www.goodreads.com/book/auto_complete?format=json&q=<ISBN>"
```

🎉🎉🎉 Awww yeah. The response is in JSON, and had links to the image, the goodreads url etc. So I started off on changing the code to use JS to:

* use goodreads API to get info on books using their ISBN
* use this data to render the virtual bookshelf

I started [here](https://github.com/pratikmallya/virtual-bookshelf/pull/1) but realized it was 1am... didn't realize how quickly time passed lol. So its still a WIP for now, and If I do complete it, I'll update this post to reflect that, and point to the refactored code.

[being deprecated]: https://help.goodreads.com/s/article/Does-Goodreads-support-the-use-of-APIs
[goodreads does have an api]: https://www.goodreads.com/api
[hacker news post]: https://news.ycombinator.com/item?id=31293727
[index.html]: https://github.com/pratikmallya/virtual-bookshelf/blob/816e8bac6ab3faede29d5536a6732892f28e618c/index.html
[virtual bookshelf]: https://petargyurov.com/bookshelf/