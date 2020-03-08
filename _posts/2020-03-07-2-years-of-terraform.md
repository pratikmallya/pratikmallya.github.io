---
layout: post
title: "Two Years of Terraform"
description: "How I feel after 2 years of terraform"
tags: ["terraform", "IAC"]
---

Among Infrastructure-as-Code (IAC) tools that target public cloud, terraform is arguably the most appealing due to its declarative syntax, simple architecture and [operator support]. After 2 years of using terraform and evangelizing it within the organization, some reflection over its usability are warranted.

First off, while IAC might _sound_ like its "just code", _calling it "code" results in a dissonance among developers_. Most devs, especially those used to typed languages, will get frustrated very easily when the terraform "code" they write fails for whatever reason. Any user of terraform will know that the chances of writing terraform "code" that just works (i.e. both `plan` and `apply` succeed) is exceedingly low. This is a big problem for new users. The single biggest usability improvement would be for plugin authors to implement stringent validation during the `plan` stage, but many don't and its not clear why. Since infrastructure components can be quite complex (e.g. Kubernetes clusters), it does make sense that the `apply` would fail when the infrastructure component itself failed to create successfully. However, in my experience the majority of failures seem to be related to bad parameters which could be fixed by more validation at the `plan` stage.

Terraform code is used to _manage infrastructure components_ which makes most devs reluctant to experiment with it for understandable reasons. While a bug in app code might be reverted without much damage, accidentally deleting e.g. a cloud database instance would be a catastrophic event. Accidentally removing a cloud firewall rule can have security implications. Its important to provide a sandbox environment where devs may experiment with terraform.

Which is a great segue into terraform's _readability_ issues. It uses a custom language (HCL); any new language is a burden for developers to learn. Its not clear to devs what the difference is between `resource`, `data` and `output`. The plugins get updated frequently, and code that isn't kept up to date can spit out a TON of deprecation messages in addition to the actual `plan`; this discourages devs from actually reading the `plan` as its buried in an ocean of crap.

Its not clear what _good terraform code_ looks like: should resources be organized around modules? Should _everything_ be in module and instantiated as different environments? Should one use [terragrunt]? Its not clear. There are many different ways to organize terraform code, and different patterns may exist concurrently.

Terraform was created by Hashicorp and I suspect that operating terraform at scale is something that might be easier to do in the enterprise (paid) version. I haven't used that so can't really comment on how it addresses the issues I talk about. (Personally, I would not want to use an enterprise version of terraform since my experience with enterprise support in general has been universally bad; detailing why is something I intend to do in another post).

Terraform code can get _stale_ very easily; plans are not always applied, manual changes to infrastructure are made but their corresponding terraform code is not checked in. One solution to this is to use automation and a Pull Request based workflow; [atlantis] solves this problem (and a few others). Without this automation, keeping terraform code up to date is a herculean task for devs; as a result few are willing to keep their configs up to date.

Terraform does provide some level of _disaster recovery_; although once the infrastructure it manages become large enough its questionable as to how long it would take to re-create infrastructure in the case of a true disaster. Even if terraform itself may not spin up the resources, it does provide some idea of what the configuration looked like, which is incredibly useful to know. Its likely that the person who set it all up is long gone and the tf code is the only representation of the infrastructure component that needs to be re-created.

Terraform is good at managing resources that expose apis. A new plugin (_provider_, in terraform terminology) can be written for an api very quickly. Auto-generation of terraform plugins would be pretty nice; not sure if anyone has attempted doing that. Since its written in go, it expects the plugins to be in go as well.

Despite all the issues, terraform has wide support among different providers. Once an engineering org is comfortable with terraform, it becomes easy to switch to a different cloud, since most clouds have first class support for terraform. Its declarative syntax makes it _more_ accessible to non-technical users. There doesn't seem to be an alternative that is as well supported and addresses the usability concerns.

So after 2 years, it has been a mixed bag. For Infrastructure teams who need to manage infrastructure full time, I would highly recommend using terraform. For developer teams that need to manage infrastructure components, the usability issues make it a hard sell; however, without alternatives terraform seems like the only good choice. I would very much have liked to frame the experience as a success story but the facts are that while terraform does what it promises, until its usability issues are addressed, it will remain a pain, and not a joy, to write and maintain. Tools like [terraformer] do seem promising though.

[atlantis]: https://www.runatlantis.io/
[operator support]: https://github.com/terraform-providers
[terragrunt]: https://github.com/gruntwork-io/terragrunt
[terraformer]: https://github.com/GoogleCloudPlatform/terraformer
