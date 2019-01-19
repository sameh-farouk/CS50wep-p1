if __name__ == '__main__':
    # activating the application's virtual env
    activate_this_file = "venv/bin/activate_this.py"
    exec(open(activate_this_file).read(), {'__file__': activate_this_file})

    from application import app

    app.run(host='0.0.0.0')
