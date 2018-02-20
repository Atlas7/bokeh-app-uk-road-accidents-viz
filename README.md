# UK Road Accidents Visualization Web Application

![bokeh-app-uk-accidents-viz-v6.gif](./assets/bokeh-app-uk-accidents-viz-v6.gif)

Live demo (use either URLs):

- [https://uk-road-accidents-viz.herokuapp.com/](https://uk-road-accidents-viz.herokuapp.com/)
- [https://desolate-dusk-31283.herokuapp.com/](https://desolate-dusk-31283.herokuapp.com/)

This is an interactive web application tool that enables big data visualization of the 136k+ UK Road Accidents reported during 2016 (I may expand this to cover a longer period under a separate project).

- **For high level summary**: use the pan and wheel/box zoom tools to interact with the plots. Visualize the overall reported accident distributions, concentrations and locations by zooming and panning at the appropriate levels.
- **For low level investigation**: zoom all the way in to visualize the exact location of an individual reported accident.

For more information about the datasets please refer to [the Road Safety Data Page](https://data.gov.uk/dataset/road-accidents-safety-data), which contains datasets for other periods and dimensions.

This work is inspired by the [pyviz](https://github.com/pyviz/pyviz) tutorial series. It is my hope to incorporate further enhancements to this application, refactor and optimise the codes, and use as a reference baseline template for building other similar applications with even better capabilities.

Built with Anaconda Data Science Tools: Bokeh, Datashader, HoloViews, GeoViews, Dask, Pandas

---

**Important Notes**: Due to free-tier heroku instance / rapid prototyping purpose, the demo may be quite sluggish. It should however run much faster on a laptop locally though (with instructions provided a bit further down). Also note that the free-tier Heroku instances regularly go to "sleep" - if the app fails to zoom / respond, try refreshing the browser, wait a few seconds, and see how it goes again. Expect longer wait time when the app spin up for the first time (to let Heroku instance to "wake up").

---


## Workflow

This dev / deploy workflow is largely inspired by [pyviz workflow introduction tutorial](https://pyviz.github.io/pyviz/tutorial/01_Workflow_Introduction.html):

1. [Create Local Conda Environment](#local-conda)
2. [Local Conda Jupyter Notebook Prototype](#local-jupyter)
3. [Local Conda App Development and Test](#local-dev-test)
4. [Local Docker App Deployment and Test](#local-docker-deploy)
5. [Remote Docker App Deployment and Test](#remote-docker-deploy)

Enjoy!

<a id="local-conda"></a>
## Create Local Conda Environment

At the root of the repository, create a Conda environment:

```
$ conda env create -f environment.yml
```

This will create a conda environment called `pyviz`, which I copied over from the [pyviz](https://github.com/pyviz/pyviz) tutorial series. It contains all the big data visualization tools (including Bokeh, HolovViews, Datashader, Dask, etc.)

Activate the conda environment to make the entire Python Data Science suite available in the terminal:

```
$ source activate pyviz
```

<a id="local-jupyter"></a>
## Local Conda Jupyter Notebook Prototype

(To learn about prototyping with a Jupyter Notebook) at the root of the repository, activate conda environment and start Jupyter Notebook:

```
$ source activate pyviz
$ jupyter notebook
```

I've put together a Jupyter Notebook at the root of the repository: [Prototype A Bokeh Web Application in a Jupyter Notebook](./prototype-a-bokeh-web-app-in-a-jupyter-notebook.ipynb). Take a look - effectively we are building out what our Bokeh App may look like, before a full-fledge web application development and deployment.

Alternatively, you can [read the notebook via nbviewer here](https://nbviewer.jupyter.org/github/Atlas7/bokeh-app-uk-road-accidents-viz/blob/master/prototype-a-bokeh-web-app-in-a-jupyter-notebook.ipynb) which may be better formatted as it's pre-rendered.

<a id="local-dev-test"></a>
## Local Conda App Development and Test

At the root of the repository, activate the conda environment:

```
$ source activate pyviz
```

Navigate to the `apps` diretory and serve the bokeh app:

```
$ cd apps
$ bokeh serve webapp --port 5006
```

See the web app locally at [http://localhost:5006/webapp](http://localhost:5006/webapp)


### A note on downloading and pickling data

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


<a id="local-docker-deploy"></a>
## Local Docker App Deployment and Test

The eventual deployment option chosen is [Heroku](https://www.heroku.com/) (for hosting the app) and Docker (for managing the deployment pipeline). This combo turns out to work quite well for rapid prototyping purpose.

### Why I choose Heroku and Docker for deployment

Mainly driven by ease of use, free tier, familiarity (I've used it before), and plenty of documentations / stackoverflow troubleshoots online. Here summarises some of the decisions I made along the way:

- Option 1: Initially I tried out the [Heroku conda-buildpack](https://github.com/kennethreitz/conda-buildpack) - I had to drop this option in the end due to its inability to pull conda packages from other channels other than the default `continuum` Channel (at the time of writing this). See [this GitHub issue 11](https://github.com/kennethreitz/conda-buildpack/issues/11).
- Option 2: I also considered the default Heroku deploy option also which uses vanila `pip` instead of conda. I had to drop this option in the end due to complexity (most Bokeh / Datashader / HoloViews examples are based on Conda packages. To port to using `pip` could be an overhaul).
- Option 3:  The `README` file of the conda-buildpack however suggests there is an alternative Heroku-recommended option - [Heroku Docker Deployment](https://devcenter.heroku.com/articles/container-registry-and-runtime#getting-started). This option appears to offer most flexibility and robustness for both local and remote deployment. Though at the time of writing this my Docker skill was quite basic I believe it could be a good opportunity to learn and pick up this emerging technology - the long term benefits could be worth it (at the short-term learning curve).

This section documents how I deployment a Docker-ized Bokeh app locally (without the Heroku part yet)

At the root of the repository, build the Docker Image (defined by `Dockerfile`):

```
docker build -t bokeh-app-uk-road-accidents-viz
```

This will build a Docker Image called `bokeh-app-uk-road-accidents-viz` with a tag of `latest`. (to add a version tag at the end simply add a `:someversion` at the end. e.g. `docker build -t bokeh-app-uk-road-accidents-viz:v1`). For initial rapid prototyping and iteration purpose however, I've found using the default `latest` works quite well - I will leave this up to you.

To see the web app at [http://localhost:5006/webapp](http://localhost:5006/webapp), simply run this docker command - from any local directory (it doesn't matter)

```
docker run -i -t -p 5006:5006 bokeh-app-uk-road-accidents-viz "bokeh serve webapp --port=5006 --address=0.0.0.0"
```

Question: what does this command mean?

Answer:

- the `docker run` options `-i` (Keep STDIN open even if not attached) and `-t` (Allocate a pseudo-tty), enables us to run the container in an interactive way. Like running a shell. We can view the web GET/POST request logs directly in front of us in the terminal. (and whenever we want to kill the app, we just do a `Ctrl + c`).
- About the `-p 5006:5006` option: this is Docker way of mapping our localhost (e.g. our laptop) port number (left hand side), to the container port number (right hand side). Port `5006` turns out to be the default port number that Bokeh server uses.
- the remaining command is our way of overriding the default command to be run at container creation, as defined in the `Dockerfile` - under the line `CMD ["..."]`. (Note: because in our `Dockerfile` we've already specified the `ENTRYPOINT` as `/bin/bash -c`, by default our command will be run in bash shell. Main reason I've done this is for ease of Heroku deployment later on. Also note that the Docker image puts us in the working directory where the `webapp` folder will reside.
- to explain a bit about the local test command:
  - `bokeh serve webapp --port=$PORT --address=0.0.0.0`: after spinning up the container our work directory is changed to `/opt/apps/` (within the container). We run this command at this work directory to serve a Bokeh app within the container. Within the container it serve the app at [http://0.0.0.0:$PORT/webapp](http://0.0.0.0:$PORT/webapp). We can access this app at [http://localhost:$PORT/webapp](http://localhost:$PORT/webapp)

Navigate to [http://localhost:5006/app](http://localhost:5006/app) to view and interact with the web application.


<a id="remote-docker-deploy"></a>
## Remote Docker App Deployment and Test

The [Container Registry & Runtime (Docker Deploys)](https://devcenter.heroku.com/articles/container-registry-and-runtime#pushing-an-image-s) for documentation and [this Bokeh Server Config Doc](https://bokeh.pydata.org/en/latest/docs/user_guide/server.html) are very handy for this deployment process.


## Extra info

### FYI - Docker Hub

To potentially make life easier for other developers, I've pushed the pre-built docker image to [this Docker Hub repository](https://hub.docker.com/r/atlas7/bokeh-app-uk-road-accidents-viz/). The Docker Image uses the Continuum Miniconda Docker Image as a starting point, and prepare a install a scientific conda environment similar to the one [pyviz](https://github.com/pyviz/pyviz/blob/master/environment.yml) uses. For example, we can run `bokeh serve` with ease from a container directly, without having to install all the conda packages all over again. I've also desinged the `Dockfile` in a way that exclusively uses conda packages - i.e. no pip. Mainly motivated by familarity and simplicity.

I use [this Docker documentation: Push images to Docker Cloud](https://docs.docker.com/docker-cloud/builds/push-images/) to push my image to Docker Cloud.

## FYI - Heroku Registry

Just to emphasize: I followed the [Heroku documentation: Container Registry & Runtime (Docker Deploys)](https://devcenter.heroku.com/articles/container-registry-and-runtime#getting-started) in the deployment of the web app to a live Heroku web instance. I also find the [alpine helloworld github repo](https://github.com/heroku/alpinehelloworld/blob/master/Dockerfile) helps in understanding the mechanics of how this Docker image build / spinning up container works.

## Improvement opportunities

- at the time of creating this, the development of the HoloViews-bokeh-datashader combo was truely "bleeding edge". It is likely when you (or the future me) will find much better ways of doing things.
- Some enhancements I can think of (for another day):
  - add widgets,
  - add hover ability (see Accident ID / Longtitude / Latitude info when zoomed all the way into a point)
  - cover longer period,
  - add different views (e.g. breakdown by vehicle types, etc.)
- more performant deployment: the heroku live demo as you can probably see by now, is quite sluggish. Probably due to free tier low-budget infrastructure setup. I would be keen to see a more performant deployment option - so the user can use it just like - say, Google map.

## A Note on Bokeh

The current Bokeh version used in the conda environment is 0.12.10 - this version of `bokeh serve` currently still allows the use of the `--host` option to whitelist domain name (e.g. heroku URL). Currently I am getting web log like this:

```
2018-02-19T22:53:27.616719+00:00 app[web.1]: /opt/conda/envs/pyviz/lib/python3.6/site-packages/bokeh/command/subcommands/serve.py:320: UserWarning: The --host parameter is deprecated because it is no longer needed. It will be removed and trigger an error in a future release. Values set now will be copied to --allow-websocket-origin. Depending on your use case, you may need to set current --host values for 'allow_websocket_origin' instead.
2018-02-19T22:53:27.616735+00:00 app[web.1]:   "The --host parameter is deprecated because it is no longer needed. "
2018-02-19T22:53:27.616741+00:00 app[web.1]: 2018-02-19 22:53:27,616 Starting Bokeh server version 0.12.10 (running on Tornado 4.5.3)
```

i.e. in future we may need to consider looking into useing the `allow_websocket_origin` option, instead of `host`. Since this Docker image exclusively uses Bokeh version 0.12.10, we should be fine (for now). I am keeping a note here in case things break in future with newer version Bokeh development.

## References

[pyviz](https://github.com/pyviz/pyviz): contains tutorials and reference application templates. I was able to reuse some of the codes and modify as needed.

[Road Safety Data](https://data.gov.uk/dataset/road-accidents-safety-data): produced by [data.gov.uk](https://data.gov.uk/).

[How to host a Datashader-Bokeh Interactive Map as a web application](https://stackoverflow.com/questions/48784128/how-to-host-a-datashader-bokeh-interactive-map-as-a-web-application/48806197#48806197): a stackoverflow question that I asked - and obtained the [pyviz](https://github.com/pyviz/pyviz) tutorial referene from [Jamese A. Bednar](https://stackoverflow.com/users/5909839/james-a-bednar), a Solution Architect at Continuum Analytics.

[Visualize Traffic Accidents in UK](https://github.com/Atlas7/visualize-traffic-accidents-in-uk): one of my side projects. Containing a series of Jupyter Notebooks exploring Big Data Visualization with Bokeh, Datashader, HoloViews, GeoViews, Dask, Pandas, etc.

[Stackoverflow: Serving interactive bokeh figure on heroku](https://stackoverflow.com/questions/38417200/serving-interactive-bokeh-figure-on-heroku/38447618#38447618): stackoverflow solution.

[fungai-react-ui](https://github.com/Atlas7/fungai-react-ui): `README` file may come in handy.

[conda-buildpack](https://github.com/kennethreitz/conda-buildpack): Heroku deployment with just conda (and no docker)

[condas `source activate virtualenv` does not work within Dockerfile](https://stackoverflow.com/questions/37945759/condas-source-activate-virtualenv-does-not-work-within-dockerfile): instead of using `source activate` (which seems to be problematic when run on Heroku), set the `PATH` environmental variable to point to the newly created conda environment - this effectively use whatever in the environment.

[Docker: Push images to Docker Cloud](https://docs.docker.com/docker-cloud/builds/push-images/)

[Heroku documentation: Container Registry & Runtime (Docker Deploys)](https://devcenter.heroku.com/articles/container-registry-and-runtime#getting-started): how to deploy web app to Heroku, with Docker?

[alpine hello world github repo](https://github.com/heroku/alpinehelloworld/blob/master/Dockerfile): template `Dockerfile`.
