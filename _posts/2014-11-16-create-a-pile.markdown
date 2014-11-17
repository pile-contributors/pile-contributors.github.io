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

This is NOT what you are going to do to
create piles, it only serves as an example for
you to better understand the philosophy.

A pile template is also present in our
repository at [pile-template-cpp](https://github.com/pile-contributors/pile-template-cpp).

The class
=========

Let us start with a simple class that does 
reference counting for us. Note that, if you
are looking for an actual implementation we have
[a pile](/404.html) for it that does a lot more.

{% highlight c++ %}
// refcnt/refcnt.h
class RefCnt {
private:
    int ref_cnt_;
protected:
    RefCnt();
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
};
{% endhighlight %}

{% highlight c++ %}
// refcnt/refcnt.cc
#include "refcnt.h"
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
=============

Create two directories: `refcnt` and `refcnt-helpers`
somewhere. I will use `~\yard`, so the full path
to the directories is `~\yard\refcnt` and `~\yard\refcnt-helpers`;

The pile
--------

The `refcnt` directory is the one that will host our actual
pile. We want to keep things simple here so that when we're
going to come back in a few months to understand
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
# refcnt/refcnt.cmake

set (REFCNT_DEBUG_MSG ON)

macro    (refcntInit
          ref_cnt_use_mode)

    # default name
    set(REF_CNT_INIT_NAME "RefCnt")

    # compose the list of headers and sources
    set(REFCNT_HEADERS
        "refcnt.h")
    set(REFCNT_SOURCES
        "refcnt.cc")

    pileSetSources(
        "${REF_CNT_INIT_NAME}"
        "${REFCNT_HEADERS}"
        "${REFCNT_SOURCES}")

    pileSetCommon(
        "${REF_CNT_INIT_NAME}"
        "0;0;1;d"
        "${ref_cnt_use_mode}"
        ""
        "basics"
        "referece-count;management")

endmacro ()
{% endhighlight %}

Now for the `CMakeLists.txt`, all we have to do
is add to following lines:

{% highlight cmake %}
# refcnt/CMakeLists.txt

if (NOT REFCNT_BUILD_MODE)
    set (REFCNT_BUILD_MODE STATIC)
endif ()

include(pile_support)
pileInclude (RefCnt)
refCntInit(${REFCNT_BUILD_MODE})

{% endhighlight %}

and we will be able to use this directory as a standard
library build by CMake, if we want that. 

Now we have to include the content in a larger project.
If we want to use the source files directly, then we can do

{% highlight cmake %}
# CMakeLists.txt
cmake_minimum_required(VERSION 2.8.9)

set (PROJECT_NAME "create_pile")
project(${PROJECT_NAME})

include(pile_support)
pileInclude (RefCnt)

refCntInit(PILE)
add_executable(
    ${PROJECT_NAME}
    main.cc
    ${REFCNT_SOURCES}
    ${REFCNT_HEADERS})

{% endhighlight %}

and if we want to create a static library

{% highlight cmake %}
# CMakeLists.txt
cmake_minimum_required(VERSION 2.8.9)

set (PROJECT_NAME "create_pile")
project(${PROJECT_NAME})

add_subdirectory(refcnt)
add_executable(
    ${PROJECT_NAME}
    main.cc)
target_link_libraries(
    ${PROJECT_NAME}
    refcnt)

{% endhighlight %}

A more polished version of these code snippets
is available in
[pile-examples repository](https://github.com/pile-contributors/pile-examples/tree/master/create_pile).



The helpers
-----------

As I said earlier, `~\yard\refcnt-helpers` is for 
everything else. Notably, we can use it to store the 
tests and, in this way, to show basic usage examples 
for our pile.

The important point about the helpers is that,
although the code is held in
separate repositories, you can store them
in a single place on disk. But more on
Git repositories in [another post](#todo).

We add a top `CMakeLists.txt`:

{% highlight cmake %}
cmake_minimum_required(VERSION 2.8.9)

project(refcnt_helpers)

add_subdirectory(refcnt)
add_executable(
    refcnt_helpers
    main.cc)
target_link_libraries(
    refcnt_helpers
    refcnt)

{% endhighlight %}

and some main file.

Tools
=====

To help us in creating and managing piles a number of
tools are available. Once the content is generated you
can go ahead and customize the content that was generated.

pile-gui
--------

This is a Qt-based GUI application that has
a lot of goodies for you. It allows creating
and adding piles, and it also allows managing
then.

Others
------

There are other script tools to be developed
and will be added here in due time.
