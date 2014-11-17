---
layout: post
title:  "Git enters the scene"
date:   2014-11-17 02:00:00
categories: walkthrough
---

The CMake build system is nice and all, but
the interesting part comes when you add Git.
Both the pile and the helper are git repositories.
There are two different repositories because
we want the user to have a directory as simple
as possible when he/she gets the pile.

By using the [submodule](http://git-scm.com/docs/git-submodule)
feature we mitigate most
of the effects of this, as the maintainer of
the pile will store the duo in a single folder,
as explained below.

To create a pile from Git's point of view we
create the two directories - `pile` and `pile-helpers`
with their respective content, then:

{% highlight bash %}
PILE=refcnt
cd ~/yard/$PILE
git init
git add .
git commit -m "Initial commit"

cd ~/yard/$PILE-helpers
git init
git add .
git commit -m "Initial commit"
{% endhighlight %}

Next, we can (and should) set a remote for both
our repositories:

{% highlight bash %}
cd ~/yard/$PILE
git remote add origin git@github.com:pile-contributors/$PILE.git
git push --set-upstream origin master

cd ~/yard/$PILE-helpers
git remote add origin git@github.com:pile-contributors/$PILE-helpers.git
git push --set-upstream origin master
{% endhighlight %}

This is all pretty standard. Now comes the funky part:
we add the pile as a *submodule* to the helpers
repository. Once we do so the original directory
that hosted the pile (`~/yard/refcnt` in our case)
can be safely be deleted and we end up with a
single directory to hold the source of our pile
and related resources:

{% highlight bash %}
cd ~/yard/$PILE-helpers
git submodule add "git@github.com:pile-contributors/$PILE.git" "$PILE"
git add .
git ci -m "Imported pile source code"
git push
rm -rf ~/yard/$PILE
{% endhighlight %}

If you make changes to the pile code, commit them as
you would normally do:
{% highlight bash %}
cd ~/yard/$PILE-helpers/$PILE
git add . --all
git commit -m "Some changes happened"
git push
{% endhighlight %}

Remember, however, that the submodule feature links a repository
to a commit in another repository. Thus, the helpers repository is
left to reference the commit that was previously the HEAD in our pile.
To update to our latest commit we need to:
{% highlight bash %}
cd ~/yard/$PILE-helpers
git add $PILE
git commit -m "Upstream pile updated"
git push
{% endhighlight %}

We need to do this whenever the HEAD for our pile changes,
like if someone else updated the pile or you are using
someone else's piles and he/she updated it.

To [clone](http://git-scm.com/docs/git-clone)
a git repository that contains submodules one uses
the command as follows:
{% highlight bash %}
git clone --recursive git@github.com:pile-contributors/$PILE-helpers.git
{% endhighlight %}

If you forgot to add the `--recursive` - no biggie. Just
{% highlight bash %}
git submodule update --init --recursive
{% endhighlight %}



