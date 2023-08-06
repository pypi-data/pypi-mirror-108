# PyXtream - A Python Xtream Loader

## Summary

PyXtream loads the xtream IPTV content from a provider server. Groups, Channels, Series are all organized in dictionaries. Season and Episodes are retireved as needed.
This library was originally designed to work with Hypnotix at https://github.com/linuxmint/hypnotix

## Installing

```shell
pip3 install pyxtream
```

## Example

```python
from pyxtream import XTream
xt = XTream(servername, username, password, url)
if xt.authData != {}:
    xt.load_iptv()
else:
    print("Could not connect")
```

## API

XTream.Groups

XTream.Movies

XTream.Channels

XTream.Series

XTream.getSeriesInfoByID(series_id)

# Change Log

| Date | Version | Description |
| ----------- | -----| ----------- |
| 2021-06-04 | 0.1.1 | Updated README.md |
| 2021-06-04 | 0.1.0 | Initial Release |
