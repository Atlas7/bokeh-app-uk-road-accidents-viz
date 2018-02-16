# UK Road Accidents Visualization Web Appliaction

![bokeh-app-uk-accidents-viz-v6.gif](./assets/bokeh-app-uk-accidents-viz-v6.gif)

[See live App on Heroku](https://uk-road-accidents-viz.herokuapp.com/) - work in progress...

This is an interactive web application tool that enables big data visualization of the 136k+ UK Road Accidents reported during 2016 (I may expand this to cover a longer period under a separate project).

- **For high level summary**: use the pan and wheel/box zoom tools to interact with the plots. Visualize the overall reported accident distributions, concentrations and locations by zooming and panning at the appropriate levels.
- **For low level investigation**: zoom all the way in to visualize the exact location of an individual reported accident.

For more information about the datasets please refer to [the Road Safety Data Page](https://data.gov.uk/dataset/road-accidents-safety-data), which contains datasets for other periods and dimensions.

This work is inspired by the [pyviz](https://github.com/pyviz/pyviz) tutorial series. It is my hope to incorporate further enhancements to this application, refactor and optimise the codes, and use as a reference baseline template for building other similar applications with even better capabilities.

Built with Anaconda Data Science Tools: Bokeh, Datashader, HoloViews, GeoViews, Dask, Pandas

## Setup Conda Environment

To ensure consistent development enviroment Anaconda package manager is used to create isolated Python environment.

The `environment.yml` contains all the definitions. It's cloned from the [pyviz repo](https://github.com/pyviz/pyviz).

```
$ conda env create --force -f environment.yml
$ source activate pyviz
```

Whenever you are done with the environment just do a `source deactivate`.

## Download and Pickle Data

This step has already been done. But I am documenting this here anyway in case we need to reproduce it.

Download data from the internet, as defined by the `datasets.yml` file (eg. source ZIP file, extracted CSV file name, etc). All files will get processed and stored in the `data` directory:

```
$ python download_sample_data.py
```

Once we have the CSV file downloaded we need to do a quick Pandas manipulation, pickle and store onto disk back to the `data` directory.

```
$ python pickle_sample_data.py
```

Once both steps are done we should expect to see the pickled (`.pkl` ) files in the `data` directory.

## To run a web server locally

Start Local Server at repository root:

```
$ bokeh serve app
```

Navigate to [http://localhost:5006/app](http://localhost:5006/app) to view and interact with the web application.

## To do some experiments

If you would like to have a play, go to `.notebooks` directory, and just play around with notebooks:

```
$ jupyter notebook
```

## To deploy application to a cloud instance

Create a new Heroku app:

```
$ heroku login
$ heroku create -a name-of-your-app
$ git push heroku master
$ heroku open
```

Ensure our `pyviz` environment is already activated. (i.e. `source activate pyviz`).

Then export conda requirements to a text file `conda-requirements.txt`

```
$ conda list -e > conda-requirements.txt
```

Ensure we have a `Profile` at repos root with:

```
web: bokeh serve app --port=$PORT --host=uk-road-accidents-viz.herokuapp.com --host=* --address=0.0.0.0 --use-xheaders
```

The `app` above is our `app` folder name`. The `uk-road-accidents-viz` is our Heroku app name that we created.

Push to Heroku:

```
$ git push heroku master
```

See live app:

```
$ heroku open
```

Useful resources:

- [Serving interactive bokeh figure on heroku
](https://stackoverflow.com/questions/38417200/serving-interactive-bokeh-figure-on-heroku/38447618#38447618): stackoverflow solution.
- [fungai-react-ui](https://github.com/Atlas7/fungai-react-ui): `README` file may come in handy.
- [conda-buildpack](https://github.com/kennethreitz/conda-buildpack): `README` says we need to have the `conda-requirements` file.

## Notes

- this repository is a result of a personal 48 hour "hackathon". It can be a bit "ugly". I have done my best though to tidy as much as I can.
- it may be a good idea to start clone this repo, rename it, and build on top of it.
- at the time of creating this, the development of the HoloViews-bokeh-datashader combo was truely "bleeding edge". It is likely when you (or the future me) will find much better ways of doing things.
- Some enhancements I can think of (for another day):
  - add widgets,
  - add hover ability,
  - cover longer period,
  - add different views (e.g. breakdown by vehicle types, etc.)

## References

[pyviz](https://github.com/pyviz/pyviz): contains tutorials and reference application templates. I was able to reuse some of the codes and modify as needed.

[Road Safety Data](https://data.gov.uk/dataset/road-accidents-safety-data): produced by [data.gov.uk](https://data.gov.uk/).

[How to host a Datashader-Bokeh Interactive Map as a web application](https://stackoverflow.com/questions/48784128/how-to-host-a-datashader-bokeh-interactive-map-as-a-web-application/48806197#48806197): a stackoverflow question that I asked - and obtained the [pyviz](https://github.com/pyviz/pyviz) tutorial referene from [Jamese A. Bednar](https://stackoverflow.com/users/5909839/james-a-bednar), a Solution Architect at Continuum Analytics.

[Visualize Traffic Accidents in UK](https://github.com/Atlas7/visualize-traffic-accidents-in-uk): one of my side projects. Containing a series of Jupyter Notebooks exploring Big Data Visualization with Bokeh, Datashader, HoloViews, GeoViews, Dask, Pandas, etc.