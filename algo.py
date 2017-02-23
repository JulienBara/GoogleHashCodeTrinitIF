from parser import parser


def algo():
    a = parser()
    print(a)

def dumb_solution():
    endpoints, videos, number_of_caches, caches_capacity = parser()

    nb_caches = 0
    cache_size = 0
    videos = {}
    solution = []

    for cache_id in range(0, nb_caches):
        left = cache_size
        solution.add([])
        while (left > 0):
            for video_id, video_size in videos:
                if video_size <= left:
                    solution[cache_id].add(video_id)
                    left = left - video_size
    return solution




if __name__ == "__main__":
    solution = dumb_solution()
    print(solution)
