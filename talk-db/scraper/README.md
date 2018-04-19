## Setup

- On Mac, with Homebrew/ Homebrew Cask:
  * Install Mongodb, with `brew install mongodb`, then `mkdir -p /data/db`
  * (Optional) Install Robo 3T to view database, using `brew cask install robo-3t`

- Launch Mongodb with `mongod`
  * You should see: `[initandlisten] waiting for connections on port 27017`

## Usage

- To run normally, populating database: `scrapy crawl stalker`
- To run and create JSON: `scrapy crawl stalker -t json -o - > "data/people.json"`

## Notes

- To launch interactive MongoDB shell type:
  * `/usr/local/Cellar/mongodb/3.6.4/bin/mongo`, or
  * `mongo --host 127.0.0.1:27017`
