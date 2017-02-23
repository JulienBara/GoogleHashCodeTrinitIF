import uuid


def printer(caches, input_filename):
    f = open('out_' + input_filename + "_" + str(uuid.uuid4()) + '.txt', 'w')
    length = len(caches)
    f.write(str(length) + '\n')
    for i, cache in enumerate(caches):
        f.write(str(i) + " " + " ".join([str(a) for a in cache]))
        f.write('\n')
    f.close()
