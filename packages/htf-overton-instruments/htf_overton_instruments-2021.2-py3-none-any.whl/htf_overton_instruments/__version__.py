import datetime


__version_info__ = (int(datetime.datetime.now().strftime("%Y")), 2,)
__version__ = ".".join(map(str, __version_info__))
