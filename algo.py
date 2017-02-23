from parser import parser
from printer import printer

filename = "videos_worth_spreading.in"


def dumb_solution():
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


if __name__ == "__main__":
    solution = dumb_solution()
    # print(solution)
    printer(solution, filename)
