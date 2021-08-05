Untitled Random Knot Project
============================

One knot diagram per crossing number from 3...1000.  To install, clone
this repo and do::

  % sage -pip install .

Basic usage::

  >>> import knot_sample
  >>> knot_sample.knot(100)
  <Link: 1 comp; 100 cross>
  >>> E = knot_sample.exterior(100)
  >>> E.num_tetrahedra()
  213
