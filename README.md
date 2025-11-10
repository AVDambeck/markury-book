# markury book
script that converts markdown into an html site.

This started as a framework for complex books, in print. Essentially, this is a way to write hypertext physically. Im developing a ttrpg with the restraint that i want physically booklets (inspired by the OSE game set). the framework became complex enough I wanted to develop it on its own, both to seperate the technical and artistic aspects, but also to reuse the framework with other projects.

# how it works
markuary is a python program that collects markdown, and converts them to html. 

It can look for specific flags and repalce them with dynamic content. %INDEX% and %GALLERY% are included by default, and will add a list of links to other .md in the dir, or .jpg/png/etc respectivly.

# road map
right now, the basic function of collecting md and converting to html works. The flags are being implemented. soon there will be a system to include or trigger other scripts during render, and a script that will collect the html into a pdf.

# name origin
Its a play on both markdown and jupyter book. I had tried to use jupyter to format my ttrpg, but it wasnt exactly what i wanted, so i started writing my own solution with markdown.
