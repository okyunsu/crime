from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
from com.okyunsu.models.cctv.cctv_controller import CctvController



@app.route("/")
def index():
    
    controller = CctvController()
    controller.modeling("cctv_in_seoul.csv","crime_in_seoul.csv",
                        "pop_in_seoul.xls")

    return render_template("index.html")

@app.route("/titanic") 
def titanic():
    pass



if __name__ == '__main__':  
    app.run('0.0.0.0',port=5000,debug=True)

app.config['TEMPLATES_AUTO_RELOAD'] = True  
 