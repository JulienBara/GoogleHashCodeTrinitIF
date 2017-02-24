# Printer

import uuid


def printer(caches, input_filename):
    f = open('out_' + input_filename + '.txt', 'w')
    length = len(caches)
    f.write(str(length) + '\n')
    for i, cache in enumerate(caches):
        f.write(str(i) + " " + " ".join([str(a) for a in cache]))
        f.write('\n')
    f.close()


# Score

def score(endpoints, solution_data_structure):

    partial_num = 0
    partial_denum = 0

    for i, s in enumerate(solution_data_structure):
        solution_data_structure[i] = set(s)

    for endpoint in endpoints:
        for request in endpoints[endpoint]["requests"]:
            (video_id, nb_of_requests) = request
            possible_server = list()
            possible_server.append(endpoints[endpoint]["latency_datacenter"])
            for cache in endpoints[endpoint]["caches"]:
                (id_cache, latency_of_cache_to_the_endpoint) = cache
                if video_id in solution_data_structure[id_cache]:
                    possible_server.append(latency_of_cache_to_the_endpoint)
            minimum_latency = min(possible_server)
            time_saved = endpoints[endpoint]["latency_datacenter"] - minimum_latency
            partial_num += nb_of_requests * time_saved
            partial_denum += nb_of_requests

    score = partial_num / partial_denum
    score *= 1000

    return int(score)


# Parser

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


# if __name__ == "__main__":
#     parser("kittens.in")

# Algo

# from parser import parser
# from printer import printer
# from score import score
from random import randint
from random import shuffle


def dumb_solution(filename):
    endpoints, videos, nb_caches, cache_size, _ = parser(filename)
    solution = []

    for cache_id in range(0, nb_caches):
        left = cache_size
        solution.append([])

        for video_id, video_size in videos.items():
            if int(video_size) <= left:
                solution[cache_id].append(video_id)
                left -= int(video_size)
    return solution


def better_solution(filename, endpoints, videos, nb_caches, cache_size, all_requests):
    solution = []
    caches = {i: cache_size for i in range(nb_caches)}

    for _ in range(nb_caches):
        solution.append(set())

    for id_endpoint, nb_req, id_video in all_requests:
        nb = randint(0, len(endpoints) - 1)

        endpoint = endpoints[nb]
        for id_cache, latency in endpoint["caches"]:
            if caches[id_cache] > videos[id_video]:
                caches[id_cache] -= videos[id_video]
                solution[id_cache].add(id_video)
                break

    for i in range(len(solution)):
        solution[i] = list(solution[i])

    return solution


def better_better_solution(filename):
    endpoints, videos, nb_caches, cache_size, all_requests = parser(filename)
    solution = []
    caches = {i: cache_size for i in range(nb_caches)}

    endpoints_ordered = list(endpoints.values())

    for _ in range(nb_caches):
        solution.append(set())

    shall_we_go_on = True
    while shall_we_go_on:
        shall_we_go_on = False
        endpoints_ordered.sort(key=lambda x: -x["requests"][0][1] if x["requests"] else -1)
        for i, endpoint in enumerate(endpoints_ordered):
            if not endpoint["requests"]:
                continue
            if len(endpoint["requests"]) == 1:
                id_video, _ = endpoint["requests"][0]
            else:
                id_video, _ = endpoint["requests"][randint(0, 1)]
            for id_cache, _ in endpoint["caches"]:
                if caches[id_cache] > videos[id_video]:
                    solution[id_cache].add(id_video)
                    caches[id_cache] -= videos[id_video]
                    endpoints_ordered[i]["requests"] = endpoints_ordered[i]["requests"][1:]
                    shall_we_go_on = True
                    break

    for i in range(len(solution)):
        solution[i] = list(solution[i])

    return solution, endpoints


def rand_solution(filename):
    endpoints, videos, nb_caches, cache_size, all_requests = parser(filename)
    solution = []
    caches = {i: cache_size for i in range(nb_caches)}

    endpoints_shuffled = list(endpoints.values())

    for _ in range(nb_caches):
        solution.append(set())

    shall_we_go_on = True
    while shall_we_go_on:
        shall_we_go_on = False
        shuffle(endpoints_shuffled)

        for i, endpoint in enumerate(endpoints_shuffled):
            if not endpoint["requests"]:
                continue
            else:
                id_video, _ = endpoint["requests"][randint(0, len(endpoint["requests"])-1)]
            shuffle(endpoint["caches"])
            for id_cache, _ in endpoint["caches"]:
                if caches[id_cache] > videos[id_video]:
                    solution[id_cache].add(id_video)
                    caches[id_cache] -= videos[id_video]
                    endpoints_shuffled[i]["requests"] = endpoints_shuffled[i]["requests"][1:]
                    shall_we_go_on = True
                    break

    for i in range(len(solution)):
        solution[i] = list(solution[i])

    return solution, endpoints




if __name__ == "__main__":
    filenames = ["kittens.in", "me_at_the_zoo.in", "trending_today.in", "videos_worth_spreading.in"]
    maxscores = {f: -1 for f in filenames}
    for i in range(1000):
        print("i = " + str(i))
        for filename in filenames:
            solution, endpoints = rand_solution(filename)
            nowscore = score(endpoints, solution)
            if nowscore > maxscores[filename]:
                print("new best score for " + filename + " is " + str(nowscore))
                maxscores[filename] = nowscore
                printer(solution, filename)

    # maxscore = -1
    # filename = "kittens.in"
    # for i in range(20):
    #     print("i = " + str(i))
    #     solution, endpoints = rand_solution(filename)
    #     nowscore = score(endpoints, solution)
    #     if nowscore > maxscore:
    #         print("new best score for " + filename + " is " + str(nowscore))
    #         maxscore = nowscore
    #         printer(solution, filename)


