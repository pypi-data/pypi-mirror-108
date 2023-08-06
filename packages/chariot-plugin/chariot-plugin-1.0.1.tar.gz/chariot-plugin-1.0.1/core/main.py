import os
import sys
import argparse


from .tasks import generate, run, http, test as tasks_test


"""
入口
"""



def cmdline():

    parser = argparse.ArgumentParser(description="插件生成器")


    parser.add_argument("-g", "--generate", help="插件生成", action="append")
    parser.add_argument("-r", "--run", help="运行action", action="append")
    parser.add_argument("--http", help="启动api接口", action="store_true")
    parser.add_argument("-t", "--test", help="测试", action="append")



    args = parser.parse_args()

    if args.generate:
        yml = (args.generate)[0]

        generate(os.getcwd(), yml)

    elif args.run:

        path = os.getcwd()
        tests_path = args.run[0]

        run(path, tests_path)

    elif args.http:

        path = os.getcwd()

        http(path)

    elif args.test:

        path = os.getcwd()
        tests_path = args.test[0]

        tasks_test(path, tests_path)








