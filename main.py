import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import cv2
import smtplib


wikipedia.set_lang('es')
listener = sr.Recognizer()
name = "juana"
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice',voices[2].id)

def talk (some_text):
    engine.say(some_text)
    engine.runAndWait()

def send_email(to, subject, body):
    conexion = smtplib.SMTP(host='smtp.gmail.com', port=587)
    conexion.ehlo()
    conexion.starttls()
    conexion.login(user='PruebaasistentePA@gmail.com', password='asistentevirtual123')
    message = f'Subject: {subject}\n\n{body}'
    conexion.sendmail(from_addr='PruebaasistentePA@gmail.com', to_addrs=to, msg=message)
    conexion.quit()

def listen():

    try:    #Usar el microfono como fuente de info
        with sr.Microphone() as source:
            print("Si, te estoy escuchando")
            #Limpie sonido ambiente
            listener.adjust_for_ambient_noise(source)
            #obtener el audio
            audio = listener.listen(source)
            #reconocer
            rec = listener.recognize_google(audio, language="es")
            rec = rec.lower()
    except sr.UnknownValueError:
        print("Disculpa, no te entendi, vuelve a hablar...")

    return rec

def run_juana():
    while True:
        try:
            rec = listen()

        except UnboundLocalError:
            talk("Disculpa, no te entendi, vuelve a hablar")
            continue
        if name in rec:
            rec = rec.replace(name, '').strip()
            if 'reproduce' in rec:
                song = rec.replace('reproduce', '').strip()
                pywhatkit.playonyt(song)
                talk(f"Se esta reproduciendo {song}.")
            elif 'time' in rec:
                time = datetime.datetime.now().strftime('%I:%M %p')
                talk('Son las ' + time)
            elif 'wikipedia' in rec:
                rec = rec.replace('wikipedia', '')
                info = wikipedia.summary(rec, sentences=1)
                talk(f"Wikipedia dice, ' {info}")
            elif 'google' in rec:
                webbrowser.open('https://www.google.com/?hl=es')
            elif 'foto' in rec:
                cap = cv2.VideoCapture(0)
                leido, frame = cap.read()
                if leido == True:
                    cv2.imwrite("foto.png", frame)
                    print("Foto tomada correctamente")
                else:
                    print("Error al acceder a la cámara")
                cap.release()
            elif 'correo' in rec:
                    talk('Destinatario')
                    to = input('Para: ')
                    talk('Asunto')
                    subject = input('dime el asunto:' )
                    talk('Cuerpo del correo')
                    body = input('Cuerpo del correo: ')
                    send_email(to, subject, body)
                    talk('Enviado')
if __name__ == '__main__':
    run_juana()