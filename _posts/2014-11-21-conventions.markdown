---
layout: post
title:  "Conventions"
date:   2014-11-21 17:54:00
categories: walkthrough
---

Here are the conventions to use in the piles.

Files
-----

All file names are lower-cased. The words are
separated by underscores: `example_file.cc`.

Preprocessor definitions
-------------------------

These should be upper-cased with underscores
indicating the word boundaries.

{% highlight c++ %}
#define EXAMPLE_VALUE 567
#define EXAMPLE_MACRO(__param__) (__param__+1)
{% endhighlight %}

The macro arguments should be enclosed in
two underscores to avoid confusion.

Namespaces
----------

Namespaces are lower-cased; most of the
time they should consist of a single word.

{% highlight c++ %}
namespace example {

} // namespace example
{% endhighlight %}

The end of the namespace should also be clearly identified.

Classes
-------

The name of the class is camel-cased.

{% highlight c++ %}
class ExampleClass : public BaseClass {

}; // class ExampleClass
{% endhighlight %}

The end of the class should also be clearly identified.



[git]:        http://git-scm.com
[cmake]:      http://www.cmake.org/
[googletest]: https://code.google.com
[doxygen]:    http://www.doxygen.org
