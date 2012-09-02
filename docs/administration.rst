Administration
==============

The administration is available at the ``/admin`` url, or on the demo deployed
at http://tcp.agopian.info/admin.
You may login using the demo credentials ``admin:admin``.

There's two items available:

* Requests: the list of all requests (manual and through the API)
* Providers: where the configuration of new (or existing) providers is done

Providers configuration
-----------------------

The http://tcp.agopian.info/admin/provider/provider/ link displays the list of
current providers. It's possible to search a provider by its name using the top
search bar.

Adding or modifying a provider is as simple as clicking on the "Add provider"
button in the top-right corner, or on the name of an existing provider.

* Name: purely informal
* Link template: template used to build the canonical link from the video id.
  It should contain the ``{{ video_id }}`` template tag where the video id
  should be replaced.
* Embed template: template used to build the new embed code. The link built
  from the previous template will replace the ``{{ video_link }}`` tag.
* Validation link template: used to validate that the video is still available
  (returns a ``HTTP status code`` less than 400).

Link Matches
------------

Those are the `regular expressions`_ used to map an embed code to a provider.
It should capture the video id, used in the link template above.


Please take example on the current configured providers!

.. _`regular expressions`: http://docs.python.org/library/re.html
