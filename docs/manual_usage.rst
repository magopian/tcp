Manual usage
============

Launch your web browser on your server's root url, or check out the demo
available on http://tcp.agopian.info.

There's a textarea, put your video embed code in there, and watch the magic
happen:

* it first tries to find the provider (Youtube, Google Video, Dailymotion,
  Vimeo and CrossTV are already set up and configured)
* it then updates the embed code to the one configured in the administration
* it finally validates if the video is still accessible (if it finds anything
  lower than a ``400 HTTP status code``)

Examples:

Dailymotion::

    <object width="480" height="381"><param name="movie" value="http://www.dailymotion.com/swf/k6Lg9UXest3kho5p9X&related=0"></param><param name="allowFullScreen" value="true"></param><param name="allowScriptAccess" value="always"></param><embed src="http://www.dailymotion.com/swf/k6Lg9UXest3kho5p9X&related=0" type="application/x-shockwave-flash" width="480" height="381" allowFullScreen="true" allowScriptAccess="always"></embed></object>


Vimeo::

    <iframe src="http://player.vimeo.com/video/17921737?title=0&byline=0&portrait=0&color=ffffff" width="480" height="372" frameborder="0"></iframe>


Youtube::

    <object width=\"480\" height=\"390\"><param name=\"movie\" value=\"http://www.youtube.com/v/WjsTx0RLrLM?fs=1&hl=fr_FR&rel=0\"></param><param name=\"allowFullScreen\" value=\"true\"></param><param name=\"allowscriptaccess\" value=\"always\"></param><embed src=\"http://www.youtube.com/v/WjsTx0RLrLM?fs=1&hl=fr_FR&rel=0\" type=\"application/x-shockwave-flash\" width=\"480\" height=\"390\" allowscriptaccess=\"always\" allowfullscreen=\"true\"></embed></object>
