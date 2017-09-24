"""
TODO: http://www.nobius.org/~dbg/practical-file-system-design.pdf

Requirements -
1) read vs write frequency
2) sequential vs random access
3) file-size distribution
4) long vs short-lived files
5) proportion of files to directories
6) directory size

Design goals of a file system -
1) Journaling - Its for added file system integrity and quick boot times.
2) 64-bit file sizes


TODO - http://web.cs.ucla.edu/classes/fall10/cs111/scribe/11a/
FAT file system vs BSD unix file system

Other references -
https://www.cs.hmc.edu/~geoff/classes/hmc.cs135.201109/slides/class03_filesystems_beamer.pdf

MIT file system design HW - http://web.mit.edu/6.033/1997/handouts/html/04sfs.html
"""