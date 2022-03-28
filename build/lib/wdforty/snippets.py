# Check md5s
localDic = {}
with open('localCheck') as f:
    for line in f:
        hashstr = line.strip().split('  ')[0]
        filestr = line.strip().split('  ')[1]
        localDic[filestr] = hashstr
with open('posaCheck') as f:
    for line in f:
        hashstr = line.strip().split('  ')[0]
        filestr = line.strip().split('  ')[1]
        if filestr not in localDic:
            print("{} missing")
        else:
            if localDic[filestr] != hashstr:
                print("{} wrong"
                