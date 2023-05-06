from Count import CountInfo

count_info = CountInfo(name="count")

@count_info.count_time
@count_info.count_memory
def test():
    for i in range(1000):
        a = i * i



def main():
    test()

main()
print(count_info.time_result)
print(count_info.memory_result)
