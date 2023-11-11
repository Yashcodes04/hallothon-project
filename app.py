# from flask import Flask, render_template
# from functions import test1, test2
from flask import Flask, render_template, request
import sympy
import sympy as sp
import scipy.stats as stats
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


app = Flask(__name__)

def hello():
    return "hello"

@app.route('/hello')
def hello():
    return hello()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/options')
def options():
    return render_template('option.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/abc')
def abc():
    return render_template('index.html')

# @app.route('/testing')
# def testing():
    # return render_template('testing.html')
@app.route('/testing', methods=['GET', 'POST'])
def laplace_fuc():
    if request.method == "POST":
        t, s = sympy.symbols('t s')
        Tfunc = request.form['Tfunc']
        f1 = sympy.sympify(Tfunc)
        Laplacef1 = sympy.laplace_transform(f1, t, s, noconds=True)
        result = f'Laplace Transform of {Tfunc} is {Laplacef1}'
        return render_template('testing.html', result=result)
    else:
        return render_template('testing.html')

@app.route('/testing2', methods=['GET', 'POST'])
def inv_lapla():
    if request.method == 'POST':
        Laplace_transform_str = request.form['laplace_transform_input']
        try:
            s, t = sp.symbols('s t')
            Laplace_transform = sp.sympify(Laplace_transform_str)
            inverse_transform = sp.inverse_laplace_transform(Laplace_transform, s, t)
            pretty_inverse_transform = sp.pretty(inverse_transform, use_unicode=True)
            return render_template('testing2.html', result=pretty_inverse_transform)
        except sp.SympifyError:
            return render_template('testing2.html', error_message="Invalid input. Please enter a valid Laplace-transformed function.")
    return render_template('testing2.html')

@app.route('/testing3', methods=['GET', 'POST'])
def taylor():
    if request.method == 'POST':
        func_str = request.form['function_input']
        try:
            x = sympy.symbols('x')
            func = sympy.sympify(func_str)
            n = 20
            x0 = 0

            result = func.subs(x, x0)

            for i in range(1, n):
                result += sympy.diff(func, x, i).subs(x, x0) * (x - x0)**i / sympy.factorial(i)

            return render_template('testing3.html', result=result)
        except sympy.SympifyError:
            return render_template('testing3.html', error_message="Invalid input. Please enter a valid mathematical expression.")
    return render_template('testing3.html')


@app.route('/testing4', methods=['GET', 'POST'])
def poisson():
    lambda_parameter = None
    pmf_values = []
    cdf_values = []
    mean = None
    variance = None

    if request.method == 'POST':
        lambda_parameter = float(request.form['lambda_parameter'])
        poisson_dist = stats.poisson(mu=lambda_parameter)

        for k in range(10):  # You can adjust the range as needed
            pmf_values.append(poisson_dist.pmf(k))
            cdf_values.append(poisson_dist.cdf(k))

        mean = poisson_dist.mean()
        variance = poisson_dist.var()

    return render_template('testing4.html', lambda_parameter=lambda_parameter, pmf_values=pmf_values, cdf_values=cdf_values, mean=mean, variance=variance)

@app.route('/testing5', methods=['GET', 'POST'])
def bino():
    user_function = None
    binomial_expansion = None

    if request.method == 'POST':
        user_function = request.form['user_function']
        try:
            user_expr = sp.sympify(user_function)
            binomial_expansion = sp.expand(user_expr, power_base=True)
        except sp.SympifyError:
            error_message = "Invalid input. Please enter a valid mathematical expression."

    return render_template('testing5.html', user_function=user_function, binomial_expansion=binomial_expansion)


def user_ode(t, y, equation):
    try:
        variables = {'t': t, 'y': y}
        result = eval(equation, variables)
        return result
    except:
        return 0

@app.route('/testing6', methods=['GET', 'POST'])

# ... Your existing code ...

def de():
    equation = None
    initial_t = None
    initial_y = None
    t_values = None
    y_values = None

    if request.method == 'POST':
        equation = request.form['equation']
        initial_t = float(request.form['initial_t'])
        initial_y = float(request.form['initial_y'])
        t_span = (initial_t, initial_t + 10)

        sol = solve_ivp(user_ode, t_span, [initial_y], args=(equation,), t_eval=np.linspace(initial_t, initial_t + 10, 100))
        t_values = sol.t
        y_values = sol.y[0]
    else:
        # Assign a default value in case of a GET request or other cases
        equation = "Default equation"  

    return render_template('testing6.html', equation=equation, initial_t=initial_t, initial_y=initial_y,
                           t_values=t_values, y_values=y_values)


@app.route('/testing7', methods=['GET', 'POST'])
def set_operation():
    set1 = request.form.get('set1', '').split(',')
    set2 = request.form.get('set2', '').split(',')
    choice = request.form.get('choice', '')

    result = None

    if choice:
        result = perform_set_operation(set1, set2, choice)

    return render_template('testing7.html', set1=','.join(set1), set2=','.join(set2), choice=choice, result=result)


if __name__ == '__main__':
    app.run(debug=True)