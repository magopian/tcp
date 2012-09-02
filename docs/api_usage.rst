API usage
=========

Setting your ``Accept-encoding`` header to ``application/json`` will trigger
the "API mode". It'll answer with ``json`` data.

Example::

    $ curl -H "Accept-encoding: application/json" --data-urlencode 'initial_code=<iframe src="http://player.vimeo.com/video/17921737?title=0&byline=0&portrait=0&color=ffffff" width="480" height="372" frameborder="0"></iframe>' http://tcp.agopian.info

    {"video_link": "http://player.vimeo.com/video/17921737", "is_valid": "true", "clean_code": "<iframe src="http://player.vimeo.com/video/17921737" width="480" height="372" frameborder="0"></iframe>", "message": "", "provider": "Vimeo"}

The ``json`` contains the following fields:

* video_link: the canonical link of the video to be embedded
* is_valid: if a ``HEAD`` request on the validation link configured in the
  administration returns a ``HTTP status code`` less than 400.
* clean_code: the new embed code
* message: optional information message
* provider: the video provider
