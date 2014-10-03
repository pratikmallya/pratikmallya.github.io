---
layout: post
title: "Introducing My New Blog"
description: "New blog of Pratik Mallya"
tags: [jekyll, intros]
---

The first blog that I wrote in was in blogspot, or blogger (I'm still not
sure what the difference is between them). I then tried Wordpress, before
finally settling on [blogger]("http://approxint.blogspot.com/") again. To
be fair, the new blogger is pretty good, and I do like the minimalistic
theme. However, I wanted absolute, complete control over my website. Why?
Ownership breeds pride. I won't put in personal manual labor improving the
garden of my rented house. But if it was my own, I most certainly would.

Similarly, with complete ownership over my content and how it's displayed,
I can put in effort into designing it better. I mean CSS-styles better.
I mean having the option to use superb UI frameworks like
[Foundation](http://foundation.zurb.com/).

I've decided to start with a very simplistic, very very minimalistic design
though. I will be playing around with CSS to make it look nicer, but I won't
be putting in any flashy stuff. My inspiration is the indomitable Mike
Bostock, whose [blog](http://bost.ocks.org/mike/) made me realize that
features do not equal beauty. (He also resolved the very important problem
of naming one's blog: simply use your full name).

Configuring A Custom Domain
---------------------------
One of the first things I wanted was a custom domain name. There are many
reasons why you would want to host your website under a custom domain name
rather than using Github's subdomain, but I think the most important one is
that in case I wanted to move my site away from Github, I would have to
change all references to my old webpage: Resume's, other websites, business
cards etc. Having you own domain name can be really cheap, I used
[Namecheap](https://www.namecheap.com) to obtain mine for $8 p.a.

I wasn't very familiar with DNS, so at first I had trouble configuring it.
In particular, I did not configure an A record to point to the IP address of
Github. An A record is an address record, which is what tells your DNS host
(in this case, Namecheap) where it can find the content for the domain.
Since I did not configure it, of course the content could not be found.

Anyways, here's what you need to do:
* Add a [CNAME](https://github.com/pratikmallya/pratikmallya.github.io/blob/master/CNAME)
  file in your repository which contains the bare domain name.

* Configure _two_ A records to point to the ip address of Github
  pages in Namecheap. You can find the IP addresses
  [here](https://help.github.com/articles/my-custom-domain-isn-t-working#dns-errors)

* Add a CNAME for the url provided by Github in Namecheap, so that everyone that
  tries to access that url will be redirected to your new page. So,
  my case I added a CNAME record with url as
  [pratikmallya.github.io]("http://pratikmallya.github.io").
  Therefore, anyone entering that url in the browser will be
  automatically redirected to my custom domain name
  [mallya.me](http://mallya.me)

Thanks
------
My friend Prakhar Srivastav has been responsible for much of the styling
improvements, especially optimizations for mobile devices. He did so without
me even asking for his help! It goes without saying that the blog looks much
nicer after contribution; and also his tips on making it more SEO-friendly.
Check out his awesome [blog](http://prakhar.me/) for more
awesome stuff. He also convinced me to use
[Jekyll](http://jekyllrb.com/), which is super simple to setup and use.
