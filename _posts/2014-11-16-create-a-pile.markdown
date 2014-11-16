---
layout: post
title:  "Creating a pile from a C++ class"
date:   2014-11-16 00:00:00
categories: walkthrough
---

We are going to do through the creation of
a pile for a C++ class step-by-step. There
are automated ways to do this at the end of 
this post.

A pile template is also present in our
repository at [pile-template-cpp](https://github.com/pile-contributors/pile-template-cpp).

The class
---------

Let us start with a simple class that does 
reference counting for us. Note that, if you
are looking for an actual implementation we have
[a pile](/404.html) for it that does a lot more.

{% highlight c++ %}
// refcnt.h
class RefCnt {
private:
    int ref_cnt_;
protected:
    RefCnt();
private:
    virtual ~RefCnt();
public:
    void acquire() {
        ++ref_cnt_;
    }
    void release() {
        if (--ref_cnt_ <= 0) {
            delete this;
        }
    }
}
{% endhighlight %}

{% highlight c++ %}
// refcnt.cc
RefCnt::RefCnt() :
    ref_cnt_(1)
{}
RefCnt::~RefCnt()
{}
{% endhighlight %}

Instead of just throwing this class inside our source tree
we may think that we will use this class in future projects
so we should create a pile. This way improvements to this 
class will propagate to all the projects that use it.

The structure
-------------

Create two directories: `refcnt` and `refcnt-helpers`
somewhere. I will use `~\yard`, so the full path
to the directories is `~\yard\refcnt` and `~\yard\refcnt-helpers`;

The pile
========

The `refcnt` directory is the one that will host our actual
pile. We want to keep things simple here so that when we're
going to came back in a few months to understand 
what's going on in a blink of an eye. Whatever tests, support,
related scripts, project files we may nee we're going to throw
in `refcnt-helpers`.

So let's move `refcnt.h` and `refcnt.cc` inside
`~\yard\refcnt`. next, we're going to need a cmake file
that will configure our pile. We do so not with a standard
`CMakeLists.txt` (we're going to use it in a minute) but 
with a script file named after the pile. We do that
because CMake uses `CMakeLists.txt` in a predefined manner
and we want to be more flexible.

[pile-cmake](https://github.com/pile-contributors/pile-cmake)
offers a number of helper macros and we're going to make use of
those to create following simple file:

{% highlight cmake %}
# refcnt.cmake

# TODO

{% endhighlight %}

Now for the `CMakeLists.txt`, all we have to do
is add to following lines:

{% highlight cmake %}
# CMakeLists.txt

# TODO

{% endhighlight %}

and we will be able to use this directory as a standard
library build by CMake, if we want that. 

The helpers
===========

As I said earlier, `~\yard\refcnt-helpers` is for 
everything else. Notably, we can use it to store the 
tests and, in this way, to show basic usage examples 
for our pile.

We add a top `CMakeLists.txt`:

{% highlight cmake %}
# CMakeLists.txt

# TODO

{% endhighlight %}

