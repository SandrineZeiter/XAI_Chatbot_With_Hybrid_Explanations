category_ranges = [('bad', range(-15, -9)),
                   ('rather bad', range(-9, -2)),
                   ('average', range(-2, 3)),
                   ('rather good', range(3, 9)),
                   ('good', range(9, 16))
                   ]

categories = {'bad': 1,
              'rather bad': 2,
              'average': 3,
              'rather good': 4,
              'good': 5
              }

rating_all_feelings = {index: categories[key] for index, key in enumerate(categories)}
rating_groups = {'bad': 0, 'rather bad': 1, 'rather good': 2, 'good': 3}

category_ranges_dict = {key: value for key, value in category_ranges}
