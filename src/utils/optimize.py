# # 使用网格搜索进行超参数调优

# param_grid = {
#     'n_estimators': [10, 50, 100, 200],
#     'max_depth': [None, 10, 15, 20, 30, 40, 50],
#     'min_samples_split': [20, 25, 30, 35, 40, 45, 50],
#     'min_samples_leaf': [20, 25, 30, 35, 40, 45, 50],
# }

# # 统计训练时间
# from datetime import datetime
# start_time = datetime.now()
# grid_search = GridSearchCV(rf, param_grid, cv=cv, scoring='roc_auc', n_jobs=-1)
# grid_search.fit(X_train, y_train)
# end_time = datetime.now()

# print('Training took: ', end_time - start_time)
# print('Best params & Best score', grid_search.best_params_, grid_search.best_score_)

# # 使用随机搜索进行超参数调优
# param_dist = {
#     'n_estimators': sp_randint(50, 200),
#     'max_depth': [None] + list(sp_randint(10, 20).rvs(10)),
#     'min_samples_leaf': sp_randint(1, 5)
# }


# random_search = RandomizedSearchCV(rf, param_distributions=param_dist, n_iter=20,
#                                       cv=cv, scoring='roc_auc', n_jobs=-1, random_state=17)
# random_search.fit(X_train, y_train)

# print(random_search.best_params_, random_search.best_score_)