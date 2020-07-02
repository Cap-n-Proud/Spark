//SCMD SerialDebug_ON
//SCMD Motors_ON

int TxLoopTime;

// Commands: READ => Reads value, defaults etc
// SCMD: Set commands


//T: Telemetry
//E: Error
//I: Information
//

void RemoteInit()
{
  //Initialze the headers for the various dictionaries
  //These MUST be in the same order as in RemoteUpload()
  //TH - Telemetry
  //PIDH - PID
  //SYSH - System
  String headers = "";
  headers = "TH" + SEPARATOR +
            "yaw" + SEPARATOR +
            "pitch" + SEPARATOR +
            "roll" + SEPARATOR +
            "heading" + SEPARATOR +
            "info" + SEPARATOR +
            "LoopT";

  Serial.println(headers);/*
  delay(100);
  headers = "PIDH" + SEPARATOR +
            "speedPIDKp" + SEPARATOR +
            "speedPIDKi" + SEPARATOR +
            "speedPIDKd" + SEPARATOR +
            "anglePIDConKp" + SEPARATOR +
            "anglePIDConKi" + SEPARATOR +
            "anglePIDConKd" + SEPARATOR +
            "anglePIDAggKp" + SEPARATOR +
            "anglePIDAggKi" + SEPARATOR +
            "anglePIDAggKd" + SEPARATOR +
            "TriggerAngleAggressive" + SEPARATOR +
            "calibratedZeroAngle" + SEPARATOR +
            "OPT";
  Serial.println(headers);
  delay(100);
  headers =   "SYSH" + SEPARATOR +
              "FirmwareVersion";
  Serial.println(headers);*/
}

void setCommand()
{
  char *arg;
  char *value;
  char *value2;

  arg = SCmd.next();
  value = SCmd.next();
  value2 = SCmd.next();

  //This echoes the command back to confirm it is received correctely
  String cmd = String("SCMD " + String(arg) + " " + String(value) + " " + String(value2));
  Serial.println(cmd);

  if (value != NULL)
  {
    // parameters
    if (String("speedPIDKp").equals(arg)) {
      //configuration.speedPIDKp = atof(value) / 10000;
      delay(5);
      controlConfig();
    }/*
    else if (String("test").equals(arg)) {
      Serial.print("this is a test arg ");
      Serial.println(value);
    }

    else if (String("SerialDebug").equals(arg)) {
      configuration.debug = atoi(value);
    }*/

    else if (String("E_EEPROM").equals(arg)) {
      for (int i = 0; i < 512; i++)
        EEPROM.write(i, 255);

      loadConfig();
      RemoteInit();


    }
    else if (String("SaveCfg").equals(arg)) {
      saveConfig();
    }
    else if (String("Load_def").equals(arg)) {
      setConfiguration((boolean) int(value));

    }

    // steering
    else if (String("SetsteerGain").equals(arg))
      configuration.steerGain = atoi(value) / 100;
    else if (String("SetthrottelGain").equals(arg))
      configuration.steerGain = atoi(value) / 100;

    else if (String("move").equals(arg))
    {

      UserControl[1] =  (atof(value) / 100) * configuration.Maxthrottle;
      UserControl[0] = (atof(value2) / 100) * configuration.Maxsteer;
    }
    else if (String("Steer").equals(arg))
    { //sign * value
      //SCMD Steer 10
      UserControl[0] = (atof(value) / 100) * configuration.Maxsteer;

      //Serial.println(UserControl[0]);
    }
    else if (String("Throttle").equals(arg))
    { //SCMD Throttle 50
      UserControl[1] =  (atof(value) / 100) * configuration.Maxthrottle; //((atof(value))/(atof(value))) * max(abs(atof(value)), configuration.Maxthrottle);

      //Serial.println(UserControl[1]);
    }
    else if (String("MotorsStop").equals(arg))
    { //SCMD MotorsStop 1
      UserControl[1] =  0;
      UserControl[0] =  0;
    }
    else if (String("Maxsteer").equals(arg))
    { //sign * value
      configuration.Maxsteer = atoi(value);
    }
    else if (String("Motorstest").equals(arg))
    { //sign * value
      //SCMD Motorstest 0
      Serial.print("stepsPerRev ");
      Serial.println(configuration.stepsPerRev);
      Serial.print("Rin1Pin ");
      Serial.println(configuration.Rin1Pin);
      /*          Serial.println("testing motors");configuration.Rin2Pin,
                  Serial.println("testing motors");configuration.Rin3Pin,
                    Serial.println("testing motors");configuration.Rin4Pin)
      */    Serial.println("testing motors");

      /*motorR.setSpeed(10);
        motorR.step(50);
        Serial.println("testing LEFT motor");
        motorL.setSpeed(10);
        motorL.step(-50);*/
    }


    else if (String("Maxthrottle").equals(arg))
    { //sign * value
      configuration.Maxthrottle = atoi(value);
    }

    else if (String("maxAcc").equals(arg))
    { //sign * value
      configuration.maxAcc = atoi(value);
    }

    else if (String("debugLevel").equals(arg))
      configuration.debugLevel = atoi(value);
    else if (String("debugSampleRate").equals(arg))
      configuration.debugSampleRate = atoi(value);



    else {

      Serial.print("E, Unknown command ");
      Serial.print(arg);
      Serial.print(" arg ");
      Serial.println(value);
    }


  }
  else {

    Serial.print("E, Unknown command ");
    Serial.println(arg);

  }




}


void RemoteRead() {
  SCmd.readSerial();     // We don't do much, just process serial commands
}


//Transmits the system parmeters. To be called upon initialization event and every time a parameter changes
void SYSParamTX()
{

  String line = "";
  if (!configuration.debug) {
    line = "SYS" + SEPARATOR
           + configuration.FirmwareVersion;

    Serial.println(line);
  }

}


void unrecognizedCMD() {

  Serial.print("E, unrecognized command");

}

//Triggered by READ command
void printCommand() {
  char *arg = SCmd.next();

  //SCMD PIDParamTX
  if (String("PIDParamTX").equals(arg))
    Serial.println("No function defined for this command");
  //PIDParamTX();
  else if (String("RemoteInit").equals(arg))
    RemoteInit();
  else if (String("SYSParamTX").equals(arg))
    SYSParamTX();
  else if (String("printConfig").equals(arg)) {
    Serial.println("DebugCFG");
    Serial.println("Configuration");
    Serial.println("--------------------------------------------------");
    Serial.print("FirmwareVersion "); Serial.println(configuration.FirmwareVersion);
    Serial.print("Rin1Pin "); Serial.println(configuration.Rin1Pin);
    Serial.print("Rin2Pin "); Serial.println(configuration.Rin2Pin);
    Serial.print("Rin3Pin "); Serial.println(configuration.Rin3Pin);
    Serial.print("Rin4Pin "); Serial.println(configuration.Rin4Pin);
    Serial.print("Lin1Pin "); Serial.println(configuration.Lin1Pin );
    Serial.print("Lin2Pin "); Serial.println(configuration.Lin2Pin );
    Serial.print("Lin3Pin "); Serial.println(configuration.Lin3Pin );
    Serial.print("Lin4Pin "); Serial.println(configuration.Lin4Pin );
    Serial.print("stepsPerRev "); Serial.println(configuration.stepsPerRev);
    Serial.print("maxSpeed "); Serial.println(configuration.maxSpeed);
    Serial.print("maxAcc "); Serial.println(configuration.maxAcc);
    Serial.print("steerGain "); Serial.println(configuration.steerGain);
    Serial.print("throttleGain "); Serial.println(configuration.throttleGain);
    Serial.print("Maxsteer "); Serial.println(configuration.Maxsteer);
    Serial.print("Maxthrottle "); Serial.println(configuration.Maxthrottle);

    //ADD HERE OTHER PARAMETERS
    Serial.println("--------------------------------------------------");

  }



}

void TelemetryTX()
{ // for help on dtostrf http://forum.arduino.cc/index.php?topic=85523.0

  String line = "";
  String info = "info";
  if (!configuration.debug) {
    String telemMarker = "T";
    //Need to calculate parameters here because the main loop has a different frequency
    //TxLoopTime = millis() - TxLoopTime;


    line = telemMarker + SEPARATOR +
           String(IMU_Readings.yaw) +  SEPARATOR +
           String(IMU_Readings.pitch) +  SEPARATOR +
           String(IMU_Readings.roll) +  SEPARATOR +
           String(IMU_Readings.heading) +  SEPARATOR +
           String(info) +  SEPARATOR +
           String(LoopT);
    Serial.println(line);

    /*line = "T" + SEPARATOR
           + yaw + SEPARATOR
           + pitch + SEPARATOR
           + roll + SEPARATOR
           + heading + SEPARATOR
           + Info
      //+ SEPARATOR
      //+ LastEvent;*/
    //Serial.println(line);
  }
}


//Transmits the PID parmeters. To be called upon initialization event and every time a parameter changes
/*void PIDParamTX()
  {

  String line = "";
  if (!configuration.debug)
  {
    line = "PID" + SEPARATOR
           + int(configuration.speedPIDKp * 10000)  + SEPARATOR
           + int(configuration.speedPIDKi * 10000) + SEPARATOR
           + int(configuration.speedPIDKd * 10000) + SEPARATOR
           + int(configuration.anglePIDConKp * 100) + SEPARATOR
           + int(configuration.anglePIDConKi * 100) + SEPARATOR
           + int(configuration.anglePIDConKd * 100) + SEPARATOR
           + int(configuration.anglePIDAggKp * 100) + SEPARATOR
           + int(configuration.anglePIDAggKi * 100) + SEPARATOR
           + int(configuration.anglePIDAggKd * 100) + SEPARATOR
           + int(configuration.TriggerAngleAggressive * 100) + SEPARATOR
           + int(configuration.calibratedZeroAngle * 100) + SEPARATOR
           + int(5);
    Serial.println(line);
  }

  }*/

void sendE(const String& E) {
  String line = "";
  String info = "info";
  if (!configuration.debug) {
    String errorMarker = "E";
    line = errorMarker + SEPARATOR +
           String("ERROR") +  SEPARATOR +
           String(E);
    Serial.println(line);

  }
}

void sendI(const String& I) {
  String line = "";
  if (!configuration.debug) {
    String infoMarker = "I";
    line = infoMarker + SEPARATOR +
           String("INFO") +  SEPARATOR +
           String(I);
    Serial.println(line);

  }
}
