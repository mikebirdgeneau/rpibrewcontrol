# Raspberry Pi PID Temperature Control #

### What is this repository for? ###

* Temperature Control & Logging for Brewing using the RaspberryPi
* Version 0.1a (Early Development)

### How do I get set up? ###

In order to get started, there are a couple steps you need to perform:

Install package dependencies & required modules:
```
chmod +x install_requirements.sh
./install_requirements.sh
```

Add your pushbullet key by copying `secrets.yml.template` to `secrets.yml` and editing it to include your access key:
```
cd rpiBrewControl
cp secrets.yml.template secrets.yml
vim secrets.yml 
```

If you're working in the adafruit webIDE for development, then when you clone, you should strongly consider checking the box to not update the remote repository... this should keep it linked to this repo.