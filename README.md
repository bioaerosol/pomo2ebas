# pomo2ebas

Debian package with tools that convert Hund BAA500 data files to EBAS Nasa Ames file format. The input file format is a vendor specific format of Helmut Hund
GmbH, Wetzlar. The output format is a FFI 1001 Nasa Ames format with EBAS specific extensions (additional standardized EBAS metadata) which is used by EBAS,
a database infrastructure developed and operated by NILU – Norwegian Institute for Air Research.

References:
- [Helmut Hund GmbH](https://www.hund.de)
- [EBAS Home](https://ebas.nilu.no/)
- [EBAS Nasa Ames Files](https://ebas.nilu.no/data-access/datasearch/ebas-nasa-ames/)

# Usage
## Download
To install latest release provide a GitHub PAT as environment variable $GITHUBPAT (as long as this repo is not public)
```
GITHUBPAT=<PAT>
```
and then download latest release using this command:
```
wget -O $(curl -H "Authorization: token $GITHUBPAT" -s https://api.github.com/repos/bioaerosol/pomo2ebas/releases/latest | jq '.assets[] | select(.name | endswith(".deb")) | .name' | tr -d '"') --header "Authorization: token $GITHUBPAT" --header "Accept: application/octet-stream" $(curl -H "Authorization: token $GITHUBPAT" -s https://api.github.com/repos/bioaerosol/pomo2ebas/releases/latest | jq '.assets[] | select(.name | endswith(".deb")) | .url' | tr -d '"')
```
## Installation
Package can be installed as any other Debian package, e.g.:
```
sudo apt install <package-file>
```
## Configuration
The application is configured by two files:

### Defaults
```/etc/pomo2ebas/defaults.yaml``` contains all defaults of the application:
| Key | Description |
| --- | --- |
| Config.timezone | Timezone of timestamps in output. Defaults to UTC. |
| Config.datalevel | Data level of output. Please refer to [EBAS Data Submission Manual](https://ebas-submit.nilu.no/templates/Bioaerosols/lev2) for more details. Defaults to 1.5 (NRT) |
| Config.projects | List of projects (aka EBAS framework) to which the transformed data should be assigned to. |

### Stations
```/etc/pomo2ebas/stations.yaml``` contains a detailed list of stations with their meta information which is needed to build output:

| Key | Description |
| --- | --- |
| stations.station[n] | Entry of a single station. Parameters come from [EBAS Nasa Ames Files](https://ebas.nilu.no/data-access/datasearch/ebas-nasa-ames/) specification and will be put directly to output of the data's station. |

# Development
## Requirements for Local Setup

To develop and start this software locally, you need Python 3 and the EBAS Lib. EBAS lib can be installed with:

```
pip install src/usr/share/pomo2ebas/ebas_io-4.1.0-py3-none-any.whl
```

You may switch to your local environment if you are using one.

For more information about EBAS package please visit https://git.nilu.no/ebas/ebas-io/-/wikis/home.

