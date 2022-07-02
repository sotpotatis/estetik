# Estetik Platform

*Estetik* is a platform I created for keeping track of creative work including
photography, music and audio, and writing (but can be expanded to anything else). The platform includes a *static website with a simple
and clean aesthetic*, and *API to manage assets of the platform*. It also includes a *Python API Client* and a
*Discord management bot*.
___
## Parts included
### The website

The website is a static website that uses the API to render data. The static website is powered by *Svelte*
and *Tailwind CSS*. It has, of course, been optimized for multiple sizes of screens.

**Website screenshots**

**Website features**
* Browse content
* Interacts with the API - update once, available everywhere
* Click on an image to enlarge it

### The API

The API uses Express and is my first Node.JS project ever. It contains an open asset API
as well as a management API requiring authorization.

### The API client

There is a Python API client with wrappers around most endpoints included for interacting with the API.

### The Discord management bot

The Discord management bot is capable of adding new assets (images) and adding new parts to the website.
___
## Learning the structure of the content
The heart of the `estetik` platform is to be a digital art and media gallery. 

#### Where to place your content
The content is placed inside the `api/content` folder since the `api` acts as a media server too.
The `content` folder has several subfolders, by default three of them: `images`, `sounds`, and `text`.
These subfolders will determine which pages visitors can visit on your website and what they can explore.
This is also where you should put your static content.

#### The structure.json file
Inside each of these folders must also be a `structure.json` file. If you examine the default directory structure,
there is a `structure.json` file displaying how the content should be formatted.

The structure file is divided into *parts*. Think a *part* like a separate section,
or if you're thinking of a photo library, think of it as like a way to separate vacation
pictures from pictures you took during work.

And the *parts* is divided into *segment*. I have included several segment types. As a start, I'll use the platform personally to 
display photography, but I'll include some starter segments for other media types.
A segment can be an image, some text, or a button.

#### Page structure
By default, the page will render with 3 segments per row on screens larger than mobile.
Mobile screens will see one segment per row.
___
## Installation

### Installing the API

The API is mostly plug-and-play. Just edit the `authorized_tokens.json.example` file and add some API tokens if
you want to be able to remotely manage assets. Also rename it to `authorized_tokens.json`.
You can run the API using the command `node app.js'` or `npm run server`.

### Installing the static website

I have tested the static website with Netlify (run `npm run build` to create output files).
You can simply change the adapter used in `svelte.config.js` to any adapter to deploy it elsewhere.

### Installing the Python API Client

The API client is not available on PyPi, but you can still copy the files for the client and use it however you like.
Documentation can be found in its directory (see `automation/python_api_client`)
### Installing the Discord Bot

* Make sure the Python API Client is accessible as a package
* Set the following environment variables:
  * `ESTETIK_BOT_TOKEN` - The Discord bot token - required 
  * `ESTETIK_TOKEN` - Access token for the API - required
  * `ESTETIK_API_DOMAIN` - API domain to use for requests - required unless you are me (default domain is my API domain)
  * `ESTETIK_SSL` - `True/False` whether to disable SSL or not - optional (default if unset is True)