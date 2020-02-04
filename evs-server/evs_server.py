#coding=utf-8
from flask import Flask,request,make_response
import Generate_answer
import Create_Knowledge_Base
from bing_speech_api import BingSpeechAPI
import datetime
import Rognition_Service
app = Flask(__name__)
bing = BingSpeechAPI()
kbid = 'f8ac8194-fbb0-4bbd-856f-60aebbb4c92a'

@app.route('/totext/', methods=['POST','GET'])
def totext():
    audio_data = request.get_data()
    text = bing.recognize(audio_data)
    return text

@app.route('/tospeech/', methods=['POST','GET'])
def text_to_speech():
    question = request.form['question']
    #kbid = Create_Knowledge_Base.get_kbId()
    
    answer = Generate_answer.get_answer(kbid,question)
    speech = bing.synthesize(answer, stream=None)
    return speech

@app.route('/speechcommu/',methods=['POST','GET'])
def tospeechcommu():
    starttime = datetime.datetime.now()
    audio_data = request.get_data()
    text = bing.recognize(audio_data)
    #kbid = Create_Knowledge_Base.get_kbId()
    answer = Generate_answer.get_answer(kbid,text)
    speech = bing.synthesize(answer, stream=None)
    resp = make_response(speech)
    resp.headers["SST"] = answer
    endtime = datetime.datetime.now()
    print("time difference:%s" % (endtime-starttime).seconds)
    return resp

if __name__ == '__main__':
    # app.run()
    Rognition_Service.Speech_Recognition()
    app.run(host='0.0.0.0',port='8020')
    
