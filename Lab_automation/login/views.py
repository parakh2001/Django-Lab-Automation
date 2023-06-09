from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import base64
import csv
import random as rd
from io import BytesIO
import pyvisa as visa
from datetime import datetime, timedelta
from jupyterplot import ProgressPlot
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

# Create your views here.


def HomePage(request):
    return render(request, 'home.html')


def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            return HttpResponse("Passwords don't match")
        else:
            my_user = User.objects.create_user(username, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            messages.success(
                request, f"Hello <b>{user.username}</b>! You have been logged in")
            return redirect('home')
        else:
            return HttpResponse("Incorrect password or Username")
    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('login')


def Equipments(request):
    return render(request, 'Equipments.html')


# def Option_1(request):
#     print("Hello")
#     start = float(request.POST.get('s1') or 0.1)
#     end = float(request.POST.get('s2') or 0.1)
#     value = float(request.POST.get('v') or 0.1)
    # path = open("Readings(x,y).csv", "w")  # open csv file
    # rm = visa.ResourceManager()
    # B2901B = rm.open_resource('USB0::0x2A8D::0x9001::MY60440157::0::INSTR')
    # idn = B2901B.query('*IDN?')
    # print(idn)
    # B2901B.write('*RST')
    # B2901B.write(':OUTPut:STATe %d' % (1))
    # response = dict()
    # values= np.linspace(start, end, value)
    # response={}
    # for i in values:
    #     B2901B.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (i))
    #     B2901B.write(':FORMat:DATA %s' % ('ASCii'))
    #     temp_values = B2901B.query_ascii_values(':MEASure:CURRent:DC?')
    #     response[i]=temp_values
    # #response["V"] = response["V"].append(i)
    # B2901B.write('*RST')
    # z = csv.writer(path)
    # for x, y in response.items():  # write data into csv file
    #     z.writerow([x, y])

    # path.close()
    # df = pd.read_csv('Readings(x,y).csv', header=None)
    # df.rename(columns={0: 'X', 1: 'Y'}, inplace=True)  # header names
    # df.to_csv('Readings(x,y).csv', index=False)
    # # ----PLOTTING----
    # # plt.rcParams["figure.figsize"] = [7.00, 3.50]
    # # plt.rcParams["figure.autolayout"] = True
    # columns = ["X", "Y"]
    # df = pd.read_csv("Readings(x,y).csv", usecols=columns)
    # print("Contents in csv file:\n", df)

    # plt.xlabel('Voltage (v)->')
    # plt.ylabel('Current (I)->')
    # plt.title("IV Graph")
    # plt.plot(df.X, df.Y)
    # plt.plot(response["V"], response["I"])
    # s = BytesIO()
    # plt.savefig(s)
    # b64 = base64.b64encode(s.getvalue()).decode()
    # s_csv= BytesIO()
    # df.to_csv(s_csv)
    # b64_csv = base64.b64encode(s_csv.getvalue()).decode()

    # submitbutton = request.POST.get('Submit')
    # # x = df.to_html()
    # context = {
    #            'image': b64,
    #            #'csv': df.to_html(),
    #            'submitbutton': submitbutton}
    # return render(request, "Option_1.html")


def test(request):
    print("Hello")
    start_value = float(request.POST.get('r1') or 0.1)
    end_value = float(request.POST.get('r2') or 0.1)
    no_step = float(request.POST.get('nv') or 0.1)
    n = float(request.POST.get('n') or 0.1)
    I = float(request.POST.get('I0') or 0.1)
    # return render(request,'test.html')
    #     st2 = int (r2)
    #     st3 = int (nv)
    val = abs(end_value) - abs(start_value)
    stepsize = no_step
    print(start_value)
    # print(stepsize)
    vals = {}  # Empty dictionary for values
    # -----CSV FILE-----
    path = open("Readings(x,y).csv", "w")  # open csv file
    voltage_range = np.arange(-start_value, end_value, stepsize)
    I_ph = 2e-3  # photocurrent in amperes
    I_0 = I  # diode reverse saturation current in amperes
    # n = 1.3  # diode ideality factor
    T = 300  # temperature in Kelvin
    q = 1.602e-19  # electron charge in Coulombs
    k = 1.38e-23  # Boltzmann constant in Joules/Kelvin

# Calculate the current for each voltage using the diode equation

    for i in voltage_range:
        current = I_ph - I_0 * (np.exp(q * i / (n * k * T)) - 1)
        vals[i] = current
    # print(vals)

    z = csv.writer(path)
    for x, y in vals.items():  # write data into csv file
        z.writerow([x, y])

    path.close()
    df = pd.read_csv('Readings(x,y).csv', header=None)
    df.rename(columns={0: 'X', 1: 'Y'}, inplace=True)  # header names
    df.to_csv('Readings(x,y).csv', index=False)
    # ----PLOTTING----
    # plt.rcParams["figure.figsize"] = [7.00, 3.50]
    # plt.rcParams["figure.autolayout"] = True
    columns = ["X", "Y"]
    df = pd.read_csv("Readings(x,y).csv", usecols=columns)
    print("Contents in csv file:\n", df)

    plt.xlabel('Voltage (v)->')
    plt.ylabel('Current (I)->')
    plt.title("IV Graph")
    plt.plot(df.X, df.Y)
#     voltage_range = np.arange(-0.8, 0.8, 0.01)
#     I_ph = 2e-3  # photocurrent in amperes
#     I_0 = 5e-12  # diode reverse saturation current in amperes
#     n = 1.3  # diode ideality factor
#     T = 300  # temperature in Kelvin
#     q = 1.602e-19  # electron charge in Coulombs
#     k = 1.38e-23  # Boltzmann constant in Joules/Kelvin

# # Calculate the current for each voltage using the diode equation
#     current = I_ph - I_0 * (np.exp(q * voltage_range / (n * k * T)) - 1)

# # Plot the IV curve
#     plt.plot(voltage_range, current)
#     plt.title('Solar Cell IV Curve')
#     plt.xlabel('Voltage (V)')
#     plt.ylabel('Current (A)')

    s = BytesIO()
    plt.savefig(s)
    b64 = base64.b64encode(s.getvalue()).decode()
    s_csv = BytesIO()
    df.to_csv(s_csv)
    b64_csv = base64.b64encode(s_csv.getvalue()).decode()

    submitbutton = request.POST.get('Submit')
    # x = df.to_html()
    context = {
        'image': b64,
        # 'csv': df.to_html(),
        'submitbutton': submitbutton}

    return render(request, 'test.html', context)
