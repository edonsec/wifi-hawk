# WifiHawk - Wifi Passive Recon

I wrote this as a proof of concept and it is not to be used for for any illegitimate purposes.

After setting your wifi adaptor into monitor mode (`airmon-ng start <wifi if>`), this tool passively collects wifi probe requests and logs them into a database. It can be supplied with a PCAP file also.

This database can then be used to plot approximate locations for these access points upon a google map. 

### Prerequisites

- A monitor mode compatible wifi adaptor 
- A wigle account (Create here: https://wigle.net/login?destination=/account)
- A google maps geocoding API key and a google maps javascript api key: (Create here: https://console.developers.google.com/projectselector/apis/dashboard?supportedpurview=project)
- Copy config.ini.dist to config.ini or to ~/.wifihawk.ini then complete the config

## Detail

A lot of wifi devices send "Probe" requests asking for specific networks to which they have joined before (this also happens when out of range), using these SSID names if deemed unique enough they can be used to trace a Wifi access point's location. UK ISP supplied routers tend to use unique names and can easily be used to pinpoint the location of said router using the freely available Wigle API. This can in many cases lead to identifying a home address.

This application consists of two command line applications, the first "WifiHawkCapture" will sniff for probe requests and log their details within an SQLite database, the other application "WifiHawkPlot" will utilise this database to obtain GPS coordinates for the access points - this application also leverages google maps and can plot them.

To prevent this - disable wifi when not within Wifi range and remove networks which are not used. Also consider renaming routers to far more generic names, 'linksys' is one of the most frequent ones, however this could identify you as a target for other wifi based attacks, so choose wisely.

## Usage

Sort out necessary dependencies:

```
virtualenv env
source ./env/bin/activate

python setup.py install
```

Available options
```
./WifiHawkCapture -h
./WifiHawkPlot -h
```

First run the capture (needs to be run as root):
```
./WifiHawkCapture -i wlan0mon -d "~/wifihawk.db"
```

View currently captured results (doesn't need root, but ensure db file is readable / writable by non-root):

```
./WifiHawkPlot -d "~/wifihawk.db" --dry -v
```

Attempt to plot map:

```
./WifiHawkPlot -d "~/wifihawk.db" -w resources/rules/uk-router.json -o ~/ssid-map.html -v
```

Providing no errors or limits hit - just open ~/ssid-map.html in your favourite web browser. The GPS co-ordinates will be listed in the terminal output if using verbose mode too.

## Limitations
 - There are API usage limitations on both Wigle and Google - if you hit these limits, attempt to hone the whitelist file, target a single mac address, reduce the count or segment the database table... feel free to modify the application.
