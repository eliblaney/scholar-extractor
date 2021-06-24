# Scholar Extractor

This simple project scrapes publicly available information about Goldwater scholars from the [official website](https://goldwater.scholarsapply.org).

## Purpose

In building the [Goldwater Scholar Community website](https://goldwatercommunity.org), we wanted to have an easily searchable database of all the scholars to date. Although the website has only tracked scholars since 2006, it will serve as a good start as we begin to import older records.

## Usage

Ensure you have installed Python3 and the required modules: re, requests, bs4, csv. Then you can run the program using:

    python3 main.py

Note that the program will scrape the site by querying each award year page, so please be mindful of network traffic.
