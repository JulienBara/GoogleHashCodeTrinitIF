def printer(caches):
	f = open('out.txt', 'w')
	length = len(caches)
	f.write(str(length)+'\n')
	for cache in caches:
		for videos in cache:
			s = str(videos)
			f.write(s+' ')
		f.write('\n')
	f.close()


if __name__ == "__main__":
    printer()