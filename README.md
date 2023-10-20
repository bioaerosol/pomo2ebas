# pomo2ebas
Debian package with tools that convert Hund BAA500 data files to EBAS Nasa Ames file format.

# Requirements for Local Setup
To develop and start this software locally, you need Python 3 and the EBAS Lib. EBAS lib can be installed with:
```
pip install  src/usr/share/pomo2ebas/ebas_io-4.1.0-py3-none-any.whl
```
You may switch to your local environment if you are using one.

For more information about EBAS package please visit https://git.nilu.no/ebas/ebas-io/-/wikis/home.

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
