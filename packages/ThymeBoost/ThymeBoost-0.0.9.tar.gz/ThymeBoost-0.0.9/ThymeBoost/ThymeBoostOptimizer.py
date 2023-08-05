# -*- coding: utf-8 -*-

import itertools as it
import pandas as pd
from tqdm import tqdm
import traceback
import numpy as np
from toolz import unique
from ThymeBoost.CostFunctions import calc_smape, calc_mape, calc_mse, calc_mae
from timeit import default_timer as timer

class ThymeBoostOptimizer:   
    def __init__(self,
                 model_object,
                 y,
                 seasonal_period,
                 optimization_type,
                 optimization_strategy,
                 optimization_steps,
                 lag,
                 optimization_metric,
                 forecast_horizon,
                 test_set,
                 trend_cap_target,
                 global_cost,
                 split_cost,
                 min_sample_pct, 
                 approximate_splits,
                 regularization,
                 fourier_components,
                 arima_order,
                 seasonal_sample_weight,
                 params = {},
                 verbose = 1):
        self.optimization_type = optimization_type
        self.optimization_strategy = optimization_strategy
        self.lag = lag
        self.optimization_metric = optimization_metric
        seasonal_period = [[i] if type(i) == int else i for i in seasonal_period]
        self.seasonal_period = seasonal_period
        self.forecast_horizon = forecast_horizon
        if self.optimization_strategy == 'holdout':
            optimization_steps = 1
        self.optimization_steps = optimization_steps
        self.params = params
        self.y = y
        self.model_object = model_object
        self.test_set = test_set
        self.trend_cap_target = trend_cap_target
        self.verbose = verbose
        self.seasonal_sample_weight = seasonal_sample_weight
        self.global_cost = global_cost
        self.split_cost = split_cost
        self.min_sample_pct =  min_sample_pct
        self.approximate_splits = approximate_splits
        self.regularization = regularization
        self.fourier_components = fourier_components
        self.arima_order = arima_order
        
        return
    
    def set_optimization_metric(self):
        if self.optimization_metric == 'smape':
            self.optimization_metric = calc_smape
        if self.optimization_metric == 'mape':
            self.optimization_metric = calc_mape
        if self.optimization_metric == 'mse':
            self.optimization_metric = calc_mse
        if self.optimization_metric == 'mae':
            self.optimization_metric = calc_mae
            
        return
            
    def get_search_space(self):
        additive = [True,
                    # False
                    ]
        fit_type = ['global', 'local']
        poly = [1,
                # 2
                ]
        trend_estimator = ['mean',
                            # 'median',
                           'linear',
                            # 'ses',
                            # 'des',
                            # 'ar',
                           # 'loess',
                           # 'ewm'          
                            ]
        seasonality_estimator = [#'naive',
                                 'harmonic',
                                 # 'mult'
                                    ]
        seasonality = list(map(list, unique(map(tuple, self.seasonal_period))))
        parameters = list(it.product(additive,
                                     fit_type,
                                     trend_estimator,
                                     seasonality_estimator,
                                     poly,
                                     seasonality,
                                     ))        
        approved_models = [] 
        for setting in parameters:
            if not ('ets' not in setting or 'local' not in setting):
                pass
            elif not ('ses' not in setting or 'local' not in setting):
                pass
            elif not ('des' not in setting or 'local' not in setting):
                pass
            elif not ('ar' not in setting or 'local' not in setting):
                pass
            # elif not ('ewm' not in setting or 'local' not in setting):
            #     pass
            # elif not ('loess' not in setting or 'local' not in setting):
            #     pass
            # elif not (True not in setting or 'mult' not in setting):
            #     pass
            # elif ([0] in setting and False in setting):
            #     pass
            # elif ([0] in setting and 'naive' not in setting):
            #     pass
            # elif (2 in setting and 'linear' not in setting):
            #     pass
            else:
                approved_models.append(setting)
                
        return approved_models
    
    def fit(self):
        parameters = self.get_search_space()
        self.set_optimization_metric()
        results = {}
        for num_steps in range(1, self.optimization_steps + 1):
            test_y = self.y[-self.lag - num_steps + 1:]
            train_y = self.y[:-self.lag - num_steps + 1]
            # print(train_y)
            # print(test_y)
            results[str(num_steps)] = {}
            self.param_times = []
            if self.verbose:
                param_iters = tqdm(parameters)
            else:
                param_iters = parameters
            for run_settings in param_iters:
                start = timer()
                additive, fit_type, trend_estimator, seasonal_estimator, poly, seasonal_period = run_settings
                try:   
                    if self.seasonal_sample_weight is None:
                        ssw = self.seasonal_sample_weight
                    else:
                        ssw = self.seasonal_sample_weight[:len(train_y)]
                    boosted_model = self.model_object(seasonal_period = run_settings[5],
                                     fit_type = fit_type,
                                     trend_estimator = trend_estimator,
                                     params = self.params,
                                     seasonal_estimator = seasonal_estimator,
                                     additive = additive,
                                     seasonal_sample_weight = ssw,
                                     global_cost = self.global_cost,
                                     split_cost = self.split_cost,
                                     min_sample_pct = self.min_sample_pct, 
                                     approximate_splits = self.approximate_splits,
                                     regularization = self.regularization,
                                     fourier_components = self.fourier_components,
                                     arima_order = self.arima_order,
                                     poly = poly
                                     
                                     )
                    output = boosted_model.fit(train_y, forecast_horizon = self.lag)
                    #print(output['predicted'])
                    predicted = output['predicted']
                    if self.test_set == 'all':
                        test_error = self.optimization_metric(A=test_y, F=predicted)
                    elif self.test_set == 'last':
                        test_error = self.optimization_metric(A=test_y[-1], F=predicted[-1])
                    test_me = test_y[:self.lag]
                    test_me = test_me.to_frame()
                    test_me['predicted'] = predicted
                   
                    #results[str(num_steps)][','.join(map(str, run_settings))] = test_y[self.lag - 1], predicted
                    #error = (test_y[self.lag - 1] - predicted)
                    # if error < 0:
                    #     error = error * .5
                    results[str(num_steps)][','.join(map(str, run_settings))] = test_error
                    #results[str(num_steps)][','.join(map(str, run_settings))] = test_error
                    end = timer()
                    self.param_times.append((run_settings, end - start))
                except Exception as e:
                    results[str(num_steps)][','.join(map(str, run_settings))] = np.inf
                    print(f'{e} Error running settings: {run_settings}')
                    traceback.print_exc()
        
        return results
    
    def predict(self):
        opt_results = self.fit()  
        average_result = {}
        for key in opt_results['1'].keys():
            summation = 0
            for step in opt_results.keys():
                summation+= opt_results[step][key]
            average_result[key] = summation / len(opt_results.keys())
        if self.verbose:
            for step in opt_results.keys():
                print(f'{step} Step Mean: {np.mean(list(opt_results[step].values()))}')
                print(f'{step} Step Median: {np.median(list(opt_results[step].values()))}')
                print(f'{step} Step Max: {max(opt_results[step], key=opt_results[step].get),float(np.max(list(opt_results[step].values())))}')
                print(f'{step} Step Min: {min(opt_results[step], key=opt_results[step].get),float(np.min(list(opt_results[step].values())))}')

        average_result = pd.Series(average_result)
        average_result = average_result.sort_values()    
        run_settings = average_result.index[0].replace('[', '').replace(']', '').split(',')
        additive, fit_type, trend_estimator, seasonal_estimator, poly, *seasonal_period = run_settings
        seasonal_period = [int(i.strip()) for i in seasonal_period]
        boosted_model = self.model_object(seasonal_period = seasonal_period,
                         fit_type = fit_type,
                         trend_estimator = trend_estimator,
                         params = self.params,
                         poly = int(poly),
                         seasonal_estimator = seasonal_estimator,
                         additive = eval(additive),
                         trend_cap_target = self.trend_cap_target,
                         seasonal_sample_weight = self.seasonal_sample_weight,
                         global_cost = self.global_cost,
                         split_cost = self.split_cost,
                         min_sample_pct = self.min_sample_pct, 
                         approximate_splits = self.approximate_splits,
                         regularization = self.regularization,
                         fourier_components = self.fourier_components,
                         arima_order = self.arima_order,
                         )
        output = boosted_model.fit(self.y, forecast_horizon = self.forecast_horizon)
        if self.verbose:
            print(f'Optimal model configuration: {run_settings}')
        
        return output

