# -*- coding: utf-8 -*-
"""archon_query.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MjxPdQkhWjJzvn-bL3pioeeQ4YA-CERo
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install python-osc
import numpy as np
import json as json
import os, os.path
import argparse
import math
from scipy.spatial.distance import pdist
import pythonosc

from pythonosc import dispatcher
from pythonosc import osc_server

destination_db = "/content/drive/My Drive/IRCMS_GAN_collaborative_database/Experiments/colab-violingan/archon-analysis/" #@param {type:"string"}

analysis_filename = "/content/drive/My Drive/analysis_500ms.json" #@param {type:"string"}
trial_filename = "/content/drive/My Drive/trial.json" #@param {type:"string"}

## IMPORT JSON FILE
def json_load (filename):
  f = open(filename)
  l = json.load(f)
  return l

def closest_node(input_db, comparative_db):

    in_ = json_load(input_db)
    db_ = json_load(comparative_db)

    flatscl = 100000.0
    min_ = "init"
    result_ = "error"

    for k, v in in_.items():

      sample = v

      pitch = str(sample.get("pitch"))

      in_metrics = [
              float(
                  sample.get("cent")), 
              float(
                  sample.get("flat")) * flatscl, 
              float(
                  sample.get("rolloff"))]


    for k, v in db_.items():

        sample_ = v
        if (pitch == sample_.get("pitch")):

          db_metrics = [
                float(
                    sample_.get("cent")), 
                float(
                    sample_.get("flat")) * flatscl, 
                float(
                    sample_.get("rolloff"))]
          dist = pdist([in_metrics, db_metrics], metric = 'euclidean')[0]

          if (min_ == "init"): min_ = dist
          if (dist < min_):
            min_ = dist
            result_ = ("distance: " + str(dist) + ", file: " + k)
    
    return result_

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/filter", print)
  dispatcher.map("/volume", print_volume_handler, "Volume")
  dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()

  x = closest_node(trial_filename, analysis_filename)
print(x)