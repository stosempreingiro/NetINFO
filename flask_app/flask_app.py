from flask import Flask
from net_info import Output
from flask import render_template,redirect,request
from net_info import check_input_ip,subnet_decimal

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    try:
        if request.method=="POST":
            user_input=request.form["user_input"]
            if user_input=="":
                return redirect("/")
            else:
                if check_input_ip(user_input):
                    output_list=subnet_decimal(user_input,info="all")
                    output=Output(output_list[0],output_list[1],output_list[2],output_list[3],output_list[4])
                    return render_template("index.html",output=output)
                else:
                    input_error="Input Error. Try Again."
                    return render_template("index.html",error=input_error)
        else:
            return render_template("index.html")
    except:
        return redirect("/")
    
if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)