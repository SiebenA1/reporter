# report_generator

## Table of Contents

- [report\_generator](#report_generator)
  - [Table of Contents](#table-of-contents)
  - [Disclaimer](#disclaimer)
  - [Licenses](#licenses)
  - [Release](#release)
  - [Description](#description)
  - [How To Update](#how-to-update)
  - [Processing](#processing)
    - [Activity Diagram](#activity-diagram)
    - [Process Description](#process-description)
  - [Architecture](#architecture)
  - [Installation](#installation)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [General](#general)
    - [Arguments](#arguments)
    - [Examples](#examples)
      - [Default Script Execution](#default-script-execution)
      - [Script Execution with Debug Mode](#script-execution-with-debug-mode)
  - [Input](#input)
  - [Output](#output)
    - [Commandline Output Example](#commandline-output-example)
    - [CSV File Output Example](#csv-file-output-example)
  - [Testing](#testing)
  - [Setup](#setup)
    - [Process Flow](#process-flow)
    - [How to Create an Exe File](#how-to-create-an-exe-file)
  - [Features, Issues \& Limitations](#features-issues--limitations)
    - [List of Features](#list-of-features)
    - [Known Issues](#known-issues)
    - [Known Limitations](#known-limitations)

## Disclaimer

|||
|-|-|
|||

## Licenses

Further details can be found in `doc/license`.

## Release

Current release version and further details can be found in `CHANGELOG.md`.

## Description

**TODO** is a python tool to...

## How To Update

```powershell
```

## Processing

### Activity Diagram

The following diagram shows the sequence of actions of the python script.

### Process Description

## Architecture

## Installation

1. Install Python 3.11.x to your local machine

2. Create and activate virtual environment in Powershell window

```powershell
# powershell
python3 -m venv <PATH_AND_NAME_TO_VENV>
<PATH_AND_NAME_TO_VENV>\Scripts\activate.ps1
```

3. Update pip

```powershell
# powershell
python -m pip install --upgrade pip
```

4. Install requirements

```powershell
# powershell
python -m pip install -r requirements_full.txt
```

## Requirements

See `requirements.txt`

## Usage

### General

See the scripts help information for more details.

```powershell
python -m report_generator
```

```powershell
.\report_generator.exe --help
```

### Arguments

```powershell
```

### Examples

#### Default Script Execution

```powershell

```

#### Script Execution with Debug Mode

```powershell

```

## Input

todo

## Output

todo

### Commandline Output Example

todo

### CSV File Output Example

The output csv file is saved to the via parameter given input folder <input_folder_path>.

```csv
todo
```

## Testing

Test implementation can be run with the help of nox module.

A test report and coverage report is created. The submodules are also considered.

```powershell
nox -s lint
nox -s test
```

## Setup

This chapter contains the description of setup routine for the tool. With help of setup routine the main script of the tool can be converted from python source code to a compiled windows exe delivery item.

### Process Flow

1. Get version information from `version.py`
2. Print start inforamtion to command line
3. Clean up old setup with removing setup directories
4. Check if python script files are configured for setup?
   1. Exit if no script file is configured for setup
5. Create delivery item folder structure
6. For each configured python script do the following tasks
   1. Create a new log file with date time appendix
   2. Do setup call to build the exe file
   3. Copy the compiled exe to the delivery item folder
   4. Remove the build directory
   5. Prepare all script dependencies in the delivery item folder
7. Create a user readable version text file
8. Create a release information file
9. Create final delivery item as zip file

### How to Create an Exe File

1. Create a new clean python virtual environment with the requirements installed.
2. Check the version information in `version.py`
3. Run 'nox -s build' from command line in virtual environment.
4. The final delivery item will be created in the `delivery` directory.

The delivery item is now ready for upload to gitlab package registry.

## Features, Issues & Limitations

<!-- features-start -->
### List of Features

| Feature ID | Status | Feature Name | Feature Description |
| --- | --- | --- | --- |

### Known Issues

| Issue ID | Status | Issue Name | Issue Description | Proposed Solution |
| --- | --- | --- | --- | --- |

### Known Limitations

| Limitation ID | Status | Limitation Name | Limitation Description | Proposed Solution |
| --- | --- | --- | --- | --- |
