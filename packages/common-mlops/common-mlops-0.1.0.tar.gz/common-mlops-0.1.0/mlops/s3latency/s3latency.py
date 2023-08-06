#!/usr/bin/env python3

import boto3
import time
from sklearn import linear_model


class S3Latency:
    def __init__(self):
        self.regions = ['us-west-2']

    def put(self, s3, bucketname, key, filename):
        start_time = time.time()
        s3.Bucket(bucketname).put_object(Key=key, Body=open(filename, 'rb'))
        return time.time() - start_time

    def get(self, s3, bucketname, key):
        start_time = time.time()
        s3.Object(bucketname, key).get()['Body'].read()
        return time.time() - start_time

    def delete(self, s3, bucketname, key):
        start_time = time.time()
        s3.Object(bucketname, key).delete()
        return time.time() - start_time

    def latency(self, size=30, verbose=False):
        files = ['1KB', '10KB', '1MB', '10MB']
        runs = 10
        seconds = " seconds"

        # f = open("log", 'w')
        for region in self.regions:
            session = boto3.Session(profile_name='default', region_name=region)
            s3 = session.resource('s3')
            bucketname = 'oceania-' + region
            s3.create_bucket(Bucket=bucketname, CreateBucketConfiguration={'LocationConstraint': region})

            print('-----[', region, ']-----')
            # f.write('-----[%s]-----\n' % region)
            put_latency = {}
            get_latency = {}
            del_latency = {}
            for key, file in enumerate(files):
                averput = averget = averdel = 0
                print('File Size', file)
                # f.write('File Size %s\n' % file)

                for i in range(0, runs):
                    averput += self.put(s3, bucketname, str(key), "mlops/s3latency/" + file)
                average_put_latency = averput / runs
                print("\tAverage PUT latency " + str(average_put_latency) + seconds)
                put_latency[key] = average_put_latency
                # f.write('\tAverage PUT latency %.6f\n' % (averput/runs))

                for i in range(0, runs):
                    averget += self.get(s3, bucketname, str(key))
                average_get_latency = averget / runs
                print("\tAverage GET latency " + str(average_get_latency) + seconds)
                get_latency[key] = average_get_latency
                # f.write('\tAverage GET latency %.6f\n' % (averget/runs))

                for i in range(0, runs):
                    averdel += self.delete(s3, bucketname, str(key))
                average_del_latency = averdel / runs
                print("\tAverage DEL latency " + str(average_del_latency) + seconds)
                del_latency[key] = average_del_latency
                # f.write('\tAverage DEL latency %.6f\n' % (averdel/runs))

            s3.Bucket(bucketname).objects.all().delete()
            s3.Bucket(bucketname).delete()

        # f.close()

        # Regresión lineal.

        # Casteamos los datos.
        x = [[1], [10], [1000], [10000]]
        y_put = [[put_latency[0]], [put_latency[1]], [put_latency[2]], [put_latency[3]]]
        y_get = [[get_latency[0]], [get_latency[1]], [get_latency[2]], [get_latency[3]]]
        y_del = [[del_latency[0]], [del_latency[1]], [del_latency[2]], [del_latency[3]]]

        # Algoritmo de la biblioteca sklearn.
        model_put = linear_model.LinearRegression()
        model_get = linear_model.LinearRegression()
        model_del = linear_model.LinearRegression()

        model_put.fit(x, y_put)
        model_get.fit(x, y_get)
        model_del.fit(x, y_del)

        size_gb = size * 1000000
        ypred_put = model_put.predict([[size_gb]])
        ypred_get = model_get.predict([[size_gb]])
        ypred_del = model_del.predict([[size_gb]])

        # x son los datos.
        # y son los valores deseados.
        # yprev son las predicciones para esos mismos valores (y).

        # Podemos predecir de los tamaños de archivos que no se encuentran en la lista.
        print("Predict for dvc push or S3.upload_to_s3() of file " + str(size) + " GB: " + str(ypred_put) + seconds)
        print("Predict for dvc pull of S3.download_file_to_local_drive() file " + str(size) + " GB: " + str(ypred_get) + seconds)
        print("Predict for dvc rm of S3.delete_file() file " + str(size) + " GB: " + str(ypred_del) + seconds)
