**Cifonauta** is an image database for marine organisms created by the [Marine Biology Center](http://www.usb.br/cbm/) of [University of São Paulo](http://www.usp.br/) (CEBIMar/USP) in an effort to share scientific information produced by research projects and teaching activities of the center.

Content is organized by descriptive information such as taxonomic classification, life stage, geolocation, references, and other tags, and can be browsed and refined interactively.

Project developed with [Python](http://python.org/) using [Django](http://djangoproject.com/) framework and [PostgreSQL](http://postgresql.org/)database.

**URL:** http://cifonauta.cebimar.usp.br/

**Authors:** Alvaro E. Migotto & Bruno C. Vellutini

**Support:** CNPq - National Council for Scientific and Technological Development, Call MCT / CNPq No. 42/2007 (process 551951/2008-7).


== Vagrant support ==

For this, you need to instal Virtual Box on [https://www.virtualbox.org/]

On the root of the project, run `vagrant up` and it will install the Virtual Machine (VM). This may take some time... once it's completed, run `vagrant ssh` and you'll ssh the VM.

Once on the VM, `cd /var/www` and you'll be in the root of the project. Then you should start running the server (this is the bit that needs to be complete).