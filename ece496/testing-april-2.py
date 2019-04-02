import requests
import time
from pprint import pprint

container_2_2 = {
    'cpu_query': 'http://142.150.208.216:9090/api/v1/query?query=(sum by (name) (rate(container_cpu_usage_seconds_total{job="cadvisor",name="good_good.1.bpefzdlhdh1xa879nk7yawgt0"}[1m])*100))/7',
    'mem_query': 'http://142.150.208.216:9090/api/v1/query?query=' + 'container_memory_usage_bytes{job="cadvisor",container_label_com_docker_swarm_service_name="good_good"}-container_memory_cache{job="cadvisor",container_label_com_docker_swarm_service_name="good_good"}-container_memory_rss{job="cadvisor",container_label_com_docker_swarm_service_name="good_good"}'
}

container_4_4 = {
    'cpu_query': 'http://142.150.208.216:9090/api/v1/query?query=(sum by (name) (rate(container_cpu_usage_seconds_total{job="cadvisor",name="cpu_ram_scale_cpu_ram_stress.1.skya53j86tenhv27bygslcmze"}[1m])*100))/2',
    'mem_query': 'http://142.150.208.216:9090/api/v1/query?query=container_memory_usage_bytes{job="cadvisor",name="cpu_ram_scale_cpu_ram_stress.1.skya53j86tenhv27bygslcmze"}-container_memory_cache{job="cadvisor",name="cpu_ram_scale_cpu_ram_stress.1.skya53j86tenhv27bygslcmze"}-container_memory_rss{job="cadvisor",name="cpu_ram_scale_cpu_ram_stress.1.skya53j86tenhv27bygslcmze"}'
}

def getMemoryFromPrometheus(container):
    query = container['mem_query']
    r = requests.get(query, auth=('admin', 'admin'))
    requestJson = r.json()
    if requestJson['data']['result']:
        u_value = requestJson['data']['result'][0]['value']
        print "MEMORY: ", u_value[1]
    else:
        print "MEMORY: NO RESULT"

def getCPUFromPrometheus(container):
    query = container['cpu_query']
    r = requests.get(query, auth=('admin', 'admin'))
    requestJson = r.json()
    if requestJson['data']['result']:
        u_value = requestJson['data']['result'][0]['value']
        print "CPU %: ", u_value[1]
    else:
        print "CPU %: NO RESULT"
count = 0

while True:
    print "\n------------ COUNT: {} --------------".format(count)
    print "Container 2_2"
    try:
        getMemoryFromPrometheus(container_2_2)
        getCPUFromPrometheus(container_2_2)
    except NameError:
        print "prometheus calls failing"
        print "most likely due to container scaling"
        print NameError
    print "\nContainer 4_4"
    getMemoryFromPrometheus(container_4_4)
    getCPUFromPrometheus(container_4_4)
    time.sleep(10)
    count += 1