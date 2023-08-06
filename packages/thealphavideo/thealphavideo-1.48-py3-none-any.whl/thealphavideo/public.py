from __main__ import app
from flask import Flask, render_template, request, url_for, flash, redirect, Response, session

@app.route('/')
def index():
    return render_template('public.html')
