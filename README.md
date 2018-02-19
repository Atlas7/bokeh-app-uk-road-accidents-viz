# UK Road Accidents Visualization Web Appliaction

![bokeh-app-uk-accidents-viz-v6.gif](./assets/bokeh-app-uk-accidents-viz-v6.gif)

[See live App on Heroku](https://uk-road-accidents-viz.herokuapp.com/) - work in progress...

This is an interactive web application tool that enables big data visualization of the 136k+ UK Road Accidents reported during 2016 (I may expand this to cover a longer period under a separate project).

- **For high level summary**: use the pan and wheel/box zoom tools to interact with the plots. Visualize the overall reported accident distributions, concentrations and locations by zooming and panning at the appropriate levels.
- **For low level investigation**: zoom all the way in to visualize the exact location of an individual reported accident.

For more information about the datasets please refer to [the Road Safety Data Page](https://data.gov.uk/dataset/road-accidents-safety-data), which contains datasets for other periods and dimensions.

This work is inspired by the [pyviz](https://github.com/pyviz/pyviz) tutorial series. It is my hope to incorporate further enhancements to this application, refactor and optimise the codes, and use as a reference baseline template for building other similar applications with even better capabilities.

Built with Anaconda Data Science Tools: Bokeh, Datashader, HoloViews, GeoViews, Dask, Pandas

## Workflow

1. Local Conda Development and Test
2. Local Docker Deployment and Test
3. Remote Docker Deployment and Test

## Local Conda Development and Test

At the root of the repository, create a Conda environment:

```
$ conda env create -f environment.yml
```

This will create a conda environment called `pyviz`, which I copied over from the pyviz](https://github.com/pyviz/pyviz) tutorial series. It contains all the big data visualization tools (including Bokeh, HolovViews, Datashader, Dask, etc.)

Activate the conda environment:

```
$ source activate pyviz
```

Serve the bokeh app:

```
$ cd apps && bokeh serve webapp --port 5006
```

See the web app locally at [http://localhost:5006/webapp](http://localhost:5006/webapp)

---

### A note on downloading and pickling data

Note: this step has already been done. So you shall not need to worry about this. But I am documenting this here anyway in case we need to reproduce it how I prepare the source data in the first place.

Download data from the internet, as defined by the `datasets.yml` file (eg. source ZIP file, extracted CSV file name, etc). All files will get processed and stored in the `data` directory (wtihin `apps/webapp`):

```
$ cd apps/webapp
$ python download_sample_data.py
```

Once we have the CSV file downloaded we need to do a quick Pandas manipulation, pickle and store onto disk back to the `data` directory.

```
$ python pickle_sample_data.py
```

Once both steps are done we should expect to see the pickled (`.pkl` ) files in the `apps/webapp/data` directory.

---

## Local Docker Deployment and Test

The eventual deployment option chosen is Heroku (for hosting the app) and Docker (for managing the deployment pipeline).

### Why I choose Heroku and Docker for deployment

The initial deployment option I've chosen is [Heroku](https://www.heroku.com/) - purely driven by its ease of deployment pipeline, free (as in prototyping deployment cost), and familarity - I've used it before in the dployment of [this ReactJS app](https://fungai-react-ui.herokuapp.com/fungpredict).

Option 1: Initially I tried out the [Heroku conda-buildpack](https://github.com/kennethreitz/conda-buildpack) - I had to drop this option in the end due to its inability to pull conda packages from other channels other than the default `continuum` Channel (at the time of writing this). See [this GitHub issue 11](https://github.com/kennethreitz/conda-buildpack/issues/11).

Option 2: I also considered the default Heroku deploy option also which uses vanila `pip` instead of conda. I had to drop this option in the end due to complexity (most Bokeh / Datashader / HoloViews examples are based on Conda packages. To port to using `pip` could be an overhaul).

Option 3:  The `README` file of the conda-buildpack however suggests there is an alternative Heroku-recommended option - [Heroku Docker Deployment](https://devcenter.heroku.com/articles/container-registry-and-runtime#getting-started). This option appears to offer most flexibilty and robustness for both local and remote deployment. Though at the time of writing this my Docker skill was quite basic I believe it could be a good opportunity to learn and pick up this emerging technologies - the long term benefits could be worth it (at the short-term learning curve).

This section documents how I deployment a Docker-ized Bokeh app locally (without the Heroku part yet)

At the root of the repository, build the Docker Image:

```
docker build -t bokeh-app-uk-road-accidents-viz:miniconda-pyviz-1 .
```

This will build a Docker Image called `bokeh-app-uk-road-accidents-viz` with a tag of `miniconda-pyviz-1`.

---

Question: why I name the tag this way?

Answer: the `Dockerfile` is built on top of `continuumio/miniconda` (hence the `miniconda`). The Conda environment (as defined in `environment.ymnl`) is called `pyviz`, copied over from the pyviz](https://github.com/pyviz/pyviz) tutorial series. The `1` at the end is just for us to keep track of Docker images should we decided to try out different things, such as modifying `Dockerfile` contents for experimentation purpose. Without the tag `1` at the end it will simply be set to the default `latest` (if you would just like to keep overwriting the same image, `latest` tag may be the best).

---

To see the web app, simply run this (from any local directory - it doesn't matter)

```
export PORT=5006 && docker run -i -t -p $PORT:$PORT bokeh-app-uk-road-accidents-viz:miniconda-pyviz-1 /bin/bash -c "source activate pyviz && bokeh serve webapp --port=$PORT --address=0.0.0.0 --usea-xheaders"
```

---

Question: what does this command mean?

Answer:

- first, we create an environmental variable `PORT` that has the value of 5006 (the default port number for Bokeh App).
- we use `docker run` to spin up a the docker image that we built earlier (`bokeh-app-uk-road-accidents-viz:miniconda-pyviz-1`) and create a Docker container (with a random name). This container is effectively our app and runs in an isolated environment.
- the `docker run` options `-i` (Keep STDIN open even if not attached) and `-t` (Allocate a pseudo-tty), enables us to run the container in an interactive way. Like running a shell. We can view the web GET/POST request logs directly in front of us in the terminal. (and whenever we want to kill the app, we just do a `Ctrl + c`).
- About the `-p $PORT:$PORT` option: this is Docker way of mapping our localhost (e.g. our laptop) port number (left hand side), to the container port number (right hand side). The reason we use an environmental variable is to make this consistent with Heroku deployment - which uses `$PORT` for port configuration. Feel free to hard code the port numbers for experimentation purpose though!
- the remaining `bin/bash -c "..."` is our way of overriding the default command to be run at container creation, as defined in the `Dockerfile` - under the line `CMD ["..."]`.
- to explain a bit about the local test command:
  - `source activate pyviz`: to activate our `pyviz` conda environment, which was created at the Docker Image build srage. (and defined by the `environment.yml` file)
  - `bokeh serve webapp --port=$PORT --address=0.0.0.0 --usea-xheaders`: after spinning up the container our work directory is changed to `apps/`. We run this command at this work directory to serve a Bokeh app within the container. Within the container it serve the app at [http://0.0.0.0:$PORT/webapp](http://0.0.0.0:$PORT/webapp). We can access this app at [http://localhost:$PORT/webapp](http://localhost:$PORT/webapp)

---

Navigate to [http://localhost:5006/app](http://localhost:5006/app) to view and interact with the web application.

## Remote Docker Deployment and Test

Use [Container Registry & Runtime (Docker Deploys)](https://devcenter.heroku.com/articles/container-registry-and-runtime#pushing-an-image-s) for now.

Still a work in progress to get this working.

## Improvement opportunities

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

[Serving interactive bokeh figure on heroku](https://stackoverflow.com/questions/38417200/serving-interactive-bokeh-figure-on-heroku/38447618#38447618): stackoverflow solution.

[fungai-react-ui](https://github.com/Atlas7/fungai-react-ui): `README` file may come in handy.

[conda-buildpack](https://github.com/kennethreitz/conda-buildpack): Heroku deployment with just conda (and no docker)
