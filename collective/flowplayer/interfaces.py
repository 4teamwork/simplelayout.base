from zope.interface import Interface


class IFlowPlayable(Interface):
    """A file playable in the flowplayer
    """


class IVideo(IFlowPlayable):
    """Marker interface for files that contain FLV content
    """


class IAudio(IFlowPlayable):
    """Marker interface for files that contain audio content
    """


class IMediaInfo(Interface):
    """Information about a video object
    """
