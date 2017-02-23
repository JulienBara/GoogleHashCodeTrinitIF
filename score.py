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


