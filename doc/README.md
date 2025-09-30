# Architecture Documentation of the Online Characterization Method

We use a doc-as-code approach based on [arc42](https://arc42.org/) and the [C4
model](https://c4model.com/) using the
[structurizr](https://docs.structurizr.com/) tools for generating a static
documentation html site.

## What can I do here?

* ***You need docker to use the tools.***
* ***You need bash to use the tools.*** If your OS doesn't have bash (Mac's can install bash via homebrew)
  look up the scripts in the tools directory to see how you would start the docker container without bash.

### Edit

Edit the documents under [./src](./src).

### Check

Run `./tools/validate`.

### View

* Run a local server for the generated site: run `PORT=8080 ./tools/serve`.
* Browse to [http://localhost:8080](http://localhost:8080) to view the results.

## Sources

The src directory contains the doc-as-code sources.

* [./src/architecture.md](./src/architecture.md) - the arc42-based architecure documentation.
* [./src/workspace.dsl](./src/workspace.dsl) - the root file of the structurizr workspace.
* [./src/views/](./src/views/) - contains the structurizr views.
* [./src/model/](./src/model/) - contains the structurizr model.
  * In the models directory, the [src/model/model.dsl](./src/model/model.dsl) is the root file, including
    other files in the same directory.
  * Please add a single file for every *group* -- e.g.,
    [src/model/repositories.dsl](./src/model/repositories.dsl) for the "Repositories" group -- and add everything
    that belongs to the group as well as relations *within* elements of that group.
  * Put all *inter-group* relations into [src/model/relations.dsl](./src/model/relations.dsl)
* [./src/decisions/](./src/decisions/) - contains Architecture Decision Records (adr).

## Tools

The tools directory contains the following tools:

* [./tools/serve](./tools/serve) - serve a static site on http://localhost:8080 which renders the documentation,
  including diagrams.
* [./tools/validate](./tools/validate) - validate your structurizr workspace.
* [./tools/structurizer-lite](./tools/structurizer-lite) - the original structurizer-lite tool. Use this to interactively
  layout single diagrams. http://localhost:8081
* [./tools/plantuml](./tools/plantuml) - serve a local plantuml webui under http://localhost:8082 which can help
  you editing plantuml diagrams.
* [./tools/export](./tools/export) - export the C4 diagrams as Plantuml text files to [./export](./export).

All tools require docker, more information in the [readme](tools/README.md) in the tools directory.

## Background

### More Docs

* [Generator](https://github.com/avisi-cloud/structurizr-site-generatr)
* [Markdown Flavor](https://avisi-cloud.github.io/structurizr-site-generatr/main/extended-markdown-features/)
* [Structurizr](https://docs.structurizr.com/)
* [C4](https://c4model.com/)
* [Arc42](https://arc42.org/documentation/)
* [Plantuml](https://plantuml.com/)

## License

* Copyright (C) 2024-2025 IndiScale GmbH <mailto:info@indiscale.com>
* Copyright (C) 2024-2025 Timm Fitschen
* Copyright (C) 2024 Henrik tom Wörden

The documents under the subdirectory [./src](./src/) are licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) unless expressly stated otherwise.

Code under the subdirectory [./tools](./tools/) is licensed under the
[GNU Affero General Public License](./LICENSE.md) (version 3 or later) unless expressly stated otherwise.
