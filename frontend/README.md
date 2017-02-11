Node.js / Angular frontend
==========================

A video surveillance frontend for Hepia Summer School project 2015.

Using Jade for HTML templates, Less for stylesheets and CoffeeScript
for javascripts.

By Antony Ducommun dit Boudry, Frederick Ney, Francesco Piva


Installation
------------

This project requires node.js on the development machine.


Build
-----

Then from the command-line:

    npm install
    bower install
    grunt

This will put production files in the assets/ folder.


Deployment
----------

Copy the following files to the server:

* package.json
* assets/
* src/

On the server, run:

    npm install --production

This will download the required dependencies.

The server can then be launched by typing:

    node src/server.js

The server listen on localhost:8080.
