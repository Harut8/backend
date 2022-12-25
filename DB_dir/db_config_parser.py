# class ConfigParser:
#
#     @classmethod
#     def get_configs(cls):
#         cls.configs = dict()
#         with open('db_configs.txt') as configs:
#             for line in configs:
#                 key, value = line.strip().split('=')
#                 cls.configs[key] = value
#         print("CONFIGS CREATED")
#         return True
#
#
