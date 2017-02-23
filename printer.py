import uuid


def printer(caches, input_filename):
    f = open('out_' + input_filename + "_" + str(uuid.uuid4()) + '.txt', 'w')
    length = len(caches)
    f.write(str(length) + '\n')
    for cache in caches:
        for videos in cache:
            s = str(videos)
            f.write(s + ' ')
        f.write('\n')
    f.close()
