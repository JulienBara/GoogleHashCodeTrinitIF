import os


def parser(filename):
    endpoints = {}
    videos = {}

    with open(os.path.join("inputs", filename)) as f:
        lines = f.readlines()

    V, E, R, number_of_caches, caches_capacity = [int(i) for i in lines[0].split()]
    sizes = [int(i) for i in lines[1].split()]
    for i in range(V):
        videos[i] = sizes[i]

    lines = lines[2:]

    j = 0
    for i in range(E):
        latency, nb_of_caches = [int(a) for a in lines[j].split()]
        j += 1
        endpoints[i] = {
            "latency_datacenter": latency,
            "caches": [],
            "requests": []
        }
        for k in range(nb_of_caches ):
            id_cache, latency_cache = [int(a) for a in lines[j+k].split()]
            endpoints[i]["caches"].append((id_cache, latency_cache))
        j += nb_of_caches

    lines = lines[j:]
    for i in range(R):
        video_id, endpoint_id, nb_of_requests = [int(a) for a in lines[i].split()]
        endpoints[endpoint_id]["requests"].append((video_id, nb_of_requests))

    for i in range(E):
        endpoints[i]["requests"].sort(key=lambda x: -x[1])
        endpoints[i]["caches"].sort(key=lambda x: x[1])

    all_requests = []
    for id_endpoint, value in endpoints.items():
        all_requests += [(id_endpoint, r[1], r[0]) for r in value["requests"]]
    all_requests.sort(key=lambda x: (-float(x[1]), videos[x[2]]))  # nb_req then size_of_video

    return endpoints, videos, number_of_caches, caches_capacity, all_requests


if __name__ == "__main__":
    parser("kittens.in")
