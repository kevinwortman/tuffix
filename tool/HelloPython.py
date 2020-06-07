import pwd, grp
for p in pwd.getpwall():
    print (p[0], grp.getgrgid(p[3])[0])
