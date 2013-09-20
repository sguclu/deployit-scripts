Sample for directory tree rights propagation:

path='path/to/the/application'
pathelement=path.split("/")
print pathelement
for i in range(len(pathelement)):
  if (i>0):  pathelement[i]=pathelement[i-1]+'/'+pathelement[i]
print pathelement
