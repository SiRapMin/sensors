## Fix it problem in the future:
* Overtrain Net
* Analyze value of Ultraviolet

## Sensor Program and Artificial Vision with Tensorflow(CO2, Humidity, Temperature, TPOC)

### Some data will be recolected from diferents environments using environmental sensors to check some variables as CO2, humidity, temperature, pH, ultraviolet like some other gases.<br>

**Note:**

*_Dataset for Entrenate Model could be downloaded of this repository https://drive.google.com/drive/folders/1ISauTzslU2SmAfkqp_hcklumDV5piaXu?usp=sharing_*

Python Libraries needed:<br>
```
pip install -r requirements.txt
```

Requirements:<br>
* Put the serial port you will use in the in the arduinoPort variable inside the conectarArduino procedure, by this way the data will be read from the avaible port from your computer.<br>
* Serial port needs to be free to make sure that data will be write correctly.
* Have the [mongoCredentials.json](https://drive.google.com/file/d/1H0q1zoWg0-hLZHG9_GzQtTtOU7AyInSj/view?usp=sharing) in the project root directory to access the MongoDB Cloud Database.
