import collections

n = input()
customers = list(map(int,input().split()))
leader, member = map(int, input().split())
result = 0

for i in customers:
    done = i
    done -= leader
    result += 1
    if not done:
        done = done // member +1
        result += done

print(result)