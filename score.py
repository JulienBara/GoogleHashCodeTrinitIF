def score(endpoints, solution_data_structure):

    partial_num = 0
    partial_denum = 0

    for endpoint in endpoints:
        for request in endpoint["requests"]:
            (video_id, nb_of_requests) = request
            possible_server = list()
            possible_server.append(endpoint["latency_datacenter"])
            for cache_id, cache in enumerate(solution_data_structure):
                for video in cache:
                    if video == video_id:
                        possible_server.append(endpoint["caches"][cache_id])
            minimum_latency = min(possible_server)
            time_saved = endpoint["latency_datacenter"] - minimum_latency
            partial_num += nb_of_requests * time_saved
            partial_denum += nb_of_requests

    score = partial_num / partial_denum

    return score


