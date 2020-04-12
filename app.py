from flask import Flask, request, render_template
import txt2img
import pixel

import io

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def start():
    error = None
    if request.method == 'POST':
        inpt = request.form['letters']
        print(inpt)
        imgdir = txt2img.converter(inpt)
        print(imgdir)
        pixel.match(imgdir)
        # we're gonna end up returning... vectors shapes? downloaded STL files?
        return inpt


    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html', error=error)
