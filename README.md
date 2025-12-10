## QR 2 model

This is a simple program which takes a message from a user and procedes to generate a QR code from message. 
The message is then taken from the QR object and is progrimatically constructed using numpy-stl to generate 
a mesh which can be 3d printed.  

## How to Run

#### Python

1)  setup the virtual env
```
python3 -m venv env
```

2) activate the environment

```
source env/bin/activate
```

3) install the requirements

```
pip install -r requirements.txt
```

4) start fast api 

```
fastapi run app/app.py --port 80
```

#### Podman

I didn't publish this, so the image would need to be built locally in the repo 

```
podman build . -t qr2model:latest
```

```
podman run -dp 8080:80 qr2model:latest
```


## Application Usage

On the web browser page, there is a simple form with the following properties:

| Property   | Usage                                               | Default        |
| ---------- | --------------------------------------------------- | -------------- |
| size       | the width & height of a square in the qr code       | 1              |
| depth      | the depth of a square which is false in the qr code | 1              |
| true_depth | the depth of a square which is true in the qrcode   | 1              |
| message    | the message to be encoded                           | Required Field |

After the form is submitted. an STL blob should be automatically downloaded onto your computer. This should be able imported in various slicers or modeling software.  Enjoy messing around with this application!
