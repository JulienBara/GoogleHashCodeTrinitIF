from parser import parser
from printer import printer
from score import score


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
        endpoint = endpoints[id_endpoint]
        for id_cache, latency in endpoint["caches"]:
            if caches[id_cache] > videos[id_video]:
                caches[id_cache] -= videos[id_video]
                solution[id_cache].add(id_video)
                break

    for i in range(len(solution)):
        solution[i] = list(solution[i])

    return solution


if __name__ == "__main__":
    filenames = ["kittens.in", "me_at_the_zoo.in", "trending_today.in", "videos_worth_spreading.in"]
    max_score = 0
    solution = {}
    while(True):
        sum_score = 0
        for filename in filenames:
            endpoints, videos, nb_caches, cache_size, all_requests = parser(filename)
            solution[filename] = better_solution(filename, endpoints, videos, nb_caches, cache_size, all_requests)
            this_score = score(endpoints, solution)
            print(this_score)
            sum_score = sum_score + this_score
            
        if(sum_score > max_score):
            max_score = sum_score
            print(max_score)
            printer(solution, filename)
    print(max_score)