# Astro Python

## Introduction

Sooner or later, I will write a proper introduction to this project. For now... This is a simple Template for a project using Python for application logic and Astro with TailwindCSS for the frontend. WebUI is used as a way to bridge the two and provide a windowed interface for the application.

_It's a work in progress, You've been warned!_

[Cheak out the wiki](https://github.com/SvalTek/astro-python/wiki)

## Features

- ✅ IPC Event based communication between the Astro UI and python backend.
- ✅ Astro & Python.
- ✅ WebUI - using the available browser for the UI.
- ✅ Markdown & MDX support.
- ✅ Vue Components.
- ✅ Nanostores & Nanostores/persistant.
- ✅ Typescript & Tailwind CSS.
- ✅ Basic packaging. (win/linux x64)

## Installation

clone the repository install using the following commands:

```bash
yarn # installs node dependencies
yarn run poetry install # sets up the python environment
```

## Building & Running

To build and run the project, run the following command:

```bash
yarn run build
yarn start
```
To package the app run the following, the packaged app can then be found at dist/astro-python

```bash
# build and package using
yarn run package
# package (skipping build)
yarn run build:python-package
```
