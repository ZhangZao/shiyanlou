#!/usr/bin/env python3
from multiprocessing import Process, Queue
import sys
import csv

q1 = Queue()
q2 = Queue()

class Config:

    def __init__(self, conf_file):

        self._configdata = {}
        with open(conf_file, 'r') as f:
            for line in f:
                pair = line.split('=')
                ins_name = pair[0].strip()
                ins_value = float(pair[1].strip())
                self._configdata[ins_name] = ins_value                
    def get_configdata(self):
        return self._configdata

class UserData:

    def __init__(self, user_file):

        self._short_table = {}
        self._long_table = {}

        with open(user_file) as f:
            data = list(csv.reader(f))
            for line in data:
                work_id = int(line[0])
                salary = line[1]
                self._short_table[work_id] = salary

    def get_short_table(self):
        return self._short_table

    def compute(self, configdata):

        for work_id in self._short_table.keys():

            salary = float(self._short_table[work_id])
            insurance = 0
            totax = 0
            tax = 0
            income = 0
            sec_rate = 0
            outputline = []

            for sec_name in configdata.keys():
                if sec_name != 'JiShuH' and \
                    sec_name != 'JiShuL':
                    sec_rate += configdata[sec_name]

            if salary > configdata['JiShuH']:
                insurance = configdata['JiShuH'] * sec_rate
            elif salary > configdata['JiShuL']:
                insurance = salary * sec_rate
            else:
                insurance = configdata['JiShuL'] * sec_rate

            totax = salary - insurance - 3500

            if totax > 80000:
                tax = totax * .45 - 13505
            elif totax > 55000:
                tax = totax * .35 - 5505
            elif totax > 35000:
                tax = totax * .3 - 2755
            elif totax > 9000:
                tax = totax * .25 - 1005
            elif totax > 4500:
                tax = totax * .2 - 555
            elif totax > 1500:
                tax = totax * .1 - 105
            elif totax > 0:
                tax = totax * .03
            else:
                tax = 0

            income = salary - insurance - tax
            salary = int(salary)
            insurance = '{:.2f}'.format(round(insurance,2))        
            tax = '{:.2f}'.format(round(tax,2))
            income = '{:.2f}'.format(round(income,2))    

            outputline.append(work_id)
            outputline.append(salary)
            outputline.append(insurance)
            outputline.append(tax)
            outputline.append(income)

            self._long_table[work_id] = outputline

    def write_data(self, output_file):
        for work_id in self._long_table.keys():
            with open(output_file,'w') as f:
                csv.writer(f).writerow(self._long_table[work_id])

def readuser(user_file, q1):
    userdata = UserData(user_file)
    q1.put(userdata)    

def compute(conf_file, q1, q2):
    userdata = q1.get()
    config = Config(conf_file)
    configdata = config.get_configdata()
    userdata.compute(configdata)
    q2.put(userdata)

def outputdata(output_file,q2):

    userdata = q2.get()
    userdata.write_data(output_file)

def main():
    args = sys.argv[1:]
    conf_file_index = args.index('-c') + 1
    conf_file = args[conf_file_index]

    user_file_index = args.index('-d') + 1
    user_file = args[user_file_index]

    output_file_index = args.index('-o') + 1
    output_file = args[output_file_index]    

    proc_readuser = Process(target=readuser, args=(user_file, q1))
    proc_compute = Process(target=compute, args =(conf_file, q1, q2))
    proc_outputdata = Process(target=outputdata, args = (output_file, q2))

    proc_readuser.start()
    proc_compute.start()
    proc_outputdata.start()

if __name__ == '__main__':
    main()
