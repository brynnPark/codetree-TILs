import collections

n = input()
customers = list(map(int,input().split()))
leader, member = map(int, input().split())
result = 0

for i in customers:
    done = i
    done -= leader
    result += 1
    #print(done)
    if done > 0:
        if not done%member:
            done = done // member
        else:
            done = done // member +1
        result += done

print(result)