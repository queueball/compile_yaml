# Overview

`compile_yaml` is a simple script that takes a yaml file and generates a static html page.

The driver behind such a script is the need to share some pieces of information in a nicer display format while also having a source file that's easy to grep.
One of the original design avenues was using something like markdown, but markdown has poor support for easily manipulating tables and nested data structures.
Yaml has better support for complex data structures and thus was used as a source definition file.
