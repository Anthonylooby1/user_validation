from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "Vollstin"
DATABASE = 'login_validation'