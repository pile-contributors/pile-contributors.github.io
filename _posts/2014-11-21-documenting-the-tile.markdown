---
layout: post
title:  "Documenting the pile"
date:   2014-11-21 17:27:00
categories: walkthrough
---

We are going to use [doxygen][doxygen] for documenting
the code. CMake provides a 
[FindDoxygen.cmake](http://www.cmake.org/cmake/help/v3.1/module/FindDoxygen.html)
module that allows us to locate the executable.

Files
-----

The C / C++ source and header files shall start with 
following header:

{% highlight c++ %}
/**
 * @file example.cc
 * @brief declarations for Example class
 * @author John Smith <john.smits@home.org>
 * @author Mary Smith <mary.smits@home.org>
 * @copyright Copyright 2014 piles contributors. All rights reserved.
 * This file is released under the 
 * [MIT License](http://opensource.org/licenses/mit-license.html)
 */
{% endhighlight %}


Variables
---------

Variables are documented as follows:

{% highlight c++ %}
int i; ///< description of the variable
{% endhighlight %}

Classes
-------

The header file for a class is to contain only brief
documentation. 

{% highlight c++ %}
/**
 * @file example.cc
 */

//! This class dose nifty things.
class ExampleClass : public BaseClass {
	
	//! Create a deep copy of this class.
	ExampleClass *
	clone () const;
	
}; // class ExampleClass
{% endhighlight %}

Detailed documentation is to be included 
in the source file:

{% highlight c++ %}
/**
 * @file example.h
 */

/**
 * @class ExampleClass
 *
 * Have I told you about the nifty things this class can
 * do? Rite... So it has this beautiful clone() method...
 * 
 */

/**
 * The method may fail but don't think so.
 * @return a new instance
 */
ExampleClass * ExampleClass::clone () const
{
	// ...
};
{% endhighlight %}




Preprocessor definitions
------------------------

Preprocessor definitions are only documented 
where they appear.

{% highlight c++ %}
//! This is value 567 with a name assigned.
#define EXAMPLE_VALUE 567

//! macro that does this and that.
/**
 * Add some information about the argument
 */
#define EXAMPLE_MACRO(__param__) (__param__+1)
{% endhighlight %}

For definitions that are conditionally compiled
we can use following form:
{% highlight c++ %}
/**
 * @def ABSTRACT_AWAY_PLATFORM
 * @brief Does some wonderful simple stuff.
 *
 * This was a smart move and we now live happily ever after.
 */
#ifdef WIN32
#  define ABSTRACT_AWAY_PLATFORM (1+2 != 3)
#else // WIN32
#  define ABSTRACT_AWAY_PLATFORM (1+2 == 3)
#endif // WIN32
{% endhighlight %}


[git]:        http://git-scm.com
[cmake]:      http://www.cmake.org/
[googletest]: https://code.google.com
[doxygen]:    http://www.doxygen.org
