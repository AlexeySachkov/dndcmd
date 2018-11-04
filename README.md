# D&D command line interface

[![Build Status](https://travis-ci.com/AlexeySachkov/dndcmd.svg?branch=master)](https://travis-ci.com/AlexeySachkov/dndcmd)

During "online" D&D sessions we use [roll20][roll20] in our party...but it is hard to setup a nice and
full-featured script to automate calculating attack and damage rolls. And anyway: you can
track status of the your character in any tool including pen and paper.

So, I decided to create a simple command line application which allows me to track status
of the my character in D&D: number of Hit Points, Action Points, etc. Also this app should
be able to roll dices and automatically calculate attack and damage based on weapons that my
character is currently wearing.

## Current status

This repo is currently in very initial state: it is almost empty actually.

## TODO-list:

- [ ] Command to print current character status
- [ ] Commands to track damage/ongoing damage/healing surges
- [ ] Emit diagnostic messages for wrong `roll` commands
- [ ] Develop tests for evaluating of `roll` commands
- [ ] Command to roll ability checks
- [ ] Command to roll attacks
- [ ] Describe requirements somehow
- [X] Develop some tests
- [X] Setup some CI to check code style and launch tests

## License

[MIT](LICENSE)




[roll20]: https://roll20.net/
