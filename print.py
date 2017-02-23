def print(caches):
	f = open('out.txt', 'w')
	len = len(caches)
	f.write(str(len)+'\n')
	for cache in caches:
		for videos in cache:
			s = str(videos)
			f.write(s+' ')
		f.write('\n')
	f.close()


if __name__ == "__main__":
    print()