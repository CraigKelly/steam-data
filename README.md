# Steam Data

A simple data project for Steam data.

If you want the entire data set, including all files generated in the process of
creating the final file, then you can download it
[here](https://s3.amazonaws.com/public-service/steam-data.tar.gz).

If you are only interested in the final data set, we have made it available on
[data.world](https://data.world/craigkelly/steam-game-data)

The subdirectory `./data` is a Makefile driven pipeline for retrieving and
cleaning all data. You'll need make and Python3.

## Other Goodies

See `./analysis` for some simple, example Jupyter notebooks examining the
data. You'll need Jupyter and the usual Python data analysis tools. Using the
jupyter Docker image `jupyter/datascience-notebook` should be sufficient.

See `./report` for a brief report on work with this dataset. The report is
in LaTeX and uses make+rubber to build the final PDF.

## Licensing

All code here is licensed under the MIT license. All data is licensed under
the data holder's license. We promise that we have made a best effort to insure
that all data that you can obtain with this code is then usable for personal
or research purposes. Please double-check with the data originator(s) if you
intend to make the data publicly available (including via publication) or to
use it for commercial purposes.

## Citing this work

Please let us know if you wish to cite this work!
