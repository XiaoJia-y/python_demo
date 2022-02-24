
# import asyncio
 
# async def coroutine_example():
#     for i in range(10):
#         await asyncio.sleep(1)
#         print('zhihu ID: Zarten')
 
# async def coroutine_example1():
#     for j in range(10):
#         await asyncio.sleep(0.5)
#         print("hello")

# loop = asyncio.get_event_loop()
# tasks = [loop.create_task(coroutine_example('Zarten_' + str(i))) for i in range(3)]

# coro = coroutine_example()
# )
# loop.run_until_complete(coro)
# loop.close()
def test1():
    x = 1
global x
y = x
def test():
    global x
    print(x)
test()