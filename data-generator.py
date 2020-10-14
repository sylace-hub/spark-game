# socket-data-generator.py                                                                                                        

#!/usr/bin/env python

import socket
import random,time

from datetime import datetime

HOST = '172.31.33.143'  # Standard loopback interface address (localhost)
PORT = 9998         # Port to listen on (non-privileged ports are > 1023)n=0
i=0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    n = 0
    with conn:
	print('Connected by', addr)
        while True:
            n = n + 1
            i = i + random.choice([-1,1])
            # Send bytes, need to decoded
            message = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
            message = message + "\n"
            # print(message)
            conn.sendall(bytes(message, 'utf-8'))
            time.sleep(1 / 100)
            if n == 1000000:
                break


"""
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

df_stream = spark \
	.readStream \
	.format("socket") \
	.option("host", "172.31.33.143") \
	.option("port", 9998) \
	.load()

messageDecoded = df_stream.selectExpr("CAST(value AS STRING)")

query = messageDecoded \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()
"""


# Le nouveau Spark Structured Streaming
# Peut se connecter à un flux TCP

# Time window Average
# Agréger toutes le secondes ou les dix secondes
