#!/usr/bin/python
# -*- coding: utf-8 -*-
# Submit Tool v 1.0
import re
import requests
import time
from getpass import getpass

BASE_ADDRESS = 'http://147.46.15.109:9480'
LOGIN_URL = '{}/accounts/login/'.format(BASE_ADDRESS)


def submit(ass):
    upload_url = '{}/assignment/{:02d}/submit' .format(BASE_ADDRESS, ass)
    payload = {}
    with requests.Session() as s:
        while True:  # try login
            username = raw_input('id: ')
            password = getpass('password: ')
            s.get(LOGIN_URL)
            csrftoken = s.cookies['csrftoken']

            payload['username'] = username
            payload['password'] = password
            payload['csrfmiddlewaretoken'] = csrftoken

            ret = s.post(LOGIN_URL, data=payload)
            if ret.url == LOGIN_URL:
                print "login failure"
            else:
                break

        # upload file
        ret = s.get(upload_url)
        csrftoken = s.cookies['csrftoken']
        payload['csrfmiddlewaretoken'] = csrftoken
        path = '{:02d}/submission.zip'.format(ass)
        try:
            submission = open(path, 'rb')
        except IOError:
            try:
                submission = open('submission.zip', 'rb')
            except:
                print "try make submission first"
                return
        f = {'submitted_file': submission}
        ret = s.post(upload_url, files=f, data=payload)
        f.close()

        # get current submission number
        se = re.search("(/submission/)(\d+)", ret.text)
        submit_num = int(se.group(2))

        # wait for results
        result_page = '{}/submission/{}'.format(BASE_ADDRESS, submit_num)
        while True:
            print("grading...")
            ret = s.get(result_page)
            state = re.search("Status: ([A-Z ]+)", ret.text).group(1)
            if state != "RUNNING":
                result = re.search("Score: \d+/\d+", ret.text).group()
                print state
                print result
                return
            time.sleep(2)


def main():
    ass = input("assignment number: ")
    submit(ass)
if __name__ == '__main__':
    main()
