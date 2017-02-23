from parser import parser
from printer import printer



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


def better_solution(filename):
    endpoints, videos, nb_caches, cache_size, all_requests = parser(filename)
    solution = []
    caches = {i: cache_size for i in range(nb_caches)}

    for _ in range(nb_caches):
        solution.append(set())

    for id_endpoint, nb_req, id_video in all_requests:
        endpoint = endpoints[id_endpoint]
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
        endpoints_ordered.sort(key=lambda x: -x["requests"][0][1])
        for i, endpoint in enumerate(endpoints_ordered):
            if not endpoint["requests"]:
                continue
            id_video, _ = endpoint["requests"][0]
            for id_cache, _ in endpoint["caches"]:
                if caches[id_cache] > videos[id_video]:
                    solution[id_cache].add(id_video)
                    caches[id_cache] -= videos[id_video]
                    endpoints_ordered[i]["requests"] = endpoints_ordered[i]["requests"][1:]
                    shall_we_go_on = True
                    break

    for i in range(len(solution)):
        solution[i] = list(solution[i])

    return solution


if __name__ == "__main__":
    filenames = ["kittens.in", "me_at_the_zoo.in", "trending_today.in", "videos_worth_spreading.in"]
    for filename in filenames:
        solution = better_better_solution(filename)
        printer(solution, filename)
