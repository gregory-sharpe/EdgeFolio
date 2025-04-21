# # check_performance_flags.py

# import inspect
# from utils.flags import potential_performance_flag
# # Import your models or any other classes you want to check

# # Import the decorator to search for it


# @potential_performance_flag
# def Testing():
#     print("test")


# def check_performance_flags():
#     flagged_methods = []

#     # Loop over all classes in the project (or specific classes)
#     for cls_name, cls in globals().items(): # shouldn't be globals().items
#         print(cls_name)
#         if isinstance(cls, type):  # Only check classes
#             # Loop through methods in the class
#             for name, method in inspect.getmembers(cls):
#                 if callable(method) and hasattr(method, 'potential_performance_flag'):
#                     if method.is_flagged_for_performance_check:
#                         flagged_methods.append((cls_name, name))

#     # Output the methods flagged for performance
#     if flagged_methods:
#         print("Methods flagged for performance checks:")
#         for cls_name, method_name in flagged_methods:
#             print(f"Class: {cls_name}, Method: {method_name}")
#     else:
#         print("No methods flagged for performance issues.")


# # Run the performance check script
# check_performance_flags()
