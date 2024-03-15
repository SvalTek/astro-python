# Astro Python

## Introduction

Sooner or later, I will write a proper introduction to this project. For now... This is a simple Template for a project using Python for application logic and Astro with TailwindCSS for the frontend. WebUI is used as a way to bridge the two and provide a windowed interface for the application.

_It's a work in progress, You've been warned!_

## Features

- ✅ IPC Event based communication between the Astro UI and python backend.
- ✅ Astro & Python.
- ✅ WebUI - using the available browser for the UI.
- ✅ Markdown & MDX support.
- ✅ Vue Components.
- ✅ Nanostores & Nanostores/persistant.
- ✅ Typescript & Tailwind CSS.

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

you can distribute the `dist` folder + the python app together in a folder and run that as a standalone application under a venv.
_I'll sort a packaging script for this soon_
