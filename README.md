

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][LICENSE.txt]
[![LinkedIn][linkedin-shield]][https://www.linkedin.com/in/rodrigo-soares-wurdig]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/rwurdig/Weavebio_project\img\wavebio_logo.png">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Weavebio Project</h3>

  <p align="center">
    This code reads an XML file and extracts data from it to create nodes and relationships in a Neo4j graph database. It uses the py2neo library to connect to the database and the xmltodict library to parse the XML file
    <br />
    <a href="https://github.com/rwurdig/Weavebio_project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/rwurdig/Weavebio_project">View Demo</a>
    ·
    <a href="https://github.com/rwurdig/Weavebio_project/issues">Report Bug</a>
    ·
    <a href="https://github.com/rwurdig/Weavebio_project/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/rwurdig/Weavebio_project)

## Author

👤 **Rodrigo Wurdig **

- Linkedin: [@rodrigo-soares-wurdig](https://www.linkedin.com/in/rodrigo-soares-wurdig)
- Github: [@rwurdig](https://github.com/rwurdig)
## Author
<% if (rwurdig) { %>
👤 **<%= rwurdig %>**
<% } %>
<% if (https://github.com/rwurdig/) { -%>
* Website: <%= https://github.com/rwurdig/ %>
<% } -%>
<% if (rwurdig) { -%>
* GitHub: [@<%= rwurdig %>](https://github.com/<%= rwurdig %>)
<% } -%>
<% if (rodrigo-soares-wurdig) { -%>
* LinkedIn: [@<%= rodrigo-soares-wurdig %>](https://linkedin.com/in/<%= rodrigo-soares-wurdig %>)
<% } -%>
<% } -%>
<% if (issuesUrl) { -%>
<% } -%>
<% if (rwurdig || rodrigo-soares-wurdig || authorGithubUsername) { -%>



Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Prerequisites

<% projectPrerequisites.map(({ name, value }) => { -%>
- <%= name %> <%= value %>
<% }) -%>
<% } -%>
<% if (installCommand) { -%>

You'll need to have [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/) installed in your machine to run this project.

## Running locally

Clone this repository

```bash
  git clone https://github.com/rwurdig/Weavebio_project
  cd weavebio-code-challenge
```

Give permission to the build.sh file and run it.

```bash
  chmod +x build.sh
  ./build.sh
```
Weavebio Project
Weavebio Project Logo

The Weavebio Project is a collection of computational biology tools and resources designed to facilitate the analysis and interpretation of biological data. This repository contains a diverse range of tools, from sequence alignment and phylogenetic analysis to gene expression analysis and structural bioinformatics. The project aims to provide a comprehensive resource for researchers in the field, making it easier to analyze complex datasets and draw meaningful conclusions from them.

Table of Contents
Features
Installation
Usage
Documentation
Contributing
License
Acknowledgements
Features
Sequence alignment and manipulation tools
Phylogenetic analysis and visualization
Gene expression analysis
Structural bioinformatics tools
User-friendly interfaces for complex analyses
Extensive documentation and tutorials
Actively maintained and updated
Installation
To install the Weavebio Project tools, please follow these steps:

Clone the repository:
bash
Copy code
git clone https://github.com/rwurdig/Weavebio_project.git
Change into the repository directory:
bash
Copy code
cd Weavebio_project
Install the required dependencies:
Copy code
pip install -r requirements.txt
Set up the environment and run the setup script:
arduino
Copy code
source setup.sh
Usage
The Weavebio Project is designed to be user-friendly, with a range of command-line tools and graphical interfaces for different tasks. For example, to perform a sequence alignment, you can run:

css
Copy code
weavebio seqalign -i input.fasta -o output.aln
For detailed information on how to use each tool, please refer to the Documentation section.

Documentation

# Data Engineering Coding Challenge

> *tl;dr*: The challenge is to create a data pipeline that will ingest a UniProt XML file (`data/Q9Y261.xml`) and store the data in a Neo4j graph database.
> :warning: To apply, email join@weave.bio with 1) the link to your solution repo and 2) your resume.
## Task
Read the XML file `Q9Y261.xml` located in the `data` directory. The XML file contains information about a protein. The task is to create a data pipeline that will ingest the XML file and store as much information as possible in a Neo4j graph database.

## Requirements & Tools
- Use Apache Airflow or a similar workflow management tool to orchestrate the pipeline
- The pipeline should run on a local machine
- Use open-source tools as much as possible

## Source Data
Please use the XML file provided in the `data` directory. The XML file is a subset of the [UniProt Knowledgebase](https://www.uniprot.org/help/uniprotkb).

The XML contains information about proteins, associdated genes and other biological entities. The root element of the XML is `uniprot`. Each `uniprot` element contains a `entry` element. Each `entry` element contains various elements such as `protein`, `gene`, `organism` and `reference`. Use this for the graph data model.

The full XML schema [is available here](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot.xsd).

## Neo4j Target Database
Please run a Neo4j database locally. You can download Neo4j from https://neo4j.com/download-center/ or run it in Docker:

```
docker run \
  --publish=7474:7474 --publish=7687:7687 \
  --volume=$HOME/neo4j/data:/data \
  neo4j:latest
```

Getting Started with Neo4j: https://neo4j.com/docs/getting-started/current/


## Data Model
The data model should be a graph data model. The graph should contain nodes for proteins, genes, organisms, references, and more. The graph should contain edges for the relationships between these nodes. The relationships should be based on the XML schema. For example, the `protein` element contains a `recommendedName` element. The `recommendedName` element contains a `fullName` element. The `fullName` element contains the full name of the protein. The graph should contain an edge between the `protein` node and the `fullName` node.

Here is an example for the target data model:

![Example Data Model](./img/example_data_model.png)


## Assessed Criteria

> :warning: The solution will not be assessed based on correctness of the data model with respect to biological entities. This requires domain knowledge that we do not expect you to have. 
We will assess the solution based on the following criteria:

- The solution captures most of the data from the XML
- The solution makes use of general purpose open-source tools
- The solution can be scaled to handle larger datasets

## Example Code
In the `example_code` directory, you will find some example Python code for loading data to Neo4j.

## Submission
**Please commit your solution to a new repository on GitHub**.

Feel free to use this repository as a starting point or to start from scratch. Include a `README.md` file that describes how to run the solution. 
Please also include a description how to set up and reproduce the environment required to run the solution.

Finally, email join@weave.bio with 1) the link to your solution repo and 2) your resume

Contributing
We welcome contributions to the Weavebio Project! If you have a feature request, bug report, or would like to contribute code, please open an issue or submit a pull request on the GitHub repository.

Before submitting a pull request, please ensure that your code adheres to the project's coding style guidelines and that you have updated the documentation and tests accordingly.

## Author

👤 **Rodrigo Wurdig **

- Linkedin: [@rodrigo-soares-wurdig](https://www.linkedin.com/in/rodrigo-soares-wurdig)
- Github: [@rwurdig](https://github.com/rwurdig)

License
The Weavebio Project is released under the MIT License.

Acknowledgements
The Weavebio Project is developed and maintained by rwurdig.


Table of contents

* [Table of Contents](#table-of-contents)
    * [Features](#table-of-contents-toc-generator-features)
    * [Installation](#table-of-contents-toc-generator-usage-installation)
    * [Usage](#table-of-contents-toc-generator-usage)
    * [Documentation](#table-of-contents-toc-generator-documentation)
    * [Contributing](#table-of-contents-toc-generator-contributing)
    * [License](#table-of-contents-toc-generator-license)
    * [Configuration](#table-of-contents-toc-generator-configuration)


<a name="table-of-contents-toc-generator-usage"></a>
## Usage

<a name="table-of-contents-toc-generator-usage-quick-start"></a>
### Quick Start

```js
import Contents from 'contents';



### 🏠 [Homepage](<%= https://github.com/rwurdig/Weavebio_project %>)
<% } -%>
<% if (projectDemoUrl) { -%>

### ✨ [Demo](<%= projectDemoUrl %>)
<% } -%>
<% if (projectPrerequisites && projectPrerequisites.length) { -%>

## Prerequisites

<% projectPrerequisites.map(({ name, value }) => { -%>
- <%= name %> <%= value %>
<% }) -%>
<% } -%>
<% if (installCommand) { -%>

## Install

```sh
<%= installCommand %>
```
<% } -%>
<% if (usage) { -%>

## Usage

```sh
<%= usage %>
```
<% } -%>
<% if (testCommand) { -%>

## Run tests

```sh
<%= testCommand %>
```


## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](<%= issuesUrl %>). <%= contributingUrl ? `You can also take a look at the [contributing guide](${contributingUrl}).` : '' %>
<% } -%>


## 📝 License

<% if (authorName && authorGithubUsername) { -%>
Copyright © <%= currentYear %> [<%= authorName %>](https://github.com/<%= authorGithubUsername %>).<br />
<% } -%>
This project is [<%= licenseName %>](<%= licenseUrl %>) licensed.
<% } -%>

***
<%- include('footer.md'); -%>
