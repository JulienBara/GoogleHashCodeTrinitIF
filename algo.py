from parser import parser


def algo():
    a = parser()
    print(a)

def dumb_solution():
    endpoints, videos, nb_caches, cache_size = parser("kittens.in")

    solution = []

    for cache_id in range(0, nb_caches):
        left = cache_size
        solution.append([])
        while (left > 0):
            for video_id, video_size in videos.items():
                if int(video_size) <= left:
                    solution[cache_id].append(video_id)
                    left = left - int(video_size)
    return solution




if __name__ == "__main__":
    solution = dumb_solution()
    print(solution)
