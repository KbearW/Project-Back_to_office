from flask import Flask, render_template, session, request

app = Flask(__name__)
app.secret_key = "blahhhhhhhh"

@app.route('/')
def show_homepage():
    return render_template('homepage.html')


@app.route('/form')
def show_form():
    return render_template('form.html')


@app.route('/results')
def show_results():
    cheery = request.args.get('cheery')
    honest = request.args.get('honest')
    dreary = request.args.get('dreary')
    
    if cheery and honest and dreary:
        msg = "Hm, that's a tall order"
    elif cheery and honest and not dreary:
        msg = "Here's a cheery and honest message: You're cool!"
    elif cheery and dreary and not honest:
        msg = "Cheery AND dreary? Be careful what you wish for. It just might come true."
    elif dreary and honest:
        msg = "All good things must come to an end."
    elif not dreary and not honest and cheery:
        msg = "Unicorns are real!"
    elif not honest and not cheery:
        msg = "All fun activities have been cancelled for the day."
    else:
        msg = "You will find what you've been looking for."

    return render_template('results.html', msg=msg)

@app.route('/save-name', methods=["POST"])
def save_name():
    name = request.form.get('name')
    session['name'] = name
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
