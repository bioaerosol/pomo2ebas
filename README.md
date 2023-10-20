# pomo2ebas
Debian package with tools that convert Hund BAA500 data files to EBAS Nasa Ames file format.

# Requirements
Python 3 and 
EBAS Lib. Use the folowing command to install EBAS lib.
```
pip install  ebas-lib/ebas_io-4.1.0-py3-none-any.whl
```
For more information about EBAS package please visit https://git.nilu.no/ebas/ebas-io/-/wikis/home

# Installation
To install latest release provide a GitHub PAT as environment variable $GITHUBPAT
```
$GITHUBPAT=<PAT>
```
then download latest release using this command
```
wget -O $(curl -H "Authorization: token $GITHUBPAT" -s https://api.github.com/repos/bioaerosol/pomo2ebas/releases/latest | jq '.assets[] | select(.name | endswith(".deb")) | .name' | tr -d '"') --header "Authorization: token $GITHUBPAT" --header "Accept: application/octet-stream" $(curl -H "Authorization: token $GITHUBPAT" -s https://api.github.com/repos/bioaerosol/pomo2ebas/releases/latest | jq '.assets[] | select(.name | endswith(".deb")) | .url' | tr -d '"')
```
and finally install downloaded package file with
```
sudo dpkg -i <package-file>
```
